import os
import logging
import shelve

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests


class SemidbmShelf(shelve.Shelf):
    """Shelf implementation using the "semidbm" dbm interface.
    This is initialized with the filename for the dbm database.
    See the module's __doc__ string for an overview of the interface.
    """

    def __init__(self, filename, flag='c', protocol=None, writeback=False):
        import semidbm
        shelve.Shelf.__init__(self, semidbm.open(filename, flag), protocol, writeback)


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
database = SemidbmShelf('games', writeback=True)


@bot.command(
    name = 'stats'
)
async def stats(ctx: commands.Context):
    embed=discord.Embed(title='Not Gambling Stats', color=discord.Color.green())
    embed.add_field(name='Current ping', value=bot.latency, inline=False)
    embed.add_field(name='Active games', value=len(database.dict.keys()), inline=False)
    embed.add_field(name='Guild ID', value=ctx.guild.id, inline=False)
    await ctx.send(embed=embed)


@bot.command(
    name = 'joke'
)
async def joke(ctx: commands.Context):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://icanhazdadjoke.com/', headers={'Accept': 'text/plain'}) as r:
            await ctx.send(await r.text())


async def is_owner(ctx: commands.Context):
    return ctx.author.id == 338005893377556480


@bot.command(
    name = 'eval',
    hidden=True
)
@commands.check(is_owner)
async def eval_command(ctx: commands.Context, *, code):
    try:
        result = eval(code)
    except Exception as e:
        await ctx.send(embed=create_error(f'`{e.__class__.__qualname__}: {e}`', 'Eval error'))
    else:
        await ctx.send(f'`{result}`')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=f'{bot.command_prefix}help'
    ))


@bot.event
async def on_command_error(ctx: commands.Context, *args, **kwargs):
    if isinstance(args[0], commands.CommandNotFound):
        return
    await ctx.send(embed=create_error(args[0]))


@bot.event
async def on_disconnect():
    database.sync()
    database.dict.compact()


bot.run(TOKEN)
