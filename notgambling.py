import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv


class EmbedErrorHelp(commands.DefaultHelpCommand):
    async def send_error_message(self, error):
        await self.get_destination().send(embed=create_error(error))


def create_error(body, title='Error'):
    return discord.Embed(title=str(title), description=str(body), color=discord.Color.red())


logging.basicConfig(
    format='[%(asctime)s] [%(threadName)s/%(levelname)s] [%(filename)s:%(lineno)i]: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot('*', help_command=EmbedErrorHelp())


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(f'{bot.command_prefix}help'))


bot.run()
