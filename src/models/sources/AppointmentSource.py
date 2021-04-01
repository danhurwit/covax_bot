from typing import List, Iterable

from models.sources.Location import Location


class AppointmentSource:
    name: str = ""
    locations: List[Location] = []
    has_time_availability: bool = False
    has_location_booking_links: bool = False
    should_update_availability: bool = True
    global_booking_link = ""
    display_properties = None
    scrape_url = ""

    def scrape_locations(self):
        pass

    def get_locations(self) -> List[Location]:
        return self.locations

    def get_name(self):
        return self.name

    def get_global_booking_link(self) -> str:
        return self.global_booking_link

    def has_time_based_availability(self) -> bool:
        return self.has_time_availability

    def has_location_based_booking(self) -> bool:
        return self.has_location_booking_links

    def get_display_props(self):
        return self.display_properties
