import itertools
from typing import List

from scraper.models.Location import Location
from scraper.sources.MassVax import MassVax

sources = [MassVax]


def scrape() -> List[Location]:
    locations = []
    for source in sources:
        s = source()
        s.scrape_locations()
        locations.append(s.get_locations())
    return list(itertools.chain(*locations))
