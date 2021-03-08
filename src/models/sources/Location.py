from datetime import datetime, timedelta
from functools import reduce
from typing import Iterable

from models.sources.AvailabilityWindow import AvailabilityWindow


class Location:
    booking_link: str = ""
    name: str = ""
    updated_at: datetime = 0
    availability_windows: Iterable[AvailabilityWindow] = []

    def __init__(self, name: str, booking_link: str, updated_at: datetime, availability_windows: Iterable[AvailabilityWindow]):
        self.booking_link = booking_link
        self.name = name
        self.updated_at = updated_at
        self.availability_windows = availability_windows

    def get_link(self) -> str:
        return self.booking_link

    def get_name(self) -> str:
        return self.name

    def get_last_updated(self) -> datetime:
        return self.updated_at

    def get_availability_windows(self) -> Iterable[AvailabilityWindow]:
        return self.availability_windows

    def has_availability(self) -> bool:
        if self.availability_windows:
            return reduce(lambda x, y: x + y, map(lambda a: a.get_num_available(), self.availability_windows)) > 0
        return False
