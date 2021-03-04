from scraper.sources.MassVax import MassVax

sources = [MassVax]


def scrape():
    for source in sources:
        s = source()
        s.scrape_locations()

        for location in s.get_locations():
            print(location.format_message())
