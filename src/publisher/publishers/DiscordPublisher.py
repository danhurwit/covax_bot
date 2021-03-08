from typing import Iterable

from decouple import config
from discord import Webhook, RequestsWebhookAdapter

from models.publishers.Publisher import Publisher
from models.sources.AppointmentSource import AppointmentSource
from models.sources.Location import Location


class DiscordPublisher(Publisher):
    publish_url = config('DISCORD_WEBHOOK_URL')

    def publish(self, source: AppointmentSource, locations: Iterable[Location]):
        webhook = Webhook.from_url(self.publish_url, adapter=RequestsWebhookAdapter())
        for message in source.get_publish_messages(locations):
            webhook.send(message)
