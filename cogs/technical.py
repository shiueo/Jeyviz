import os
import natsort
import discord

from typing import Any, Optional
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from functools import cached_property
import matplotlib.pyplot as plt
from discord.ui import View
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.ui.button import button

from essentials.draw_system_usage import draw_system_usage
from essentials.json_util import json_open


class Technical(commands.Cog, name="technical"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="기술지원",
        description="Jeyviz의 상태를 확인합니다.",
    )
    async def tech(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @tech.command(
        name="하드웨어",
        desciption="Jeyviz의 하드웨어 상태를 보여줍니다."
    )
    async def cpu_ram_disk(self, context: Context):
        draw_system_usage(path=self.bot.abs_path, cpu_usage=self.bot.cpu_usage,
                          ram_usage=self.bot.ram_usage,
                          disk_usage=self.bot.disk_usage)

        file = discord.File(f"{self.bot.abs_path}/database/viz/system_usage.png")
        await context.send(f"CPU: {self.bot.cpu_usage[59]}%\nRAM: {self.bot.ram_usage[59]}%\nDISK USAGE: {self.bot.disk_usage[59]}", file=file)


async def setup(bot):
    await bot.add_cog(Technical(bot))
