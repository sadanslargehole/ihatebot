import discord
from asyncio import sleep
from discord.ext import commands
from sys import exit
from time import localtime, strftime
import requests as r
from os import system as sys
t = localtime()
clock = strftime('%m/%d %H:%M', t)


class Utilcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='exit')
    async def exit(self, ctx, *args):
        msg = ' '.join(args)
        if ctx.channel.type is not discord.ChannelType.private:
            await ctx.message.delete()
        exit(f'{ctx.author} exited on {clock} with message:\n{msg}')

    @commands.command(name='ip')
    @commands.is_owner()
    async def get_ip_addr(self, ctx):
        ip = r.get('http://checkip.amazonaws.com')
        await ctx.author.send(ip.text)
        if ctx.channel.type is not discord.ChannelType.private:
            await ctx.send(f"Check DM's {ctx.author.mention}")

    @commands.command(aliases=["bash", 'sh'])
    async def cmd(self, ctx, *, args: str):
        if ctx.author.id == self.bot.config['owner']:
            await ctx.send(f'it workjed{ctx.author.id} ', delete_after=5)
        else:
            await ctx.message.add_reaction('❌')
            await ctx.send(f'{ctx.author.mention} you do not have permession to do this', delete_after=5)
            await ctx.message.delete(delay=5)


async def setup(bot):
    await bot.add_cog(Utilcmds(bot))
