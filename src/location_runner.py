from data import appointments_dao
from publisher import publisher
from scraper import scraper


def run():
    locations = scraper.scrape()

    locations_to_publish = get_locations_to_publish(locations)
    publisher.publish_locations(locations_to_publish)

    update_availability_counts(locations)

    print("Found new availability at: {} / {} sites".format(len(locations_to_publish), len(locations)))


def get_locations_to_publish(locations):
    available_locations = list(filter(lambda l: l.has_availability(), locations))
    locs = set()
    for location in available_locations:
        for window in location.get_availability_windows():
            if window.num_available > appointments_dao.get_site_availability(location.get_name(), window.date):
                locs.add(location)
    return locs


def update_availability_counts(locations):
    unavailable_locations = []
    for location in locations:
        if location.has_availability():
            for window in location.get_availability_windows():
                appointments_dao.update_site_availability(location.get_name(), window.get_date(), window.get_num_available())
        else:
            unavailable_locations.append(location)
    appointments_dao.reset_availability(list(map(lambda l: l.get_name(), unavailable_locations)))
