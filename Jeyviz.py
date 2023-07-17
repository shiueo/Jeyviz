import json
import os
import sys
import discord as discord

from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

if not os.path.isfile("config.json"):
    sys.exit("config.json이 없습니다. 확인해주세요.")
else:
    with open("config.json") as f:
        config = json.load(f)

intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None
)

bot.run(config["token"])
