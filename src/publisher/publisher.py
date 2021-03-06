from typing import Iterable

from models.sources.Location import Location
from publisher.publishers.DiscordPublisher import DiscordPublisher

publishers = [DiscordPublisher]


def publish(location: Location):
    publish_locations([location])


def publish_locations(locations: Iterable[Location]):
    for publisher in publishers:
        p = publisher()
        p.publish(locations)
