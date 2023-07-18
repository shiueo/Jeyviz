import os
import platform
import discord

from discord.ext import commands
from discord.ext.commands import Context


class Economy(commands.Cog, name="economy"):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Economy(bot))
