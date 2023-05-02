import discord
from discord.ext import commands
import ffmpeg
import traceback
from math import ceil, floor
from os import system

class caption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cpt'])
    async def caption(self, ctx, *, caption: str):
        for i in ctx.message.attachments:
            print(i.content_type)
        if len(ctx.message.attachments) != 1:
            await ctx.send(f'{ctx.author.mention} invalid images\n please provide 1 image to caption', delete_after=3)
        filenametmp = ctx.message.attachments[0].filename
        await ctx.message.attachments[0].save(f'./images/{filenametmp}')
        # use a to see if there was an error
        a = await self.gen_text(caption, filenametmp, ctx)
        if a == 0:
            file = discord.File(f'./text/{filenametmp}')
            await ctx.send(file=file)
            a = await self.merge_images(filenametmp, ctx)
        if a == 0:
            file = discord.File(f'./final/{filenametmp}')
            await ctx.send(file=file)

    async def merge_images(self, filename: str, ctx):
        try:
            system(
                f'ffmpeg -y -i ./text/{filename} -i ./images/{filename} -filter_complex vstack=inputs=2 ./final/{filename}')
            return 0
        except Exception as e:
            traceback.print_exc()
            print(e)
            return 1

    async def gen_text(self, caption: str, filename: str, ctx, f_size: int = 24) -> int:
        from PIL import Image, ImageDraw, ImageFont
        try:
            ogimg = Image.open(f'./images/{filename}')
            # origonial height and width of image to be captioned
            (ogw, ogh) = ogimg.size
            print(ogimg.size)
            # set the dims of our text
            bg_h = ceil(ogh/4)
            bg_color = (255, 255, 255)
            bg_w = ogw
            bg = Image.new('RGB', (bg_w, bg_h), bg_color)
            # set our bg color in RGB
            print(bg.size)
            # create a drawn obj
            draw = ImageDraw.Draw(bg)
            # load our font in ./assets/ and our font size
            font = ImageFont.truetype('./assets/Futura-Condensed-Bold.ttf', 50)
            # set our text and text color
            txt_color = (0, 0, 0)
            text_width, text_height = draw.textsize(caption, font=font)
            text_x = (bg_w - text_width) // 2
            text_y = (bg_h - text_height) // 2
            draw.text((text_x, text_y), caption, font=font, fill=txt_color)
            bg.save(f'./text/{filename}')
            return 0
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f'something went wrong: report this')
            return 1


async def setup(bot):
    await bot.add_cog(caption(bot))
