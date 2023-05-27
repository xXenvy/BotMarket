from nextcord.ext.commands import Cog
from nextcord import slash_command, Embed, Color, utils, ui, ButtonStyle, Role
from nextcord.ext.application_checks import has_permissions, ApplicationMissingPermissions

from bot import BotMarket
from utils import CustomInteraction, Enums


class VerifyButton(ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.role_id: int = Enums.verify_role.value

    @ui.button(label="Zweryfikuj", style=ButtonStyle.green, emoji="✅", row=1, custom_id="verify")
    async def verify(self, button: ui.Button, interaction: CustomInteraction) -> None:
        role: Role = interaction.guild.get_role(self.role_id)
        if not role:
            return await interaction.send_error_message(
                "Wystąpił błąd z rolą weryfikacji. Skontakuj się z administracją, aby to rozwiązać.",
                ephemeral=True)

        await interaction.user.add_roles(role)

        embed = Embed(
            title="Pomyślnie zweryfikowano <a:greenbutton:919647666101694494>",
            colour=Color.green(),
            timestamp=utils.utcnow(),
            description="Weryfikacja przebiegła pomyślnie."
        )
        embed.set_author(name=interaction.user, icon_url=interaction.avatars.get_user_avatar(interaction.user))
        embed.set_thumbnail(url=interaction.avatars.get_guild_icon(interaction.guild))
        await interaction.response.send_message(embed=embed, ephemeral=True)


class settings(Cog):

    def __init__(self, bot: BotMarket) -> None:
        self.bot: BotMarket = bot
        self.bot.loop.create_task(self.update_views())

    async def update_views(self):
        self.bot.add_view(VerifyButton())

    @slash_command(name="weryfikacja", description="Tworzy weryfikacje")
    @has_permissions(administrator=True)
    async def verify(self, interaction: CustomInteraction):
        embed = Embed(
            title="<a:success:984490514332139600> Weryfikacja",
            colour=Color.green(),
            timestamp=utils.utcnow(),
            description="> Naciśnij poniższy przycisk, aby się zweryfikować."
        )
        embed.set_author(name=interaction.guild.me, icon_url=interaction.avatars.get_user_avatar(interaction.guild.me))
        embed.set_thumbnail(url=interaction.avatars.get_guild_icon(interaction.guild))

        view = VerifyButton()
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Utwrzono weryfikacje!", ephemeral=True)

    @verify.error
    async def verify_error(self, interaction: CustomInteraction, error):
        if isinstance(error, ApplicationMissingPermissions):
            return await interaction.send_error_message("**Niestety, ale nie posiadasz wymaganego uprawnienia: `Administrator`**")


def setup(bot: BotMarket):
    bot.add_cog(settings(bot))
