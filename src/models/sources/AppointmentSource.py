from typing import List
from models.sources.Location import Location


class AppointmentSource:
    locations: List[Location] = []

    def scrape_locations(self):
        pass

    def get_locations(self) -> List[Location]:
        return self.locations

    def get_booking_links(self) -> List[str]:
        return list(map(lambda l: l.link, self.locations))
