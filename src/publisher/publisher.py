from typing import List, Iterable

from scraper.models.Location import Location
from publisher.channel.DiscordPublisher import DiscordPublisher

publishers = [DiscordPublisher]


def publish(location: Location):
    publish_locations([location])


def publish_locations(locations: Iterable[Location]):
    filtered_locations = list(filter(lambda l: l.has_availability(), locations))
    for publisher in publishers:
        p = publisher()
        p.publish(filtered_locations)
