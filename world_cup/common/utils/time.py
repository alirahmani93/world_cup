import datetime
from django.utils import timezone


def standard_response_datetime(time: datetime.datetime):
    return int(time.timestamp())


def get_now_time_stamp() -> int:
    return int(datetime.datetime.timestamp(timezone.now()))


def get_now():
    time = timezone.now()
    return time

