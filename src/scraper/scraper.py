import traceback
from typing import List

from logger import logger
from models.sources.AppointmentSource import AppointmentSource
from scraper.sources.StopShop import StopShop
from scraper.sources.Hannafords import Hannafords
from scraper.sources.Walgreens import Walgreens
from scraper.sources.Cvs import Cvs
from scraper.sources.MassVax import MassVax

sources = [Cvs, MassVax, Walgreens, Hannafords, StopShop]


def scrape() -> List[AppointmentSource]:
    scraped_sources = []

    for source in sources:
        try:
            s = source()
            s.scrape_locations()
            scraped_sources.append(s)
        except:
            logger.log(traceback.format_exc())

    return scraped_sources
