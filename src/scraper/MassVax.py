from typing import List

import requests

from bs4 import BeautifulSoup
from scraper.AppointmentSource import AppointmentSource
from scraper.Location import Location

URL = "https://vaxfinder.mass.gov/?zip_or_city=02139&vaccines_available=on&q="
BASE_URL = "https://vaxfinder.mass.gov/"


class MassVax(AppointmentSource):

    def scrape_locations(self):
        html = requests.request(method="get", url=URL)
        soup = BeautifulSoup(str(html.text), "html.parser")
        locations = soup.find_all("div", class_="location-card")
        # print(locations)
        print(locations[0])
        # for location in locations:
        #     print(location)
        #     # local_soup = BeautifulSoup(location, "html.parser")
        #     # print(local_soup.find_all("div", "location-updated"))
        #     # self.locations.append(Location())

    def __format_link(self, link: str):
        pass
