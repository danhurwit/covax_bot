from datetime import datetime
from pprint import pprint

from requests import Session

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class StopShop(AppointmentSource):
    name = "Stop & Shop"
    scrape_url = "https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/CheckZipCode"
    __payload = {'zip': '02139', 'appointmentType': '5957', 'PatientInterfaceMode': '0'}
    __zip_codes = ['02139', '02155', '01904', '01801']
    global_booking_link = "https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory"
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/9/97/Stop-and-shop-new-logo-2018.png",
        "DB7093"
    )

    def scrape_locations(self):
        session = self.__get_session()
        availability = False
        for zip_code in self.__zip_codes:
            payload = self.__payload.copy()
            payload['zip'] = zip_code
            response = session.post(self.scrape_url, data=payload)
            if "There are no locations with available appointments" not in response.text:
                pprint(self.__payload)
                pprint(response.text)
                availability = True

        locations = []
        if availability:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        self.locations = locations

    def __get_session(self):
        s = Session()
        s.headers.update({
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        })
        s.get(" https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory")
        r = s.get(
            "https://reportsonline.queue-it.net/?c=reportsonline&e=stopandshopcovid19&ver=v3-aspnet-3.6.2&cver=52&man=Stop%20%26%20Shop")
        token = s.cookies.get("Queue-it-token-v3")
        s.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory?queueittoken=" + token)
        s.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19")
        return s
