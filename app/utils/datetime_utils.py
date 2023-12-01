from datetime import datetime, timedelta, time


def convert_date_to_string(date: datetime.date) -> str:
    """Converts a datetime.date object to a string in the format '%Y-%m-%d'."""
    return date.strftime("%Y-%m-%d")


def convert_string_to_datetime(date_str: str) -> datetime:
    """Converts a string in the format '%Y-%m-%d' to a datetime object."""
    date_format = "%Y-%m-%d"
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        raise ValueError(
            "Invalid date format. Please provide a date in the format '%Y-%m-%d'."
        )


def get_dates_between(start_date: datetime.date, end_date: datetime.date) -> list:
    """
    Returns a list of dates between the start_date and end_date (inclusive).

    Args:
        start_date (datetime.date): The start date.
        end_date (datetime.date): The end date.

    Returns:
        list: List of datetime.date objects.
    """
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


def check_dates_order(start_date: datetime.date, end_date: datetime.date):
    """
    Checks if the start_date is before the end_date.

    Raises:
        ValueError: If start_date is not before end_date.
    """
    if start_date > end_date:
        raise ValueError("Start date must be before the end date.")


def check_date_is_not_today_or_future(given_date: datetime.date):
    """
    Checks if the given_date is not today or in the future.

    Raises:
        ValueError: If the given_date is today or in the future.
    """
    current_date = datetime.now()
    if given_date > current_date:
        raise ValueError("You can't request a date that is today or in the future.")


def create_timestamp_from_date_and_hour(given_day: datetime.date, hour: int) -> str:
    """
    Create a timestamp string from the given date and hour.

    Args:
        given_day (datetime.date): The date.
        hour (int): The hour.

    Returns:
        str: Timestamp string in the format '%Y-%m-%d %H:%M:%S'.
    """
    created_time = time(hour=hour, minute=0, second=0)
    created_timestamp = datetime.combine(given_day, created_time)
    return created_timestamp.strftime("%Y-%m-%d %H:%M:%S")
