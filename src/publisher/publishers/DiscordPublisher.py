from typing import Iterable

from decouple import config
from discord import Webhook, RequestsWebhookAdapter

from models.publishers.Publisher import Publisher
from models.sources.Location import Location


class DiscordPublisher(Publisher):

    publish_url = config('DISCORD_WEBHOOK_URL')

    def publish(self, locations: Iterable[Location]):
        for location in locations:
            webhook = Webhook.from_url(self.publish_url, adapter=RequestsWebhookAdapter())
            webhook.send(location.format_message())
