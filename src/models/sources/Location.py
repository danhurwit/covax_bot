from datetime import datetime, timedelta
from functools import reduce
from typing import Iterable

from models.sources.AvailabilityWindow import AvailabilityWindow


class Location:
    booking_link: str = ""
    name: str = ""
    last_updated_mins: int = 0
    availability_windows: Iterable[AvailabilityWindow] = []

    def __init__(self, name: str, booking_link: str, last_updated_mins: int, availability_windows: Iterable[AvailabilityWindow]):
        self.booking_link = booking_link
        self.name = name
        self.last_updated_mins = last_updated_mins
        self.availability_windows = availability_windows

    def get_link(self) -> str:
        return self.booking_link

    def get_name(self) -> str:
        return self.name

    def get_last_updated(self) -> datetime:
        return datetime.now() - timedelta(minutes=self.last_updated_mins)

    def get_availability_windows(self) -> Iterable[AvailabilityWindow]:
        return self.availability_windows

    def has_availability(self) -> bool:
        if self.availability_windows:
            return reduce(lambda x, y: x + y, map(lambda a: a.get_num_available(), self.availability_windows)) > 0
        return False

    def format_message(self) -> str:
        base = "Site Name: {}\nBooking Link: {}\nAvailability:\n".format(self.name, self.booking_link)
        for window in self.availability_windows:
            base += ("\t" + window.get_formatted_availability() + "\n")
        return base
