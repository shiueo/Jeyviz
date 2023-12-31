import asyncio
import json
import logging
import os
import platform
import random
import psutil
import sys
import discord as discord

from collections import deque
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from essentials.functions import inflation_function
from essentials.json_util import json_open, json_dump
from utils.utils_logger import LoggingFormatter

if not os.path.isfile("config.json"):
    sys.exit("config.json이 없습니다. 확인해주세요.")
else:
    with open("config.json", encoding="utf8") as f:
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
bot.color_thank = int(config["color_thank"], 16)
bot.color_success = int(config["color_success"], 16)
bot.color_cancel = int(config["color_cancel"], 16)
bot.dev_banner_url = config["dev_banner_url"]
bot.owners = config["owners"]
bot.money_unit = config["money_unit"]
bot.announce_channel = config["announcing_channel"]
bot.system_types = config["system_types"]
bot.cpu_usage = deque([0] * 60)
bot.ram_usage = deque([0] * 60)
bot.disk_usage = deque([0]*60)

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
    update_inflation.start()
    update_status.start()
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


@tasks.loop(minutes=1.0)
async def update_inflation():
    bot.logger.info(f"================= UPDATE INFLATION =================")
    states = bot.config["states"]
    for state in states:
        state_data = json_open(f"{bot.abs_path}/database/states/{state}.json")
        regions = bot.config[f"{state}_regions"]
        score = 0
        for region in regions:
            region_data = json_open(f"{bot.abs_path}/database/regions/{region}.json")
            for system_type in bot.system_types:
                score += eval(f"region_data['{system_type}']")

        inflation_val = inflation_function(score)
        state_data["inflation"] = inflation_val
        bot.logger.info(f"{state} -> INFLATION_VAL: {inflation_val}")
        json_dump(state_data, f"{bot.abs_path}/database/states/{state}.json")

    bot.logger.info(f"인플레이션률 계산 완료.")


@tasks.loop(seconds=1.0)
async def update_status():
    bot.cpu_usage.append(psutil.cpu_percent())
    bot.cpu_usage.popleft()
    bot.ram_usage.append(psutil.virtual_memory().percent)
    bot.ram_usage.popleft()
    bot.disk_usage.append(psutil.disk_usage('/').percent)
    bot.disk_usage.popleft()


asyncio.run(load_cogs())
bot.run(config["token"])
