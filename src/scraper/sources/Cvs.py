from datetime import datetime
from typing import List, Iterable

import requests

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.Location import Location

CVS_NAME = "CVS"

URL = 'https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.ma.json?vaccineinfo'
BOOKING_URL = 'https://www.cvs.com/vaccine/intake/store/cvd-schedule?icid=coronavirus-lp-vaccine-ma-statetool'


class Cvs(AppointmentSource):
    def get_name(self):
        return CVS_NAME

    def scrape_locations(self):
        json = requests.request(method="get", url=URL).json()
        sites = json['responsePayloadData']['data']['MA']
        locations = []
        for site in sites:
            site_name = CVS_NAME + ': ' + site['city'].capitalize()
            status = site['status']
            if not status == 'Fully Booked':
                locations.append(Location(site_name,
                                          BOOKING_URL,
                                          datetime.now(),
                                          [AvailabilityWindow(1, datetime.now())]))
            else:
                locations.append(Location(site_name, BOOKING_URL, datetime.now(), []))
        self.locations = locations

    def get_publish_messages(self, locations: Iterable[Location]) -> List[str]:
        messages = []
        for location in locations:
            base = "Site Name: {}\nBooking Link: {}\n".format(location.get_name(), location.get_link())
            base += "CVS has added appointments\n"
            messages.append(base)
        return messages
