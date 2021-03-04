from datetime import datetime


class AvailabilityWindow:
    num_available: int = 0
    date: datetime = None

    def __init__(self, num_available, date):
        self.num_available = num_available
        self.date = date

    def get_num_available(self) -> int:
        return self.num_available

    def get_date(self) -> datetime:
        return self.date

    def get_formatted_availability(self) -> str:
        return "{} available on {}".format(self.num_available, self.date.strftime("%Y-%m-%d"))
