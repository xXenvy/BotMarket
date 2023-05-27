from __future__ import annotations

from typing import Union, TYPE_CHECKING
from nextcord import Intents, Interaction, Embed, Color, utils, Guild, Member

from enum import Enum
from os import listdir

if TYPE_CHECKING:
    from bot import BotMarket


class BotUtils:

    def __init__(self):
        pass

    @staticmethod
    def load_cogs(bot: BotMarket):
        bot.load_extension("onami")
        for file in listdir("cogs"):
            if file.endswith(".py"):
                bot.load_extension(f"cogs.{file[:-3]}")
                print(f"Extension {file} loaded")

    @property
    def settings(self) -> dict:
        options: dict[str, Union[str, None, Intents]] = {
            "command_prefix": "b!",
            "help_command": None,
            "intents": Intents.all()
        }

        return options

    @property
    def bot_token(self) -> str:
        return "MTExMTcxMzI3NDEyODUxMTEyNw.Gc-azU.H92xpaZPw1mRVFlmMQS0ggfXdTUQUwUOckp-6Q"


class Avatars:

    @staticmethod
    def get_user_avatar(user: Member) -> str:
        try:
            avatar = user.avatar.url
        except AttributeError:
            avatar = user.default_avatar.url
        return avatar

    @staticmethod
    def get_guild_icon(guild: Guild) -> str:
        try:
            icon = guild.icon.url
        except AttributeError:
            icon = "https://www.howtogeek.com/wp-content/uploads/2021/07/Discord-Logo-Lede.png?height=200p&trim=2,2,2,2"
        return icon


class CustomInteraction(Interaction):

    def __new__(cls, data, state):
        custom_interaction = super().__new__(cls)

        return custom_interaction

    def __init__(self, *, data, state):
        self.avatars = Avatars
        super().__init__(data=data, state=state)

    @property
    def bot(self):
        return self.client

    def get_bot_latency(self) -> int:
        latecy: int = round(self.client * 1000)

        return latecy

    async def send_error_message(self, description: str, defer: bool = False, ephemeral: bool = False) -> None:
        embed = Embed(
            title="<:error:919648598713573417> Wystąpił błąd.",
            color=Color.red(),
            timestamp=utils.utcnow(),
            description=description
        )
        embed.set_author(name=self.user, icon_url=self.avatars.get_user_avatar(self.user))
        embed.set_thumbnail(url=self.avatars.get_guild_icon(self.guild))

        if defer:
            await self.followup.send(embed=embed, ephemeral=ephemeral)
        else:
            await self.response.send_message(embed=embed, ephemeral=ephemeral)


class Enums(Enum):
    verify_role: int = 1111703944192851974

    stats_channels: dict[str, int] = {"members": 1111745024250617918,
                                      "bans": 1111745059696689242,
                                      "date": 1111745099228004462}

    welcomes_channel: int = 1111744038886981743
    goodbyes_channel: int = 1111744040954761338

    tickets_category: int = 1112063264084459560


bot_utils = BotUtils()
