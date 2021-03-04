from typing import List

from publisher.channel.Publisher import Publisher
from scraper.models.Location import Location

from discord import Webhook, RequestsWebhookAdapter


DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/817171915331862588/pZ2gbKgfRfdTI_IdPNtu-uBezD4w2u6VjA59govva8AM3PYJFOm_TwZsP4MAbj171PUL'


class DiscordPublisher(Publisher):

    def publish(self, locations: List[Location]):
        for location in locations:
            webhook = Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
            webhook.send(location.format_message())
