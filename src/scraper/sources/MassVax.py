import requests
from bs4 import BeautifulSoup

from scraper.models.AppointmentSource import AppointmentSource

URL = "https://vaxfinder.mass.gov/?zip_or_city=02139&vaccines_available=on&q="
BASE_URL = "https://vaxfinder.mass.gov"


class MassVax(AppointmentSource):

    def scrape_locations(self):
        html = requests.request(method="get", url=URL)
        soup = BeautifulSoup(str(html.text), "html.parser")
        location_links = []
        for a in soup.find_all("a", "location-place"):
            location_links.append(self.__format_link(a['href']))

        print(location_links)

    def __format_link(self, link: str) -> str:
        return BASE_URL + link
