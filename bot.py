from nextcord.ext.commands import Bot as DiscordBot
from nextcord import Interaction, Status, Game

from typing import Any
from utils import bot_utils, CustomInteraction


class BotMarket(DiscordBot):

    def __init__(self, **kwargs: Any) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It allows you to set up your object, by giving it initial values for its attributes.
        The __init__ function can take any number of arguments, but self must be the first argument in every method definition.

        :param self: Refer to the object itself
        :param **kwargs: Any: Pass in any additional parameters that may be required by the bot
        :return: None
        """

        super().__init__(**kwargs)
        bot_utils.load_cogs(bot=self)

    async def on_ready(self) -> None:
        """
        The on_ready function is called when the bot has finished logging in and setting up its connection to Discord.
        It's a good place to print some info, or change the bot's presence.

        :param self: Refer to the current object
        :return: None
        """

        await self.change_presence(activity=Game("Służe pomocą!"), status=Status.idle)
        print("Bot is now ready!")

    def get_interaction(self, data, *, cls=Interaction) -> object:
        """
        The get_interaction function is a method of the InteractionManager class.
        It takes in data, which is a dictionary containing information about an interaction, and returns an object of type Interaction.
        The get_interaction function can be overridden to return objects of other types.

        :param self: Refer to the current instance of a class
        :param data: Pass the data from the client to the server
        :param *: Make sure that the only parameter passed in is data
        :param cls: Specify the class of the object to be returned
        :return: An instance of the interaction class
        """

        return super().get_interaction(data, cls=CustomInteraction)


if __name__ == "__main__":
    bot = BotMarket(**bot_utils.settings)
    bot.run(bot_utils.bot_token)
