import gzip
import json
import logging
from datetime import datetime
from pprint import pprint
import curlify

from urllib import request, parse

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Walgreens(AppointmentSource):
    name = "Walgreens"
    scrape_url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability'
    __request_payload = {"serviceId": "99",
                         "position": {"latitude": 42.36475590000001, "longitude": -71.1032591},
                         "appointmentAvailability": {"startDateTime": "2021-03-22"},
                         "radius": 25}
    global_booking_link = 'https://www.walgreens.com/topic/promotion/covid-vaccine.jsp'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        logging.basicConfig(level=logging.DEBUG)
        # session = self.__get_session()
        # response = session.post(url=self.scrape_url,
        #                         json=self.__request_payload)
        locations = []
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
        }

        req = request.Request("https://www.walgreens.com/topic/v1/csrf", headers=headers)
        with request.urlopen(req) as response:
            raw_cookies = response.info().get_all("Set-Cookie")
            cookie_string = ""
            for cookie in raw_cookies:
                cookie_string += cookie + "; "
            headers.update({'cookie': cookie_string})
            resp = json.loads(response.read())
            headers.update({
                resp['csrfHeaderName']: resp['csrfToken'],
                'accept-language': 'en-US,en;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json; charset=UTF-8',
            })
        data = json.dumps(self.__request_payload).encode('utf8')
        headers.update({'Content-Length': len(data)})

        appts = request.Request(self.scrape_url, data=data, headers=headers)
        with request.urlopen(appts) as appt_response:
            response = json.loads(gzip.decompress(appt_response.read()))
            if response['appointmentsAvailable']:
                locations.append(Location(self.name,
                                          self.get_global_booking_link(),
                                          datetime.now(),
                                          [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations

    # def __get_session(self):
    #     s = Session()
    #     s.headers.update({"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
    #     csrf_response = s.get('https://www.walgreens.com/topic/v1/csrf')
    #     s.headers.update({
    #         'X-XSRF-TOKEN': csrf_response.json()['csrfToken'],
    #         'authority': 'www.walgreens.com',
    #         'dnt': '1',
    #         'accept-language': 'en-US,en;q=0.9',
    #         'accept-encoding': 'gzip, deflate, br',
    #         'origin': 'https://www.walgreens.com',
    #         'accept': 'application/json, text/plain, */*',
    #         'content-type': 'application/json; charset=UTF-8',
    #         'sec-fetch-site': 'same-origin',
    #         'sec-fetch-mode': 'cors',
    #         'sec-fetch-dest': 'empty',
    #         'referer': 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
    #     })
    #     return s
