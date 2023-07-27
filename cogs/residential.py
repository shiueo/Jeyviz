import os
import platform
import discord
from discord import app_commands

from discord.ext import commands
from discord.ext.commands import Context

from essentials.json_util import json_open
from essentials.residential import edit_house_name


class HouseInfoOptions(discord.ui.Select):
    def __init__(self, bot, context, new_name):
        self.bot = bot
        self.context = context
        self.new_name = new_name
        options = []
        houses = [
            file
            for file in os.listdir(
                f"{self.bot.abs_path}/database/residential/{self.context.author.id}"
            )
            if file.endswith(".json")
        ]

        for house in houses:
            house_data = json_open(
                f"{self.bot.abs_path}/database/residential/{self.context.author.id}/{house}"
            )
            options.append(
                discord.SelectOption(
                    label=house_data["name"], description=house_data["house_type"]
                )
            )
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        user_choice = self.values[0]
        house_region, house_type = edit_house_name(
            self.bot.abs_path,
            self.context.author.id,
            user_choice,
            f"{self.bot.abs_path}/database/residential/{self.context.author.id}/{user_choice}.json",
            self.new_name,
        )
        embed = discord.Embed(
            title=f"{user_choice} 수정 완료.",
            description=f"{user_choice} -> {self.new_name}",
            color=self.bot.color_main,
        )
        await interaction.response.edit_message(embed=embed, content=None, view=None)
        announce_channel = self.bot.get_channel(self.bot.announce_channel)
        await announce_channel.send(
            f"{self.context.author.name}님 소유의 {house_region}: {user_choice} ({house_type})의 이름이 {self.new_name}으로 바뀌었습니다."
        )


class HouseInfoView(discord.ui.View):
    def __init__(self, bot, author, context, new_name):
        super().__init__()
        self.author = author
        self.add_item(HouseInfoOptions(bot, context, new_name))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


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
            if (
                len(
                    os.listdir(
                        f"{self.bot.abs_path}/database/residential/{context.author.id}"
                    )
                )
                > 0
            ):
                if not os.path.isfile(
                    f"{self.bot.abs_path}/database/residential/{context.author.id}/{new_house_name}.json"
                ):
                    view = HouseInfoView(
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
                    description="건물/집의 이름은 12자를 넘을 수 없습니다.",
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


async def setup(bot):
    await bot.add_cog(Residential(bot))
