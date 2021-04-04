import json
import uuid
from datetime import datetime
from pprint import pprint

from requests import Session

from data import sessions_dao
from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location
from models.sources.SessionState import SessionState


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
    __s = Session()

    def scrape_locations(self):
        self.__add_inititial_headers()
        session = sessions_dao.get_current_session(self.name)
        if session:
            self.__s.cookies.update({json.loads(session['cookies'])})
            session_id = session['id']
            state = self.__get_current_state()
        else:
            state = self.__get_current_state()
            session_id = str(uuid.uuid4())
            sessions_dao.create_session(self.name, session_id, state, json.dumps(self.__s.cookies.get_dict()))
            if state == SessionState.ENQUEUED:
                #  TODO Enqueue myself
                #  get https: // reportsonline.queue - it.net /?c = reportsonline & e = hannafordcovid19 & ver = v3 - aspnet - 3.6
                # .2 & cver = 54 & man = Hannaford

                #  post https: // reportsonline.queue - it.net / spa - api / queue / reportsonline / hannafordcovid19 / enqueue?cid = en - US
                sessions_dao.insert_cookies(self.name, session_id, json.dumps(self.__s.cookies.get_dict()))

        if state == SessionState.CLOSED:
            sessions_dao.update_queue_status(self.name, session_id, SessionState.CLOSED)
            self.locations = []
        elif state == SessionState.ENQUEUED:
            sessions_dao.update_queue_status(self.name, session_id, SessionState.ENQUEUED)
            self.locations = []
            self.should_update_availability = False
        elif state == SessionState.ACCEPTED:
            sessions_dao.update_queue_status(self.name, session_id, SessionState.ENQUEUED)
            locations = self.check_for_appointements()
            self.locations = locations
        else:
            self.locations = []

    def check_for_appointements(self):
        self.__get_cookies()
        availability = False
        for zip_code in self.__zip_codes:
            payload = self.__payload.copy()
            payload['zip'] = zip_code
            response = self.__s.post(self.scrape_url, data=payload)
            if "There are no locations with available appointments" not in response.text and response.text != '""':
                pprint(self.__payload)
                pprint(response.text)
                availability = True
        locations = []
        if availability:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        return locations

    def __add_inititial_headers(self):
        self.__s.headers.update({
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        })

    def __get_current_state(self):
        r = self.__s.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory")
        if 'You are now in line' in r.text:
            return SessionState.ENQUEUED
        elif 'Set Location' in r.text:
            return SessionState.ACCEPTED
        else:
            return SessionState.CLOSED

    def __get_cookies(self):
        r = self.__s.get(
            "https://reportsonline.queue-it.net/?c=reportsonline&e=stopandshopcovid19&ver=v3-aspnet-3.6.2&cver=52&man=Stop%20%26%20Shop")
        token = self.__s.cookies.get("Queue-it-token-v3")
        self.__s.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory?queueittoken=" + token)
        self.__s.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19")
