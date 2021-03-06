from typing import List

from data import appointments_dao, availability_records_dao
from models.sources.AppointmentSource import AppointmentSource
from models.sources.Location import Location
from publisher import publisher
from scraper import scraper


def run():
    sources = scraper.scrape()
    for source in sources:
        locations_to_publish = get_locations_to_publish(source)
        if locations_to_publish:
            publisher.publish_locations(source, locations_to_publish)
            record_availability(locations_to_publish, source)
        if source.should_update_availability:
            update_availability_counts(source)
        print("Found new availability at: {} / {} {} sites..."
              .format(len(locations_to_publish), len(source.get_locations()), source.get_name()))


def record_availability(locations_to_publish, source):
    for loc in locations_to_publish:
        availability_records_dao.create_availability_record(source.get_name(), loc.get_name())


def get_locations_to_publish(source: AppointmentSource) -> List[Location]:
    locations = source.get_locations()
    source_name = source.get_name()
    available_locations = list(filter(lambda l: l.has_availability(), locations))
    locs = set()
    for location in available_locations:
        for window in location.get_availability_windows():
            if window.num_available > appointments_dao.get_site_availability(source_name,
                                                                             location.get_name(),
                                                                             window.get_date()):
                locs.add(location)
    return locs


def update_availability_counts(source: AppointmentSource):
    locations = source.get_locations()
    source_name = source.get_name()
    available_locations = []
    for location in locations:
        if location.has_availability():
            available_locations.append(location)
            for window in location.get_availability_windows():
                appointments_dao.update_site_availability(source_name,
                                                          location.get_name(),
                                                          window.get_date(),
                                                          window.get_num_available())
    appointments_dao.reset_availability_excluding(source_name, list(map(lambda l: l.get_name(), available_locations)))
