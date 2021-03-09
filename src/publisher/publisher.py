import traceback
from typing import Iterable

from logger import logger
from models.sources.AppointmentSource import AppointmentSource
from models.sources.Location import Location
from publisher.publishers.DiscordPublisher import DiscordPublisher

publishers = [DiscordPublisher]


def publish(location: Location):
    publish_locations([location])


def publish_locations(source: AppointmentSource, locations: Iterable[Location]):
    for publisher in publishers:
        try:
            p = publisher()
            p.publish(source, locations)
        except:
            logger.log(traceback.format_exc())
