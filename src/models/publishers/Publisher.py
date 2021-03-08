from typing import List

from models.sources.AppointmentSource import AppointmentSource
from models.sources.Location import Location


class Publisher:
    def publish(self, source: AppointmentSource,  locations: List[Location]):
        pass
