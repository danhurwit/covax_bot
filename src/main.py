from publisher import publisher
from scraper import scraper

if __name__ == "__main__":
    locations = scraper.scrape()
    print(locations)
    publisher.publish(locations)
