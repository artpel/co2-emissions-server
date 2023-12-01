from fastapi import APIRouter, HTTPException
from ....utils.datetime_utils import (
    convert_string_to_datetime,
    get_dates_between,
    check_dates_order,
    check_date_is_not_today_or_future,
)
from ....services import odre_api_service

router = APIRouter()


@router.get("/getCO2emissions")
def get_co2_emissions(start_date: str, end_date: str):
    """
    Retrieve CO2 emissions data for a range of dates.

    Args:
        start_date (str): The start date (format: 'YYYY-MM-DD').
        end_date (str): The end date (format: 'YYYY-MM-DD').

    Returns:
        dict: Dictionary with date keys and CO2 emissions data values.

    Raises:
        HTTPException: If any error occurs during processing.
    """
    try:
        start_date_as_datetime = convert_string_to_datetime(start_date)
        end_date_as_datetime = convert_string_to_datetime(end_date)
        check_dates_order(start_date_as_datetime, end_date_as_datetime)
        check_date_is_not_today_or_future(start_date_as_datetime)
        check_date_is_not_today_or_future(end_date_as_datetime)

        dates = get_dates_between(start_date_as_datetime, end_date_as_datetime)

        api_service = odre_api_service.ODREApiService()
        return {date: api_service.get_co2_emissions_per_hour(date) for date in dates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
