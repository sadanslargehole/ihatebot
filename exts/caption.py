import discord
from discord.ext import commands
import ffmpeg
import traceback
from math import ceil, floor

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
           # await ctx.send(file=file)
            a = await self.merge_images(filenametmp, ctx)
        if a == 0:
            file = discord.File(f'./final/{filenametmp}')
            await ctx.send(file=file)

    async def merge_images(self, filename: str, ctx):
        try:
            # system(    
            # f'ffmpeg -y -i ./text/{filename} -i ./images/{filename} -filter_complex vstack=inputs=2 ./final/{filename}')
            text=ffmpeg.input(f'./text/{filename}')
            image=ffmpeg.input(f'./images/{filename}')
            joined = ffmpeg.filter([text,image], 'vstack')
            out=ffmpeg.output(joined, f'./final/{filename}').overwrite_output()
            ffmpeg.run(out)
            return 0
        except Exception as e:
            traceback.print_exc()
            print(e)
            return 1

    async def gen_text(self, caption: str, filename: str, ctx, f_size: int = 24) -> list[int, int, int]:
        from PIL import Image, ImageDraw, ImageFont
        try:
            #funtions and shit
            def get_words_per_line(bg_w, tmp_cpn, draw, font_s:int=50 ):
                for i in reversed(range(len(tmp_cpn))):
                    font = ImageFont.truetype('./Futura-Condensed-Bold.ttf', 50)
                    cpn= ' '.join(tmp_cpn[0:i-1])
                    tmp_text_width, tmp_text_height = draw.textsize(cpn, font=font) 
                    if tmp_text_width< bg_w:
                        return (i-1, tmp_text_height, len(tmp_cpn)//i-1, font_s) #returns (words per line, height of words(max), total lines,font size(will be used soon:tm:)  )
                    #minus one to account for differnt length words
                    # might change to -2 
            
            #-------------------------------------------------------------------------------------------------------------------------------------
            
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
            font = ImageFont.truetype('./Futura-Condensed-Bold.ttf', 50)
            # set our text and text color
            txt_color = (0, 0, 0)
            #set the default ammount of lines that will be used in the caption
            lines=1
            text_width, text_height = draw.textsize(caption, font=font)
            if text_width >= bg_w:
                tmp_cpn=' '.join(caption)
                linedata=get_words_per_line(bg_w, tmp_cpn, draw)
                bg = Image.new('RGB', (bg_w, (linedata[1]*(linedata[2]+2))), bg_color)
                bg_w, bg_h=bg.size
                font = ImageFont.truetype('./Futura-Condensed-Bold.ttf',50)
                draw=ImageDraw.Draw(bg)
                
                for i in range(linedata[2]+1):
                    tmp_text_width, tmp_text_height = draw.textsize(tmp_cpn[i*linedata[0]:(i+1)*linedata[0]], font=font)
                    text_x = (bg_w - tmp_text_width ) // 2 
                    text_y=((bg_h-linedata[1])//linedata[2])*(i+1)
                    draw.text((text_x, text_y),tmp_cpn[i*linedata[0]:(i+1)*linedata[0]],font=font, fill=txt_color)
            #     split=len(tmp_cpn)//2
            #     cpn_1=' '.join(tmp_cpn[0:split])
            #     print(cpn_1)
            #     cpn_2=' '.join(tmp_cpn[split:])
            #     print(cpn_2)
            #     lines=2
            # if lines==2:
            #     text_width1, text_height1 = draw.textsize(cpn_1, font=font)
            #     text_y1 = ((bg_h - text_height1) // 3)
            #     text_x1 = (bg_w - text_width1) // 2
            #     text_width2, text_height2 = draw.textsize(cpn_2, font=font)
            #     text_y2 = ((bg_h - text_height2) // 3)*2
            #     text_x2 = (bg_w - text_width2) // 2
            #     draw.text((text_x1, text_y1), cpn_1, font=font, fill=txt_color)
            #     draw.text((text_x2, text_y2), cpn_2, font=font, fill=txt_color)
            # if lines==1:

            #     text_x = (bg_w - text_width) // 2
            #     text_y = (bg_h - text_height) // 2
            #     draw.text((text_x, text_y), caption, font=font, fill=txt_color, anchor='mm')
                
                


            bg.save(f'./text/{filename}')
            return 0
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f'oops, you fucked up')
            return 1


async def setup(bot):
    await bot.add_cog(caption(bot))
