import discord
from discord.ext import commands
from cogs.commands.reg import Reg

from main import config


class Join_guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    class Batton(discord.ui.View):
        @discord.ui.button(label="Начать играть!", style=discord.ButtonStyle.primary, emoji="⚔️")
        async def ok(self, interaction: discord.Integration, button: discord.ui.Button):
            await interaction.response.send_modal(Reg.Registar())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(view=Join_guild.Batton(), content=f"Приветствую, {member.mention}! Я бот проекта Minecraft. Чтобы попасть на сервер - тебе необходимо зарегистрироваться. \n \n Напиши мне команду **/reg** и создай свой профиль в игре. Полный список моих команд ты можешь узнать, написав команду **/help**.")

        author = member
        guild = self.client.get_guild(config.bot.guild)
        role = guild.get_role(config.bot.member_role)
        await author.add_roles(role)


async def setup(client):
    await client.add_cog(Join_guild(client))