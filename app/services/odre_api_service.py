from datetime import datetime
import requests
from ..utils.datetime_utils import (
    convert_date_to_string,
    create_timestamp_from_date_and_hour,
)


class ODREApiService:
    """Service for interacting with the ODRE API to retrieve CO2 emissions data."""

    def __init__(self):
        """Initialize the ODREApiService with the API base URL and timezone."""
        self.ODRE_API_BASE_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records"
        self.timezone = "Europe / Paris"

    def get_co2_emissions_per_hour(self, given_day: datetime.date) -> list:
        """
        Get CO2 emissions data for each hour on the given day.

        Args:
            given_day (datetime.date): The date for which to retrieve CO2 emissions data.

        Returns:
            list: List of dictionaries containing CO2 emission date and value.
        """
        try:
            converted_date_to_string = convert_date_to_string(given_day)

            params = {
                "select": "sum(taux_co2) as emission_co2",
                "where": f"date = '{converted_date_to_string}'",
                "group_by": "hour(date_heure) as hour",
                "limit": "24",
            }

            try:
                response = requests.get(self.ODRE_API_BASE_URL, params=params)
                response.raise_for_status()

                return [
                    {
                        "co2_emission_date": create_timestamp_from_date_and_hour(
                            given_day, element.get("hour")
                        ),
                        "co2_emission_value": element.get("emission_co2"),
                    }
                    for element in response.json().get("results", [])
                ]
            except requests.RequestException as e:
                raise Exception(f"Error communicating with API: {e}")

        except ValueError as e:
            return e
