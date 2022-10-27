import datetime


def get_formatted_date(schedule_date: str, date_format: str) -> datetime.datetime:
    return datetime.datetime.strptime(schedule_date, date_format)
