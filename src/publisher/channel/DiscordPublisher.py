import os
from typing import List

from publisher.channel.Publisher import Publisher
from scraper.models.Location import Location

from discord import Webhook, RequestsWebhookAdapter
from decouple import config


class DiscordPublisher(Publisher):

    publish_url = config('DISCORD_WEBHOOK_URL')

    def publish(self, locations: List[Location]):
        for location in locations:
            webhook = Webhook.from_url(self.publish_url, adapter=RequestsWebhookAdapter())
            webhook.send(location.format_message())
