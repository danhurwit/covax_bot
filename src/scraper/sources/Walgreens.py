import json
import logging
import ssl
from datetime import datetime
from pprint import pprint

import curlify
import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Walgreens(AppointmentSource):
    name = "Walgreens"
    scrape_url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability'
    __request_payload = {"serviceId": "99",
                         "position": {"latitude": 42.36475590000001, "longitude": -71.1032591},
                         "appointmentAvailability": {"startDateTime": "2021-03-27"},
                         "radius": 25}
    global_booking_link = 'https://www.walgreens.com/topic/promotion/covid-vaccine.jsp'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        logging.basicConfig(level=logging.DEBUG)
        session = self.__get_session()
        # response = session.post(url=self.scrape_url,
        #                         data=json.dumps(self.__request_payload),
        #                         allow_redirects=False)


        cookies = {
            'XSRF-TOKEN': 'mLPlGqdl2Ka3UQ==.OKvY6nS5cZP8KWlZRQTsY/dm4AzWL2YmBq9LzGq2Ft4=',
            '_abck': 'B56B2D2EA9577E27D81D5B68ED2B1BF3~-1~YAAQNXEmF/2VEUZ4AQAAABgldAWfEpnzkAuxVWjZcclo+ShqZg85qiT3EQI/3DAFRMf0GWxKQjsz2V/QaTyffaAN+fKqyfFoJ5GUJP5AEWrT8aRWQZLFt4F9yt7GPapw+x3HhFNCTZ+XSbgunXnL3aGR15hI/lJN5DTsdP582B/GR71NeAyMZp19ahmCieU9NqkwsNcX0gVVVvBJZ7P1Z/skxldDiLjEbbdFh6tdrBz+jqrmorsl+Rzgz3u85Rf+gNVe7ZPzzosZb97sGNQv1YDXYz78GUMUggKCKRTJoAaQn0LTIu2YRPL8hpOKAyYTOaGJHammUv/s4USoieIgJ3MhAVNBaD9PQFSw8yQsrRqTCvgtq5eeJltqqAHuTZw=~-1~-1~-1',
            'ak_bmsc': '99DB1C4DE262FB8EBA0083100D4C895817267135520C0000E3445F60A937AB0A~plCjelnvfR1u46OtZKa/C4LBpptLoeHORv/CDboqht3F6bl2TGyaGo0DEWMqDKnvNid4QR1FA1Nka+ck5SPdTL5OJJ6RzkrlO9oPKoITYAfJ1FUU/5Z2eg3z4hS1MwPzFCCTv+O7KUfsWZ4yIe7WNguL74iaGGgI3WWQdbtFFwRTtFeZnZBNgeBhucfoonTt1VPYFEhDWW9sRQn/UUU56qcI/W1ctp9eb4WAY0WDlQmUo=',
            'bm_sz': '2A32375805D37956BBE368872365BCE7~YAAQNXEmF/yVEUZ4AQAAABgldAsJfH+qtGDWEk9ycAEPL7axU7KHcfEOUwG5IIIx6Ite69l5lNW/OyLeLbkpRv9jxD1l4CTV5zLe21Ndbt0tdpSk0BjtOPlN/qsDfT1b8eLn6MV19y0bI3juaEa3Y3kYwIa/MsSyyr1Q0yIRr9LOTYxStC7Ky08NPjNZVlg6sFwI',
            'dtCookie': '2$D5027085D938459CCCB323A00F0CFB94|0eed2717dafcc06d|1',
            'akavpau_walgreens': '1616856591~id=00fcbbbe3a098187ab6472c3998ca9c3',
        }

        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '164',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
            'X-XSRF-TOKEN': 'U7TlRSD47LwyGQ==.XSXN56d3n8hUQI6zfnQ52IaplTGBEZNqFRBO1zw83UA=',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'authority': 'www.walgreens.com',
            'content-type': 'application/json; charset=UTF-8',
        }

        data = '{"serviceId": "99", "position": {"latitude": 42.36475590000001, "longitude": -71.1032591}, "appointmentAvailability": {"startDateTime": "2021-03-27"}, "radius": 25}'

        response = requests.post('https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability',
                                 headers=headers, cookies=cookies, data=data)
        locations = []
        if response.json()['appointmentsAvailable']:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations

    def __get_session(self):
        s = Session()
        s.headers.update({"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
        csrf_response = s.get('https://www.walgreens.com/topic/v1/csrf')
        s.headers.update({
            'X-XSRF-TOKEN': csrf_response.json()['csrfToken'],
            'authority': 'www.walgreens.com',
            'accept-language': 'en-US,en;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json; charset=UTF-8',
            'Connection': 'keep-alive'
        })
        return s
