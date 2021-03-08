from typing import List, Iterable
from models.sources.Location import Location


class AppointmentSource:
    name: str = ""
    locations: List[Location] = []

    def scrape_locations(self):
        pass

    def get_locations(self) -> List[Location]:
        return self.locations

    def get_booking_links(self) -> List[str]:
        return list(map(lambda l: l.link, self.locations))

    def get_name(self):
        return self.name

    def get_publish_messages(self, locations: Iterable[Location]) -> List[str]:
        pass
