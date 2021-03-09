import copy
from typing import Iterable

from decouple import config
from discord_webhook import DiscordWebhook, DiscordEmbed

from models.publishers.Publisher import Publisher
from models.sources.AppointmentSource import AppointmentSource
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class DiscordPublisher(Publisher):
    __publish_url = config('DISCORD_WEBHOOK_URL')
    __MAX_WINDOWS_PER_EMBED = 7

    def publish(self, source: AppointmentSource, locations: Iterable[Location]):
        webhook = DiscordWebhook(self.__publish_url)
        base_embed = self.__get_embed_header(source.get_name(), source.get_display_props())
        if not source.has_location_based_booking():
            #  else, add booking link from the location
            base_embed.add_embed_field(name="Booking Link:", value=source.get_global_booking_link(), inline=False)

        if source.has_time_based_availability():
            #  If location has availability by day, one location per embed
            for location in locations:
                webhook.add_embed(self.__build_embed_for_location(location, copy.deepcopy(base_embed)))
        else:
            #  concatenate the locations onto one embed.
            webhook.add_embed(self.__get_concatenated_locations(locations, copy.deepcopy(base_embed)))
        webhook.execute()

    def __get_concatenated_locations(self, locations, embed) -> DiscordEmbed:
        embed.add_embed_field(name="Locations:",
                              value="\n".join([l.get_name() for l in locations]),
                              inline=False)
        return embed

    def __build_embed_for_location(self, location: Location, embed: DiscordEmbed) -> DiscordEmbed:
        if len(list(location.get_availability_windows())) > 7:  # Discord has a limit of 25 fields per message
            return self.__get_location_and_availability(embed, location, location.get_availability_windows())
        else:
            windows = list(location.get_availability_windows())
            for window_chunk in [windows[i:i + self.__MAX_WINDOWS_PER_EMBED] for i in
                                 range(0, len(windows), self.__MAX_WINDOWS_PER_EMBED)]:
                return self.__get_location_and_availability(embed, location, window_chunk)

    def __get_embed_header(self, source_name, display_props: DisplayProperties):
        embed = DiscordEmbed(title='Appointments now available!',
                             description=source_name + ' has added new appointments',
                             color=display_props.get_theme_color())
        embed.set_thumbnail(url=display_props.get_logo_url())
        embed.set_timestamp()
        return embed

    def __get_location_and_availability(self, embed, location, windows):
        embed.add_embed_field(name="Location:", value=location.get_name(), inline=False)
        embed.add_embed_field(name="Booking Link:", value=location.get_link(), inline=False)
        for window in windows:
            embed.add_embed_field(name="Date", value=window.get_date().strftime("%m-%d-%Y"), inline=True)
            embed.add_embed_field(name="Available", value=window.get_num_available(), inline=True)
            embed.add_embed_field(name=".", value=".", inline=True)
        return embed
