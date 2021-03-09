from typing import List, Iterable

from models.sources.Location import Location


class AppointmentSource:
    name: str = ""
    locations: List[Location] = []
    has_time_availability: bool = False
    has_location_booking_links: bool = False
    global_booking_link = ""
    all_locations_queryable = True
    display_properties = None
    scrape_url = ""

    def scrape_locations(self):
        pass

    def get_locations(self) -> List[Location]:
        return self.locations

    def get_booking_links(self) -> List[str]:
        return list(map(lambda l: l.link, self.locations))

    def get_name(self):
        return self.name

    def get_availability_message(self, locations: Iterable[Location]) -> List[str]:
        pass

    def get_global_booking_link(self) -> str:
        return self.global_booking_link

    def has_time_based_availability(self) -> bool:
        return self.has_time_availability

    def has_location_based_booking(self) -> bool:
        return self.has_location_booking_links

    def can_query_all_locations(self) -> bool:
        return self.all_locations_queryable

    def get_display_props(self):
        return self.display_properties
