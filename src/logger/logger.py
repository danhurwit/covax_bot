from decouple import config
from discord import Webhook, RequestsWebhookAdapter


def log(message: str):
    log_url = config('LOGGER_URL')
    webhook = Webhook.from_url(log_url, adapter=RequestsWebhookAdapter())
    webhook.send(message)
