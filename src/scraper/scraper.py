from typing import List

from models.sources.AppointmentSource import AppointmentSource
from scraper.sources.MassVax import MassVax

sources = [MassVax]


def scrape() -> List[AppointmentSource]:
    scraped_sources = []
    for source in sources:
        s = source()
        s.scrape_locations()
        scraped_sources.append(s)
    return scraped_sources
