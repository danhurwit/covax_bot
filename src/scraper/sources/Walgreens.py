from datetime import datetime
from pprint import pprint

import requests
from decouple import config
from requests import utils, Session

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
        session, token = self.__get_session()
        session.headers.update({'x-xsrf-token': token})
        response = session.post(url=self.scrape_url,
                                json=self.__request_payload)
        # response = {"appointmentsAvailable": "true", "stateName": "Massachusetts", "stateCode": "MA",
        #             "zipCode": "02142", "radius": 25, "days": 3}
        locations = []
        if response.json()['appointmentsAvailable']:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations

    def __get_session(self):
        s = Session()
        s.headers.update({'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
        s.get('https://www.walgreens.com/topic/promotion/covid-vaccine.jsp')
        csrf_response = s.get(self.__cookie_refresh_url)
        s.get('https://www.walgreens.com/findcare/vaccination/covid-19?ban=covid_vaccine_landing_schedule')
        s.headers.update({
            'dnt': '1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
        })
        return s, csrf_response.json()['csrfToken']
