from datetime import datetime
from pprint import pprint

import requests
from decouple import config
from requests import utils

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Walgreens(AppointmentSource):
    name = "Walgreens"
    scrape_url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability'
    __request_payload = {"serviceId": "99",
                         "position": {"latitude": 42.36475590000001, "longitude": -71.1032591},
                         "appointmentAvailability": {"startDateTime": "2021-03-21"},
                         "radius": 25}
    __cookie_refresh_url = 'https://www.walgreens.com/topic/v1/csrf'
    global_booking_link = 'https://www.walgreens.com/topic/promotion/covid-vaccine.jsp'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        csrf_token, cookies = self.__refresh_cookies()
        headers = requests.utils.default_headers()
        headers.update({'x-xsrf-token': config('WALGREENS_TOKEN'),
                        'cookie': config('WALGREENS_COOKIE')})
        response = requests.post(url=self.scrape_url,
                                 json=self.__request_payload,
                                 headers=headers)
        # response = {"appointmentsAvailable": "true", "stateName": "Massachusetts", "stateCode": "MA",
        #             "zipCode": "02142", "radius": 25, "days": 3}
        locations = []
        if response.json()['appointmentsAvailable']:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations

    def __refresh_cookies(self):
        resp = requests.get(self.__cookie_refresh_url)
        return resp.json()['csrfToken'], resp.cookies.copy()
