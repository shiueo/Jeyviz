import json
import os
import platform
import discord
import hashlib

from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

from utils.utils_numunit import number_formatter


class YesOrNo(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.value = None
        self.author = author

    @discord.ui.button(label="네", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = True
        self.stop()

    @discord.ui.button(label="아니요", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


class Corporations(commands.Cog, name="corporations"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="법인",
        description="SID를 생성하거나 제거, 수정을 요청합니다.",
    )
    async def corp(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @corp.command(name="설립", description=f"자신만의 법인을 설립합니다.")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="은행 및 금융 서비스", value="은행 및 금융 서비스"),
            app_commands.Choice(name="제조 및 생산", value="제조 및 생산"),
            app_commands.Choice(name="소매 및 유통", value="소매 및 유통"),
            app_commands.Choice(name="건설 및 부동산", value="건설 및 부동산"),
            app_commands.Choice(name="의료 및 보건", value="의료 및 보건"),
            app_commands.Choice(name="여행 및 호텔", value="여행 및 호텔"),
            app_commands.Choice(name="미디어 및 엔터테인먼트", value="미디어 및 엔터테인먼트"),
            app_commands.Choice(name="음식점 및 외식 서비스", value="음식점 및 외식 서비스"),
        ]
    )
    async def corp_establish(
        self, context: Context, corp_name: str, option: app_commands.Choice[str]
    ):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            embed = discord.Embed(
                title=f"{corp_name}을/를 설립합니다.",
                description=f"필요한 금액은 {number_formatter(str(self.bot.corp_establish_minimum_currency))} {self.bot.money_unit}입니다.",
                color=self.bot.color_main,
            )
            choice = YesOrNo(context.author)
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                if os.path.isfile(
                    f"{self.bot.abs_path}/database/users/{context.author.id}.json"
                ):
                    with open(
                        f"{self.bot.abs_path}/database/users/{context.author.id}.json",
                        "r",
                    ) as f:
                        data = json.load(f)
                        money = data["money"]

                    if money >= self.bot.corp_establish_minimum_currency:
                        if corp_name.lower() not in [
                            i.lower()[:-5]
                            for i in os.listdir(
                                f"{self.bot.abs_path}/database/corporations/"
                            )
                        ]:
                            embed = discord.Embed(
                                title=f"성공적으로 {corp_name}을 설립하셨습니다.",
                                color=self.bot.color_main,
                            )

                            data["money"] -= self.bot.corp_establish_minimum_currency
                            data["owned_company"].append(corp_name)
                            with open(
                                f"{self.bot.abs_path}/database/users/{context.author.id}.json",
                                "w",
                            ) as f:
                                json.dump(data, f)

                            data = {
                                "code": hashlib.md5(corp_name.encode()).hexdigest(),
                                "stock_available": 0,
                                "stock_price": 0,
                                "owner_list": [],
                                "employee_list": [],
                                "type": option.name,
                            }
                            embed.add_field(name="법인명", value=corp_name)
                            embed.add_field(name="법인 코드", value=data["code"])
                            embed.add_field(name="상장 여부", value="비상장")
                            embed.add_field(name="업종", value=data["type"])

                            with open(
                                f"{self.bot.abs_path}/database/corporations/{corp_name}.json",
                                "w",
                            ) as f:
                                json.dump(data, f)

                            await message.edit(embed=embed, view=None, content=None)

                        else:
                            embed = discord.Embed(
                                title=f"{corp_name}은 이미 등록된 법인명입니다.",
                                description=f"다른 이름을 사용해주세요.",
                                color=self.bot.color_cancel,
                            )
                            await message.edit(embed=embed, view=None, content=None)
                    else:
                        embed = discord.Embed(
                            title="잔액이 부족합니다.",
                            description=f"최소 {number_formatter(str(self.bot.corp_establish_minimum_currency))} {self.bot.money_unit}가 필요합니다.",
                            color=self.bot.color_cancel,
                        )
                        await message.edit(embed=embed, view=None, content=None)
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)

        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 신청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Corporations(bot))
