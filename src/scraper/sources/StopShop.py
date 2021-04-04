import json
import uuid
from datetime import datetime

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

    def scrape_locations(self):
        session = Session()
        self.__add_inititial_headers(session)
        existing_session = sessions_dao.get_current_session(self.name)
        if existing_session:
            session_id, state = self.__load_session(existing_session, session)
        else:
            session_id, state = self.__create_new_session(session)

        if state == SessionState.CLOSED:
            sessions_dao.update_queue_status(self.name, session_id, SessionState.CLOSED)
            self.locations = []
        elif state == SessionState.ENQUEUED:
            sessions_dao.update_queue_status(self.name, session_id, SessionState.ENQUEUED)
            self.locations = []
            self.should_update_availability = False
        elif state == SessionState.ACCEPTED:
            sessions_dao.update_queue_status(self.name, session_id, SessionState.ENQUEUED)
            locations, state = self._check_for_appointements(session)
            if state == SessionState.CLOSED:
                self.should_update_availability = False
                sessions_dao.update_queue_status(self.name, session_id, SessionState.CLOSED)
            self.locations = locations
        else:
            self.locations = []

    def __load_session(self, existing_session, session):
        session.cookies.update(json.loads(existing_session['cookies']))
        session_id = existing_session['id']
        state = self.__get_current_state(session)
        return session_id, state

    def __create_new_session(self, session):
        self.__get_cookies(session)
        state = self.__get_current_state(session)
        session_id = str(uuid.uuid4())
        sessions_dao.create_session(self.name, session_id, state, json.dumps(session.cookies.get_dict()))
        if state == SessionState.ENQUEUED:
            #  TODO Enqueue myself
            #  get https: // reportsonline.queue - it.net /?c = reportsonline & e = hannafordcovid19 & ver = v3 - aspnet - 3.6
            # .2 & cver = 54 & man = Hannaford

            #  post https: // reportsonline.queue - it.net / spa - api / queue / reportsonline / hannafordcovid19 / enqueue?cid = en - US
            sessions_dao.insert_cookies(self.name, session_id, json.dumps(self.__s.cookies.get_dict()))
        return session_id, state

    def _check_for_appointements(self, session):
        availability = False
        for zip_code in self.__zip_codes:
            payload = self.__payload.copy()
            payload['zip'] = zip_code
            response = session.post(self.scrape_url, data=payload)
            if response.text == '"loggedout"':
                return [], SessionState.CLOSED
            elif "There are no locations with available appointments" not in response.text and response.text != '""':
                availability = True
        locations = []
        if availability:
            locations.append(Location(self.name,
                                      self.get_global_booking_link(),
                                      datetime.now(),
                                      [AvailabilityWindow(1, datetime.now())]))
        return locations, SessionState.ACCEPTED

    def __add_inititial_headers(self, session):
        session.headers.update({
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        })

    def __get_current_state(self, session):
        r = session.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory")
        if 'You are now in line' in r.text:
            return SessionState.ENQUEUED
        elif 'Set Location' in r.text:
            return SessionState.ACCEPTED
        else:
            return SessionState.CLOSED

    def __get_cookies(self, session):
        r = session.get(
            "https://reportsonline.queue-it.net/?c=reportsonline&e=stopandshopcovid19&ver=v3-aspnet-3.6.2&cver=52&man=Stop%20%26%20Shop")
        token = session.cookies.get("Queue-it-token-v3")
        session.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory?queueittoken=" + token)
        session.get("https://stopandshopsched.rxtouch.com/rbssched/program/covid19")
