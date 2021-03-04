import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from scraper.models.AppointmentSource import AppointmentSource
from scraper.models.AvailabilityWindow import AvailabilityWindow
from scraper.models.Location import Location

URL = "https://vaxfinder.mass.gov/?zip_or_city=02139&vaccines_available=on&q="
BASE_URL = "https://vaxfinder.mass.gov"


class MassVax(AppointmentSource):

    def scrape_locations(self):
        html = requests.request(method="get", url=URL)
        global_soup = BeautifulSoup(str(html.text), "html.parser")
        location_links = []
        for a in global_soup.find_all("a", "location-place"):
            location_links.append(self.__format_link(a['href']))

        for link in location_links:
            location_result = requests.request(method="get", url=link)
            self.locations.append(self.__get_location(location_result.text))

        # location_result = open("/Users/danhurwit/Desktop/vaccine_availability.html", 'r', encoding='utf-8').read()
        # self.locations.append(self.__get_location(location_result))

    def __get_location(self, location_result: str) -> Location:
        local_soup = BeautifulSoup(str(location_result), "html.parser")
        windows = self.__get_availability_windows(local_soup)
        updated_mins = self.__parse_updated_at(local_soup.find("div", "location-updated").string.strip())
        booking_link = local_soup.find("a", "btn lg primary vertical hide-md-up full-width")['href']
        return Location(name=local_soup.find("section", "section pt").find('h1').string,
                        last_updated_mins=updated_mins,
                        booking_link=booking_link,
                        availability_windows=windows)

    def __get_availability_windows(self, local_soup):
        windows = []
        for row in local_soup.find_all("tr"):
            cells = row.findChildren('td')
            if cells:
                windows.append(AvailabilityWindow(int(cells[2].string),
                                                  datetime.strptime(cells[0].string, '%B %d, %Y')))
        return windows

    def __format_link(self, link: str) -> str:
        return BASE_URL + link

    def __parse_updated_at(self, update_string: str) -> int:
        # update_string.replace("Updated:", "")
        minutes = 0
        hours = 0
        for part in update_string.split(","):
            if part.find("minute") != -1:
                minutes = int(re.findall(r'\d+', part).pop())
            if part.find("hour") != -1:
                hours = int(re.findall(r'\d+', part).pop())
        return (hours * 60) + minutes
