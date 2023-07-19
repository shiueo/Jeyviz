import asyncio
import json
import logging
import os
import platform
import random
import sys
import discord as discord

from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from utils.utils_logger import LoggingFormatter

if not os.path.isfile("config.json"):
    sys.exit("config.json이 없습니다. 확인해주세요.")
else:
    with open("config.json") as f:
        config = json.load(f)

intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None,
)

bot.config = config
bot.abs_path = os.path.dirname(__file__)
bot.color_main = int(config["color_main"], 16)
bot.color_success = int(config["color_success"], 16)
bot.color_cancel = int(config["color_cancel"], 16)
bot.dev_banner_url = config["dev_banner_url"]
bot.owners = config["owners"]
bot.states = config["states"]
bot.money_unit = config["money_unit"]
bot.visualize_residential_block = config["visualize_residential_block"]
bot.visualize_nothing_block = config["visualize_nothing_block"]
bot.visualize_corporate_block = config["visualize_corporate_block"]
bot.visualize_industrial_block = config["visualize_industrial_block"]
bot.visualize_natural_block = config["visualize_natural_block"]
bot.visualize_security_block = config["visualize_security_block"]
bot.visualize_traffic_block = config["visualize_traffic_block"]
bot.visualize_hospital_block = config["visualize_hospital_block"]
bot.visualize_leisure_block = config["visualize_leisure_block"]
bot.corp_establish_minimum_currency = config["corp_establish_minimum_currency"]

for state in bot.states:
    exec(f"bot.{state}_initial_money = config['{state}_initial_money']")

logger = logging.getLogger("Jeyviz_bot")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler

file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


@bot.event
async def on_ready():
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    bot.logger.info("Syncing commands globally...")
    status_task.start()
    await bot.tree.sync()


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_error(context: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"이 명령어는 {f'{round(hours)} 시간' if round(hours) > 0 else ''} {f'{round(minutes)} 분' if round(minutes) > 0 else ''} {f'{round(seconds)} 초' if round(seconds) > 0 else ''} 뒤에 다시 사용하실 수 있습니다.",
            color=bot.color_cancel,
        )
        await context.send(embed=embed)


@bot.event
async def on_command_completion(context: Context):
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


async def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")


@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", "with shiüo!", "with users!", "Geometry Dash", "Osu!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


asyncio.run(load_cogs())
bot.run(config["token"])
