from datetime import datetime

import pprint
from requests import Session

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Walgreens(AppointmentSource):
    name = "Walgreens"
    scrape_url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability/'
    __request_payload = {"serviceId": "99",
                         "position": {"latitude": 42.36475590000001, "longitude": -71.1032591},
                         "appointmentAvailability": {"startDateTime": "2021-03-22"},
                         "radius": 25}
    global_booking_link = 'https://www.walgreens.com/topic/promotion/covid-vaccine.jsp'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        session, token = self.__get_session()
        session.headers.update({'x-xsrf-token': token})
        response = session.post(url=self.scrape_url,
                                json=self.__request_payload)
        locations = []
        if response.json()['appointmentsAvailable']:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations

    def __get_session(self):
        s = Session()
        s.get('https://www.walgreens.com/topic/promotion/covid-vaccine.jsp')
        csrf_response = s.get('https://www.walgreens.com/topic/v1/csrf')
        s.get('https://www.walgreens.com/findcare/vaccination/covid-19?ban=covid_vaccine_landing_schedule')
        return s, csrf_response.json()['csrfToken']
