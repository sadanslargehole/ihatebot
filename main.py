import discord
from discord.ext import commands
import json
from os import listdir
import asyncio
from util import loadconfig
#load the config
config=loadconfig('config.json')
#declare intents 
#TODO not include all intents
intents = discord.Intents.all()
#define the bot
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
# load exts
bot.config= config
async def load():
    for i in listdir('exts'):
        try:
            if i == '__pycache__':
                continue
            i=i.replace('.py', '')
            await bot.load_extension(f'exts.{i}')
            print(f'loaded: {i}')
        except Exception as e:
            print(f'error while loading {i}')
            print(e)
asyncio.run(load())
bot.owner_ids=bot.config['admins']
bot.run("MTA0ODc3ODQyNzM1Mzc5MjYzNA.GsLsqc.PF0nZCj3_QAheFOzK4PhLyooWe3Y2XS6cOn6s0")
