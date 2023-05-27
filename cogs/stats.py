from nextcord.ext.commands import Cog
from nextcord import slash_command, Embed, Color, utils, ui, ButtonStyle, Role, VoiceChannel, Guild
from nextcord.ext.application_checks import has_permissions, ApplicationMissingPermissions
from nextcord.ext import tasks

from bot import BotMarket
from typing import Optional
from utils import Enums


class stats(Cog):

    def __init__(self, bot: BotMarket) -> None:
        self.bot: BotMarket = bot
        self.bot.loop.create_task(self.run_stats())

    async def run_stats(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

        self.update_stats.start()

    @tasks.loop(minutes=5)
    async def update_stats(self):
        guild: Guild = self.bot.get_guild(1111448389314416740)
        channels: dict[str, int] = Enums.stats_channels.value

        for keyword, channel_id in channels.items():
            channel: Optional[VoiceChannel] = guild.get_channel(channel_id)
            if not channel:
                continue
            if keyword == "members":
                channel_name: str = "📊︴𝖮𝗌𝗈𝖻𝗒: {}".format(guild.member_count)
            elif keyword == "bans":
                bans = await guild.bans().flatten()
                channel_name: str = "❌︴𝖡𝖺𝗇𝗒: {}".format(len(bans))
            elif keyword == "date":
                channel_name: str = "📅︴𝖣𝖺𝗍𝖺: {}".format(str(utils.utcnow())[0:10])

            await channel.edit(name=channel_name)


def setup(bot: BotMarket):
    bot.add_cog(stats(bot))
