import discord
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        po3 = discord.Game('The best game: project ozone 3')
        await self.bot.change_presence(status=discord.Status.idle, activity=po3)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.type == discord.ChannelType.private:
            print('oh wow, a dm!')


async def setup(bot):
    await bot.add_cog(events(bot))
