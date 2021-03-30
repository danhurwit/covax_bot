from datetime import datetime
from pprint import pprint

from requests import Session

from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Hannafords(AppointmentSource):
    name = "Hannafords"
    scrape_url = "https://hannafordsched.rxtouch.com/rbssched/program/covid19/Patient/CheckZipCode"
    __payload = {'zip': '02139', 'appointmentType': '5954', 'PatientInterfaceMode': '0'}
    global_booking_link = "https://hannafordsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory"
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Hannaford_logo.svg/1920px-Hannaford_logo.svg.png",
        "9370DB"
    )

    def scrape_locations(self):
        session = self.__get_session()
        response = session.post(self.scrape_url, data=self.__payload)
        locations = []
        if "There are no locations with available appointments" not in response.text and response.text != '""':
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
        s.get("https://hannafordsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory")
        r = s.get(
            "https://reportsonline.queue-it.net/?c=reportsonline&e=hannafordcovid19&ver=v3-aspnet-3.6.2&cver=52&man=Hannaford")
        token = s.cookies.get("Queue-it-token-v3")
        s.get("https://hannafordsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory?queueittoken=" + token)
        s.get("https://hannafordsched.rxtouch.com/rbssched/program/covid19")
        return s
