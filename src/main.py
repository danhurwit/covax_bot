from publisher import publisher
from scraper import scraper
from validator import appointments_dao

if __name__ == "__main__":
    locations = scraper.scrape()
    print('Locations Available: {}'.format(len(list(filter(lambda l: l.has_availability(), locations)))))
    unavailable_locations = list(filter(lambda l: not l.has_availability(), locations))
    available_locations = list(filter(lambda l: l.has_availability(), locations))

    locs_to_publish = set()
    for location in available_locations:
        for window in location.get_availability_windows():
            if window.num_available > appointments_dao.get_site_availability(location.get_name(), window.date):
                locs_to_publish.add(location)
            appointments_dao.update_site_availability(location.get_name(), window.get_date(), window.get_num_available())

    publisher.publish_locations(locs_to_publish)
    appointments_dao.reset_availability(list(map(lambda l: l.get_name(), unavailable_locations)))
