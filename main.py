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
bot.owner_ids=config['admins']
bot.run(config['token'])
