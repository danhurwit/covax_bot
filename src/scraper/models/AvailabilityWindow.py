class AvailabilityWindow:
    num_available: int = 0
    date: str = ""

    def __init__(self, num_available, date):
        self.num_available = num_available
        self.date = date

    def get_num_available(self) -> int:
        return self.num_available

    def get_date(self) -> str:
        return self.date
