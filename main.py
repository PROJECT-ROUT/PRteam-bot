import discord
from discord.ext import commands
import signal
import aiofiles.os
import sys
import multiprocessing
from dynaconf import Dynaconf

import dbmanager


config = Dynaconf(settings_files='conf/settings.yaml',apply_default_on_none=True, secrets='.secrets.yaml')
shop = Dynaconf(settings_files='conf/shop.yaml', apply_default_on_none=True, secrets='.secrets.yaml')
client = commands.Bot(command_prefix=config.bot.prefix, intents=discord.Intents.all(), help_command=None)
db = dbmanager.dbm(config.db.login, config.db.password, config.db.host, config.db.database)


@client.event
async def on_ready():
    try:
        print("\n"
              " ___ ___   _____ ___   _   __  __ \n"
              "| _ \ _ \ |_   _| __| /_\ |  \/  |\n"
              "|  _/   /   | | | _| / _ \| |\/| |\n"
              "|_| |_|_\   |_| |___/_/ \_\_|  |_|\n")

        print()
        print(" - Информация о боте - ")
        print("Имя бота: {0.user}".format(client))
        print(f"ID бота: {client.user.id}")
        print(f"Пинг во время запуска: {round(client.latency * 1000)} мс")

        #Загрузка папки cogs
        for dir_cogs in await aiofiles.os.listdir('./cogs'):
            for filename in await aiofiles.os.listdir(f'./cogs/{dir_cogs}'):
                if filename != '__pycache__':
                    if filename.endswith('.py') and filename != '__pycache__':
                        await client.load_extension(f'cogs.{dir_cogs}.{filename[:-3]}')
                    else:
                        print(f'Не является Cogs {filename}')
        #Удаление всех команд из подсказок в Discord
        #client.tree.clear_commands(guild=None)
        for Directory in [config.web.skindir, config.web.capedir, config.web.avatardir]:
            if not await aiofiles.os.path.exists(Directory):
                await aiofiles.os.mkdir(Directory)
        print(f"Команд найдено: {len(await client.tree.sync())}")
    except Exception as ex:
        print(ex)



def signal_handler(signal, frame):
    print('\nStopping!')
    scs_thread.terminate()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    from scstorage import API
    scs_thread = multiprocessing.Process(target=API.server)
    scs_thread.start()
    client.run(config.bot.token)