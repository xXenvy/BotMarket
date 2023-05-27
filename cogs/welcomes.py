from nextcord.ext.commands import Cog
from nextcord import slash_command, Embed, Color, utils, Member, TextChannel

from bot import BotMarket
from typing import Union
from utils import Enums


class welcomes(Cog):

    def __init__(self, bot: BotMarket) -> None:
        self.bot: BotMarket = bot
        self.welcomes_channel_id: int = Enums.welcomes_channel.value
        self.goodbyes_channel_id: int = Enums.goodbyes_channel.value

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel: TextChannel = member.guild.get_channel(self.welcomes_channel_id)
        rules: TextChannel = member.guild.get_channel(1111744046474473603)
        info: TextChannel = member.guild.get_channel(1111744375010115647)

        if not rules:
            rules = "#Deleted Channel"

        if not info:
            info = "#Deleted Channel"

        if not channel:
            return

        embed = Embed(
            title="Witamy na serwerze! :wave:",
            color=Color.dark_theme(),
            timestamp=utils.utcnow(),
            description=f"Witaj {member.mention}! Cieszymy się, że do nas dołączyłeś.\n"
                        f"Zapoznaj się z naszym regulaminem na kanale {rules.mention} i przeczytaj wszystike informacje {info.mention}"
        )
        await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel: TextChannel = member.guild.get_channel(self.goodbyes_channel_id)
        if not channel:
            return

        embed = Embed(
            title="Użytkownik opuścił serwer :wave:",
            color=Color.dark_theme(),
            timestamp=utils.utcnow(),
            description=f"Żegnaj {member.mention}! Mamy nadzieje, że jeszcze do nas wrócisz."
        )
        await channel.send(embed=embed)


def setup(bot: BotMarket):
    bot.add_cog(welcomes(bot))
