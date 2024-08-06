import discord
from discord.ext import commands, tasks
import minestat
from main import config

class Server(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update_status.start()

    @tasks.loop(minutes=1)
    async def update_status(self):
        try:
            mc = minestat.MineStat('65.108.18.29', 25622)
            if mc.online:
                if mc.current_players != 0:
                    await self.client.change_presence(
                        activity=discord.Game(f"PR: {mc.current_players}/{mc.max_players} игроков"), status=discord.Status.online)
                else:
                    await self.client.change_presence(
                        activity=discord.Game(f"PR: {mc.current_players}/{mc.max_players} игроков"), status=discord.Status.idle)
            else:
                await self.client.change_presence(
                    activity=discord.Game("PR: Сервер отключен"), status=discord.Status.dnd)
        except Exception as ex:
            print(f"Ошибка при обновлении статуса: {ex}")
async def setup(client):
    await client.add_cog(Server(client))
