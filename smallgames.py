import aiohttp
import discord
from discord.ext import commands

class SimpleGames(commands.Cog, name='Simple Games/Commands'):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(
        name = 'joke',
        brief = 'Tell a short joke'
    )
    async def joke(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://icanhazdadjoke.com/', headers={'Accept': 'text/plain'}) as r:
                await ctx.send(await r.text())
