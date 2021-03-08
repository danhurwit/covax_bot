import re
from datetime import datetime, timedelta
from typing import List, Iterable

import requests
from bs4 import BeautifulSoup

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.Location import Location

URL = "https://vaxfinder.mass.gov/?zip_or_city=02139"
BASE_URL = "https://vaxfinder.mass.gov"
MASSVAX_NAME = "MassVax"


class MassVax(AppointmentSource):

    def get_name(self):
        return MASSVAX_NAME

    def scrape_locations(self):
        html = requests.request(method="get", url=URL).text
        # html = open("/Users/danhurwit/Desktop/test_html/massvax/locations_available.htm", 'r', encoding='utf-8').read()  # test data
        global_soup = BeautifulSoup(str(html), "html.parser")
        num_pages = self.__get_num_pages(global_soup)

        locations: List[Location] = []
        for i in range(num_pages):
            page_html = requests.request(method="get", url=self.__get_url_for_page(i + 1)).text
            # page_html = open("/Users/danhurwit/Desktop/test_html/massvax/locations_available.htm", 'r', encoding='utf-8').read()  # test data
            page_soup = BeautifulSoup(str(page_html), "html.parser")
            for row in page_soup.find("tbody").find_all("tr"):
                cells = row.findChildren('td')
                if cells:
                    locations.append(self.__parse_location_from_row(cells))

        self.locations = locations

    def get_publish_messages(self, locations: Iterable[Location]) -> List[str]:
        messages = []
        for location in locations:
            base = "Site Name: {}\nBooking Link: {}\nAvailability:\n".format(location.get_name(),
                                                                             location.get_link())
            for window in location.get_availability_windows():
                base += ("\t" + "{} available on {}".format(window.get_num_available(),
                                                            window.get_date().strftime("%Y-%m-%d"))
                         + "\n")
            messages.append(base)
        return messages

    def __parse_location_from_row(self, cells) -> Location:
        availability = cells[2].find("span", "text").string
        details_url = self.__get_location_details_url(cells[0].find('a')['href'])
        if availability == 'Currently Full' or availability == 'See Details':
            name = ''.join(e for e in cells[0].find('a').string if e.isalnum() or e == ' ' or e == ':').strip()
            last_updated = self.__parse_updated_at(cells[0].find('p', 'location-updated').string)
            return Location(name, details_url, self.__datetime_from_minutes(last_updated), [])
        else:
            return self.__get_location(details_url)

    def __get_url_for_page(self, page: int):
        return URL + '&' + 'page={}'.format(page)

    def __get_location(self, link: str) -> Location:
        page_html = requests.request(method="get", url=link).text
        # page_html = open("/Users/danhurwit/Desktop/test_html/massvax/vaccine_availability.html", 'r', encoding='utf-8').read()  # test data
        local_soup = BeautifulSoup(page_html, "html.parser")
        windows = self.__get_availability_windows(local_soup)
        updated_mins = self.__parse_updated_at(local_soup.find("div", "location-updated").string.strip())
        booking_link = local_soup.find("a", "btn lg primary vertical hide-md-up full-width")['href']
        return Location(name=local_soup.find("section", "section pt").find('h1').string,
                        updated_at=self.__datetime_from_minutes(updated_mins),
                        booking_link=booking_link,
                        availability_windows=windows)

    def __datetime_from_minutes(self, updated_mins):
        return datetime.now() - timedelta(minutes=updated_mins)

    def __get_availability_windows(self, local_soup):
        windows = []
        for row in local_soup.find_all("tr"):
            cells = row.findChildren('td')
            if cells:
                windows.append(AvailabilityWindow(int(cells[2].string),
                                                  datetime.strptime(cells[0].string, '%B %d, %Y')))
        return windows

    def __get_location_details_url(self, link: str) -> str:
        return BASE_URL + link

    def __parse_updated_at(self, update_string: str) -> int:
        minutes = 0
        hours = 0
        days = 0
        weeks = 0
        for part in update_string.split(","):
            if part.find("minute") != -1:
                minutes = int(re.findall(r'\d+', part).pop())
            elif part.find("hour") != -1:
                hours = int(re.findall(r'\d+', part).pop())
            elif part.find("day") != -1:
                days = int(re.findall(r'\d+', part).pop())
            elif part.find("week") != -1:
                weeks = int(re.findall(r'\d+', part).pop())
        return (weeks * 7 * 24 * 60) + (days * 24 * 60) + (hours * 60) + minutes

    def __get_num_pages(self, global_soup) -> int:
        pagination_string: str = global_soup.find("div", "pagination").find("p", "current").string
        page_string = pagination_string.strip().split(" ").pop().replace(".", "")
        return int(page_string)
