from typing import List

from scraper.models.Location import Location
from publisher.channel.DiscordPublisher import DiscordPublisher

publishers = [DiscordPublisher]


def publish(locations: List[Location]):
    filtered_locations = list(filter(lambda l: l.has_availability(), locations))
    for publisher in publishers:
        p = publisher()
        p.publish(filtered_locations)
