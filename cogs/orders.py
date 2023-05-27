from nextcord.ext.commands import Cog
from nextcord import slash_command, Embed, Color, utils, Member, TextChannel, ui, ButtonStyle, CategoryChannel
from nextcord.ext.application_checks import has_permissions, ApplicationMissingPermissions

from bot import BotMarket
from typing import Union
from utils import Enums, CustomInteraction
from asyncio import sleep


class TicketCloseView(ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Zamknij Ticket", style=ButtonStyle.gray, custom_id="ticket-close", emoji="❌")
    async def close_ticket(self, button: ui.Button, interaction: CustomInteraction):
        await interaction.message.edit(view=None)

        embed = Embed(
            title=f"Zamykanie: 5s",
            colour=Color.red(),
        )
        embed.set_author(name=interaction.user, icon_url=interaction.avatars.get_user_avatar(interaction.user))
        message = await interaction.channel.send(embed=embed)

        for x in range(5, 0, -1):
            embed.title = f"Zamykanie: {x}s"
            await message.edit(embed=embed)
            await sleep(1)

        await interaction.channel.delete()


class TicketCreateView(ui.View):

    def __init__(self):
        super().__init__(timeout=None)

        self.category_id: int = Enums.tickets_category.value

    @ui.button(label="Stwórz zamówienie", style=ButtonStyle.green, custom_id="ticket-create", emoji="<a:greenbutton:919647666101694494>")
    async def create_ticket(self, button: ui.Button, interaction: CustomInteraction):
        category: CategoryChannel = interaction.guild.get_channel(self.category_id)
        if not category:
            return await interaction.send_error_message(description="Wygląda na to, że kategoria ticketów została usunięta. Skontaktuj się z administracją.", ephemeral=True)

        channel: TextChannel = await interaction.guild.create_text_channel(name=f"{interaction.user}-zamowienie", category=category)
        await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)

        await interaction.response.send_message(f"Stworzono nowe zamówienie: {channel.mention}", ephemeral=True)

        embed = Embed(
            title=f"Witaj {interaction.user}!",
            colour=Color.dark_theme(),
            timestamp=utils.utcnow(),
            description="**Na tym kanale możesz złożyć swoje zamówienie!**\n\nAdministracja już została poinformowana o twoim tickecie. Możesz wstępnie wypisać rzeczy, które chciałbyś/abyś mieć."
        )
        embed.set_author(name=interaction.user, icon_url=interaction.avatars.get_user_avatar(interaction.user))
        embed.set_thumbnail(url=interaction.avatars.get_guild_icon(interaction.guild))
        button = TicketCloseView()

        await channel.send(interaction.guild.default_role.mention, delete_after=1)
        await channel.send(embed=embed, view=button)


class orders(Cog):

    def __init__(self, bot: BotMarket) -> None:
        self.bot: BotMarket = bot
        self.bot.loop.create_task(self.update_views())

    async def update_views(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

        self.bot.add_view(TicketCloseView())
        self.bot.add_view(TicketCreateView())

    @slash_command(name="zamowienia", description="Tworzy system zamowień")
    @has_permissions(administrator=True)
    async def orders(self, interaction: CustomInteraction):
        embed = Embed(
            title="🔧 Składanie zamówień",
            color=Color.green(),
            timestamp=utils.utcnow(),
            description="`•` **Chciałbyś złożyć zamówienie lub zrobić wstępną wycene? Stwórz ticket poniższym przyciskiem.**"
        )
        embed.set_author(name=interaction.guild.me, icon_url=interaction.avatars.get_user_avatar(interaction.guild.me))
        embed.set_thumbnail(interaction.avatars.get_guild_icon(interaction.guild))

        button = TicketCreateView()
        await interaction.channel.send(embed=embed, view=button)
        await interaction.response.send_message("Stworzono zamowienia", ephemeral=True)

    @orders.error
    async def orders_error(self, interaction: CustomInteraction, error):
        if isinstance(error, ApplicationMissingPermissions):
            return await interaction.send_error_message(
                "**Niestety, ale nie posiadasz wymaganego uprawnienia: `Administrator`**")


def setup(bot: BotMarket):
    bot.add_cog(orders(bot))
