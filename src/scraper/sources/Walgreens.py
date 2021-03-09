import json
from datetime import datetime
from typing import List, Iterable

import requests
from decouple import config

from logger import logger
from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Walgreens(AppointmentSource):
    name = "Walgreens"
    scrape_url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability'
    __request_payload = {"serviceId": "99", "position": {"latitude": 42.36475590000001, "longitude": -71.1032591},
                         "appointmentAvailability": {"startDateTime": "2021-03-09"}, "radius": 25}
    __headers = {'cookie': config('WALGREENS_COOKIE'), 'x-xsrf-token': config('WALGREENS_TOKEN')}
    #  FIXME: change once walgreens has availability
    global_booking_link = 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        response = requests.post(url=self.scrape_url,
                                 json=self.__request_payload,
                                 headers=self.__headers).json()
        # response = {"appointmentsAvailable": "true", "stateName": "Massachusetts", "stateCode": "MA",
        #             "zipCode": "02142", "radius": 25, "days": 3}
        locations = []
        if response['appointmentsAvailable']:
            logger.log("wallgreens appointment: {}".format(response))
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations
