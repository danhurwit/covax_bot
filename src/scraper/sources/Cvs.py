from datetime import datetime
from typing import List, Iterable

import requests

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Cvs(AppointmentSource):
    name = "CVS"
    scrape_url = 'https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.ma.json?vaccineinfo'
    global_booking_link = 'https://www.cvs.com/vaccine/intake/store/cvd-schedule?icid=coronavirus-lp-vaccine-ma-statetool'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/CVS_Health_Logo.svg/2560px-CVS_Health_Logo.svg.png",
        "FF5C5C")

    def scrape_locations(self):
        json = requests.request(method="get", url=self.scrape_url).json()
        sites = json['responsePayloadData']['data']['MA']
        locations = []
        for site in sites:
            site_name = self.name + ': ' + site['city'].capitalize()
            status = site['status']
            # if site['city'] == 'NEWTON' or site['city'] == 'GREENFIELD':
            #     locations.append(Location(site_name,
            #                               self.global_booking_link,
            #                               datetime.now(),
            #                               [AvailabilityWindow(1, datetime.now())]))
            if not status == 'Fully Booked':
                locations.append(Location(site_name,
                                          self.get_global_booking_link(),
                                          datetime.now(),
                                          [AvailabilityWindow(1, datetime.now())]))
            else:
                locations.append(Location(site_name, self.get_global_booking_link(), datetime.now(), []))
        self.locations = locations

    def get_availability_message(self, locations: Iterable[Location]) -> List[str]:
        messages = []
        for location in locations:
            base = "Site Name: {}\nBooking Link: {}\n".format(location.get_name(), location.get_link())
            base += "CVS has added appointments\n"
            messages.append(base)
        return messages
