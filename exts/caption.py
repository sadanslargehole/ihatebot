import discord
from discord.ext import commands
import ffmpeg


class caption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases=['cpt'])
    async def caption(self,ctx, caption:str ):
        for i in ctx.message.attachments:
            print(i.content_type)
        if len(ctx.message.attachments) != 1:
            await ctx.send(f'{ctx.author.mention} invalid images\n please provide 1 image to caption', delete_after=3)
        filenametmp = ctx.message.attachments[0].filename
        await ctx.message.attachments[0].save(f'./images/{filenametmp}')
        await ctx.send()

async def setup(bot):
    await bot.add_cog(caption(bot))
