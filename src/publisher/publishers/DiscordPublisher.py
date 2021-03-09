from typing import Iterable

from decouple import config
from discord_webhook import DiscordWebhook, DiscordEmbed

from models.publishers.Publisher import Publisher
from models.sources.AppointmentSource import AppointmentSource
from models.sources.Location import Location
from scraper.sources.Cvs import BOOKING_URL as CVS_BOOKING_URL
from scraper.sources.Cvs import CVS_NAME
from scraper.sources.MassVax import MASSVAX_NAME


class DiscordPublisher(Publisher):
    publish_url = config('DISCORD_WEBHOOK_URL')
    __MAX_WINDOWS_PER_EMBED = 7

    def publish(self, source: AppointmentSource, locations: Iterable[Location]):
        webhook = DiscordWebhook(self.publish_url)
        if source.get_name() == MASSVAX_NAME:
            for location in locations:
                if len(list(location.get_availability_windows())) > 7:  # Discord has a limit of 25 fields per message
                    webhook.add_embed(self.__get_massvax_embed(location, location.get_availability_windows()))
                else:
                    windows = list(location.get_availability_windows())
                    for window_chunk in [windows[i:i + self.__MAX_WINDOWS_PER_EMBED] for i in
                                         range(0, len(windows), self.__MAX_WINDOWS_PER_EMBED)]:
                        webhook.add_embed(self.__get_massvax_embed(location, window_chunk))
        elif source.get_name() == CVS_NAME:
            embed = self.__get_cvs_embed(locations)
            webhook.add_embed(embed)
        webhook.execute()

    def __get_cvs_embed(self, locations):
        embed = DiscordEmbed(title='Appointments now available!',
                             description='CVS has added new appointments',
                             color='03b2f8')
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/CVS_Health_Logo.svg/2560px-CVS_Health_Logo.svg.png")
        embed.add_embed_field(name="Booking Link:", value=CVS_BOOKING_URL, inline=False)
        embed.add_embed_field(name="Sites:", value="\n".join([l.get_name() for l in locations]), inline=False)
        embed.set_timestamp()
        return embed

    def __get_massvax_embed(self, location, windows):
        embed = DiscordEmbed(title='Appointments now available!',
                             description='MassVax has added new appointments',
                             color='03b2f8')
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Seal_of_Massachusetts.svg/1200px-Seal_of_Massachusetts.svg.png")
        embed.add_embed_field(name="Site:", value=location.get_name(), inline=False)
        embed.add_embed_field(name="Booking Link:", value=location.get_link(), inline=False)
        for window in windows:
            embed.add_embed_field(name="Date", value=window.get_date().strftime("%d-%m-%Y"), inline=True)
            embed.add_embed_field(name="Available", value=window.get_num_available(), inline=True)
            embed.add_embed_field(name=".", value=".", inline=True)
        embed.set_timestamp()
        return embed
