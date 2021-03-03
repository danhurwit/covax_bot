from datetime import datetime, timedelta
from typing import List

from .AvailabilityWindow import AvailabilityWindow


class Location:
    link: str = ""
    name: str = ""
    last_updated_mins: int = 0
    availability_windows: List[AvailabilityWindow] = []

    def __init__(self, link: str, name: str, last_updated_mins: int):
        self.link = link
        self.name = name
        self.last_updated_mins = last_updated_mins

    def get_link(self) -> str:
        return self.link

    def get_name(self) -> str:
        return self.name

    def get_last_updated(self) -> datetime:
        return datetime.now() - timedelta(minutes=self.last_updated_mins)
