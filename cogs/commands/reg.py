import re
import discord
import aiomcrcon
from discord.ext import commands
from discord import app_commands
from aiomcrcon import Client
from dateutil.parser import parse

from main import db, config

class Reg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="reg", description="Регистрация")
    @app_commands.default_permissions(permissions=0)
    async def reg_slash(self, interaction: discord.Interaction):
        if interaction.guild is None:
            guild = discord.utils.get(self.client.guilds, id=config.bot.guild)  # Получаем сервер по ID
            if guild:
                member = guild.get_member(interaction.user.id)  # Проверяем, является ли пользователь участником сервера
                if member:
                    role = discord.utils.get(member.roles, id=config.bot.white_list_role)
                    if role:
                        await self.reg(interaction)
                    else:
                        await interaction.response.send_message('У вас недостаточно прав для регистрации на сервере')
                else:
                    await interaction.response.send_message('Вы не являетесь участником сервера.')
            else:
                await interaction.response.send_message('Сервер не найден.')
        else:  # Если команда выполнена на сервере
            role = discord.utils.get(interaction.user.roles, id=config.bot.white_list_role)
            if role:
                await self.reg(interaction)
            else:
                await interaction.response.send_message('У вас недостаточно прав для регистрации на сервере')

    async def reg(self, interaction: discord.Interaction):
        if db.connect():
            r = db.getUsernameByDiscordID(interaction.user.id)
            if r[0] and r[1] is None:
                await interaction.response.send_modal(self.Registar())
            else:
                await interaction.response.send_message('Ты уже зарегистрирован')
            db.close()  # Закрываем соединение с базой данных после выполнения
        else:
            await interaction.response.send_message('Не удалось подключиться к базе данных, повторите попытку позже')

    class Registar(discord.ui.Modal, title="Регистрация нового аккаунта"):
        def __init__(self):
            super().__init__(timeout=None)

        login = discord.ui.TextInput(label="Игровой логин",placeholder="Логин", style=discord.TextStyle.short, required=True, min_length=4, max_length=16)
        password = discord.ui.TextInput(label="Уникальный пароль",placeholder="Пароль", style=discord.TextStyle.short, required=True, min_length=5, max_length=20)
        if config.bot.event_birthday==True:
            birthday = discord.ui.TextInput(label="Дата твоего рождения",placeholder="2015-12-31", style=discord.TextStyle.short, required=True, min_length=8, max_length=10)

        async def on_submit(self, interaction: discord.Interaction):
            if db.connect():
                try:
                    r = db.getUsernameByDiscordID(interaction.user.id)
                    login = self.login.value
                    password = self.password.value
                    if config.bot.event_birthday==True:
                        try:
                            birthday = parse(self.birthday.value)
                        except Exception:
                            await interaction.response.send_message('Вы указали дату не в том формате.')
                            return
                    else:
                        birthday = None
                    if re.fullmatch(r'[a-z0-9_-]{4,16}', login, re.IGNORECASE) == None:
                        await interaction.response.send_message('В вашем нике использует некорректные символы!')
                        return
                    r_reg = db.register(interaction.user.id, login, password, birthday)
                    if r_reg[0]:
                        embedVar = discord.Embed(title="Вы успешно зарегистрированы!", description="Вам предоставлен доступ на пробный период в 7 дней. Этого времени должно хватить, чтобы вы смогли составить мнение о проекте. По истечении срока мы предложим вам оформить подписку за символическую плату 100 рублей/месяц. Доступ по подписке помогает нам обеспечить адекватную аудиторию на сервере и больше времени уделять его развитию. Надеемся на ваше понимание и желаем вам приятной игры!", color=config.bot.embedColor)
                        embedVar.add_field(name="Ссылки на игровой клиент", value="Он необходим для входа на сервер", inline=False)
                        embedVar.add_field(name="Windows", value=f"[Скачать]({config.web.url_launcher_exe})", inline=True)
                        embedVar.add_field(name="Linux/MacOS", value=f"[Скачать]({config.web.url_launcher_jar})", inline=True)
                        await interaction.response.send_message(embed=embedVar)
                    elif (not r[0]) and (r[1] == '1062'):
                        await interaction.response.send_message('Ник или пароль уже занят')
                except Exception as ex:
                    print(ex)
                    await interaction.response.send_message(f'**Ошибка:** Неверный синтаксис\nПравильно: {config.bot.prefix}reg')
                finally:
                    db.close()


async def setup(client):
    await client.add_cog(Reg(client))
