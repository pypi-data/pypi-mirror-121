# pylint: disable=no-self-use
import json
import time
from datetime import datetime
from urllib.error import URLError

import pandas as pd
import requests

from sdc_dp_helpers.api_utilities.date_managers import date_handler
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler


class CustomOneSignalReader:
    def __init__(self, creds_file, config_file=None):
        self._creds = load_file(creds_file, "yml")
        self._config = load_file(config_file, "yml")

        self._header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {self._creds.get('api_key')}",
            "User-Agent": "Mozilla/5.0",
        }

        self._request_session = requests.Session()
        self.offset, self.data_set = 0, []

    @retry_handler(exceptions=KeyError, total_tries=5, should_raise=True)
    def _csv_export_query(self):
        """
        Query handler for csv_export.
        https://documentation.onesignal.com/reference/csv-export

        Generate a compressed CSV export of all of your current user data.
        This method can be used to generate a compressed CSV export of all
        of your current user data. It is a much faster alternative than
        retrieving this data using the /players API endpoint.
        The file will be compressed using GZip.
        The file may take several minutes to generate depending on the number
        of users in your app.
        The URL generated will be available for 3 days and includes random v4
        uuid as part of the resource name to be unguessable.

        ⚠ Note that adding any date oriented payload drastically affects
        the output data. Even if the payload values are null.
        """
        print("POST: csv_export.")
        # response is not always successful for some reason, so retry handler
        # handles the missing "csv_file_url" key response
        response: dict = self._request_session.post(
            url="https://onesignal.com/api/v1/players/csv_export",
            headers=self._header,
            json={"app_id": self._creds.get("app_id")},
        ).json()

        # status code is not always returned, so handling error strings instead
        errors = response.get("errors", [None])[0]
        if errors:
            # The header is definitely valid, so we must assume the app_id is not
            if (
                    errors
                    == "app_id not found. You may be missing a Content-Type: application/json header."
            ):
                raise EnvironmentError(
                    "App Id may not be valid or removed from the account."
                )

            # Seems like we are restricted to making one query at a time for a given user, so wait 5 minutes
            if (
                    errors
                    == "User already running another CSV export. Please wait until your other CSV exporter finishes and try again."
            ):
                time.sleep(300)  # the reader may try again after the 5 minute wait
                raise EnvironmentError(errors)

            # Raise all other unknown errors in a standard fashion
            raise EnvironmentError(errors)
        else:
            print("No errors raised, fetching url.")

        response = response["csv_file_url"]
        attempts = 0
        while True:
            try:
                # Making use of pandas to stream the
                # compressed csv data directly to a df
                _date_fmt = "%Y-%m-%d"
                data_frame: pd.DataFrame = pd.read_csv(response)

                # added functionality to filter results by created_at
                # note the filter can not exceed the last 30 days
                sd = date_handler(self._config.get("start_date", None), _date_fmt)
                ed = date_handler(self._config.get("end_date", None), _date_fmt)
                if sd is not None and ed is not None:
                    # using a temp date field to select relevant data before dropping
                    data_frame["tmp_date"] = pd.to_datetime(data_frame["created_at"])
                    data_frame["tmp_date"] = data_frame["tmp_date"].dt.strftime(
                        _date_fmt
                    )
                    data_frame = data_frame[
                        (
                                data_frame["tmp_date"]
                                >= datetime.strptime(sd, _date_fmt).strftime(_date_fmt)
                        )
                        & (
                                data_frame["tmp_date"]
                                <= datetime.strptime(ed, _date_fmt).strftime(_date_fmt)
                        )
                        ]
                    data_frame.drop("tmp_date", axis="columns", inplace=True)
                break
            except URLError:
                # max wait time is 15 minutes at 10 attempts before we need to contact Onesignal
                print(f"Waiting for file to generate, attempt {attempts}.")
                time.sleep(90)

            attempts += 1

            if attempts >= 10:
                raise URLError(
                    f"Csv file could not be generated, contact Onesignal support. "
                    f"Response {response}."
                )

        return data_frame.to_json(orient="records")

    @retry_handler(exceptions=ConnectionError, total_tries=5, should_raise=True)
    def _view_notifications_query(self):
        """
        Query handler for view_notifications.
        https://documentation.onesignal.com/reference/view-notifications

        View the details of multiple notifications.
        OneSignal periodically deletes records of API notifications
        older than 30 days.
        If you would like to export all notification data to CSV,
        you can do this through the dashboard.

        ⚠ Note that adding any date oriented payload drastically affects
        the output data. Even if the payload values are null.
        """
        print("GET: view_notifications.")
        initial_response = self._request_session.get(
            url="https://onesignal.com/api/v1/notifications",
            headers=self._header,
            json={"app_id": self._creds.get("app_id")},
        )

        total_offset = initial_response.json().get("total_count")
        for offset in range(self.offset, total_offset):
            print(f"At offset: {offset} of {total_offset}.")
            response = self._request_session.get(
                url="https://onesignal.com/api/v1/notifications",
                headers=self._header,
                json={"app_id": self._creds.get("app_id"), "offset": offset},
            )

            if response.status_code == 200:
                # if no more data is present skip response
                data = response.json().get("notifications", None)
                if data is None:
                    continue
                self.data_set.append(data)

                # keep offset safe if retry is needed
                self.offset += 1

            elif response.status_code == 524:
                # Onesignal states 524 is server failure and shutdown, and suggests
                # waiting 5 minutes before trying again.
                time.sleep(300)
            else:
                raise ConnectionError(
                    f"Connection failed with {response.status_code} and {response.reason}."
                )

        return json.dumps(self.data_set)

    def run_query(self):
        """
        The Onesignal API provides programmatic methods to
        access data in Onesignal for view_notifications and csv_exports.
        """
        _endpoint = self._config.get("endpoint")
        if _endpoint == "csv_export":
            return self._csv_export_query()
        elif _endpoint == "view_notifications":
            return self._view_notifications_query()
        else:
            raise EnvironmentError(f"Endpoint {_endpoint} is not supported.")
