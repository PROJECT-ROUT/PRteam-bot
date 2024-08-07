import discord
from discord.ext import commands, tasks
from main import config

class Members(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.change_channel_name.start()

    @tasks.loop(hours=1)
    async def change_channel_name(self):
        guild = self.client.get_guild(config.bot.guild)
        channel = self.client.get_channel(config.bot.members_vc)
        if channel and guild:
            member_count = guild.member_count
            new_name = f"Участники: {member_count}"
            await channel.edit(name=new_name)
        else:
            print(f'Канал с ID {config.bot.members_vc} или Guild ID {config.bot.guild} не найдены')

async def setup(client):
    await client.add_cog(Members(client))
