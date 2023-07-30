import json
import os
import discord
import numpy as np

from discord.ext import commands
from discord.ext.commands import Context

from essentials.displayView import DisplayHouseInfoView, DisplayStateInfoOptionsView
from essentials.draw_regions import draw_regions
from essentials.json_util import json_open
from essentials.utils_numunit import number_formatter


class Display(commands.Cog, name="display"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="조회",
        description="Natzhashite 내의 데이터 중 일부를 조회합니다.",
    )
    async def view(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @view.command(
        name="sid",
        description="자신의 SID를 조회합니다.",
    )
    async def view_sid(self, context: Context):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            user_data = json_open(
                f"{self.bot.abs_path}/database/users/{context.author.id}.json"
            )
            primary_house = user_data["primary_house"]
            residential_data = json_open(
                f"{self.bot.abs_path}/database/residential/{context.author.id}/{primary_house}.json"
            )
            embed = discord.Embed(
                title=f"{context.author.name}의 SID를 조회합니다.",
                color=self.bot.color_main,
            )
            embed.set_thumbnail(url=context.author.avatar.url)
            embed.add_field(
                name="재산",
                value=f"{number_formatter(str(user_data['money']))} {self.bot.money_unit}",
                inline=True,
            )

            embed.add_field(
                name="현 거주지",
                value=f"{residential_data['region']}-{residential_data['name']} ({residential_data['house_type']})",
            )

            embed.add_field(name="행복도", value=user_data["happiness"])

            embed.add_field(name="건강도", value=user_data["health"])
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 신청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @view.command(
        name="집",
        description="자신의 SID를 조회합니다.",
    )
    async def view_sid(self, context: Context):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            view = DisplayHouseInfoView(self.bot, context.author, context)
            await context.send("조회할 자신의 집을 선택해주세요.", view=view)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 신청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @view.command(
        name="주",
        description="특정 주의 정보를 조회합니다.",
    )
    async def view_state_info(self, context: Context):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            view = DisplayStateInfoOptionsView(self.bot, context.author, context)
            await context.send("조회할 주를 선택해주세요.", view=view)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 신청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Display(bot))
