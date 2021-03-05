from publisher import publisher
from scraper import scraper

if __name__ == "__main__":
    locations = scraper.scrape()
    print('Locations Available: {}'.format(len(list(filter(lambda l: l.has_availability(), locations)))))
    publisher.publish(locations)
