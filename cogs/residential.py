import os
import platform
import discord
from discord import app_commands

from discord.ext import commands
from discord.ext.commands import Context

from essentials.residentialView import HouseNameView, HouseCostView, DisplayHouseInfoView


class Residential(commands.Cog, name="residential"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="집",
        description="집에 관련한 정보를 수정요청 할 수 있습니다.",
    )
    async def house(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @house.command(name="이름_수정", description="소유한 집의 이름을 주어진 값으로 수정합니다.")
    async def change_name(
            self, context: Context, new_house_name: app_commands.Range[str, 1, 12]
    ):
        if os.path.isfile(
                f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            if os.listdir(f"{self.bot.abs_path}/database/residential/{context.author.id}"):
                if not os.path.isfile(
                        f"{self.bot.abs_path}/database/residential/{context.author.id}/{new_house_name}.json"
                ):
                    view = HouseNameView(
                        self.bot, context.author, context, new_house_name
                    )
                    await context.send("이름을 바꿀 자신의 집을 선택해주세요.", view=view)
                else:
                    embed = discord.Embed(
                        title="처리 불가.",
                        description="이미 소유한 집들 중 중복되는 이름이 있습니다.",
                        color=self.bot.color_cancel,
                    )
                    await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="처리 불가.",
                    description="집이 없습니다.",
                    color=self.bot.color_cancel,
                )
                await context.send(embed=embed)

        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 요청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @house.command(name="가격_수정", description="소유한 집의 가격을 주어진 값으로 수정합니다.")
    async def change_name(
            self, context: Context, new_cost: int
    ):
        if os.path.isfile(
                f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            if os.listdir(f"{self.bot.abs_path}/database/residential/{context.author.id}"):
                view = HouseCostView(
                    self.bot, context.author, context, new_cost
                )
                await context.send("가격 바꿀 자신의 집을 선택해주세요.", view=view)
            else:
                embed = discord.Embed(
                    title="처리 불가.",
                    description="집이 없습니다.",
                    color=self.bot.color_cancel,
                )
                await context.send(embed=embed)

        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 요청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @house.command(
        name="조회",
        description="자신의 집 정보를 조회합니다.",
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


async def setup(bot):
    await bot.add_cog(Residential(bot))
