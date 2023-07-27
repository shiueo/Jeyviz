import json
import os
import discord
import numpy as np

from discord.ext import commands
from discord.ext.commands import Context

from essentials.draw_regions import draw_regions
from essentials.json_util import json_open
from essentials.utils_numunit import number_formatter


class StatesInfoOptions(discord.ui.Select):
    def __init__(self, bot, context):
        self.bot = bot
        self.context = context
        options = [
            discord.SelectOption(label="Ashan", description="something"),
            discord.SelectOption(label="Cronokz", description="something"),
            discord.SelectOption(label="Esteny", description="something"),
            discord.SelectOption(label="Ghranten", description="something"),
            discord.SelectOption(
                label="Khachlen", description="Khachlen은 Natzhashite 최대의 항구도시입니다."
            ),
            discord.SelectOption(label="Novorsk", description="something"),
            discord.SelectOption(
                label="Quadrian",
                description="Quadrian은 Natzhashite의 서남부에 자리한 매우 발전된 지역 중 하나로, 탄탄한 기반시설과 다양한 편의시설을 제공합니다.",
            ),
            discord.SelectOption(label="Realmz", description="something"),
            discord.SelectOption(label="Rocktz", description="something"),
            discord.SelectOption(
                label="Schtarn",
                description="Schtarn은 Natzhashite의 중심부에 자리 잡은 매우 현대적이고 번화한 도심 지역입니다.",
            ),
            discord.SelectOption(label="Tetrin", description="something"),
            discord.SelectOption(label="Utenie", description="something"),
            discord.SelectOption(
                label="Zhalka",
                description="Zhalka는 Natzhashite의 변두리에 위치한 지역으로, 경제적으로 유리한 면을 갖추고 있습니다.",
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        user_choice = self.values[0]
        choice = self.bot.config[f"{user_choice}_regions"]
        draw_regions(user_choice, self.bot.abs_path, self.bot.config, choice)

        file = discord.File(f"{self.bot.abs_path}/database/viz/{user_choice}.png")

        await interaction.response.edit_message(
            content=f"요청하신 {user_choice} 주에 대한 상세정보입니다.", view=None
        )
        embed = discord.Embed(
            title=f"{user_choice} 주", description="", color=self.bot.color_main
        )

        RESIDENTIAL = []
        CORPORATE = []
        INDUSTRIAL = []
        NATURAL = []
        TRAFFIC = []
        SECURITY = []
        HOSPITAL = []
        LEISURE = []
        T_RESIDENTIAL = []
        T_CORPORATE = []
        T_INDUSTRIAL = []
        T_NATURAL = []
        T_TRAFFIC = []
        T_SECURITY = []
        T_HOSPITAL = []
        T_LEISURE = []
        for region in choice:
            with open(f"{self.bot.abs_path}/database/regions/{region}.json", "r") as f:
                data = json.load(f)
                T_RESIDENTIAL.append(data["residential"])
                T_CORPORATE.append(data["corporate"])
                T_INDUSTRIAL.append(data["industrial"])
                T_NATURAL.append(data["natural"])
                T_TRAFFIC.append(data["traffic"])
                T_SECURITY.append(data["security"])
                T_HOSPITAL.append(data["hospital"])
                T_LEISURE.append(data["leisure"])

        other_regions = [x for x in self.bot.config["regions"] if x not in choice]

        for region in other_regions:
            with open(f"{self.bot.abs_path}/database/regions/{region}.json", "r") as f:
                data = json.load(f)
                RESIDENTIAL.append(data["residential"])
                CORPORATE.append(data["corporate"])
                INDUSTRIAL.append(data["industrial"])
                NATURAL.append(data["natural"])
                TRAFFIC.append(data["traffic"])
                SECURITY.append(data["security"])
                HOSPITAL.append(data["hospital"])
                LEISURE.append(data["leisure"])

        RESIDENTIAL += T_RESIDENTIAL
        CORPORATE += T_CORPORATE
        INDUSTRIAL += T_INDUSTRIAL
        NATURAL += T_NATURAL
        TRAFFIC += T_TRAFFIC
        SECURITY += T_SECURITY
        HOSPITAL += T_HOSPITAL
        LEISURE += T_LEISURE

        float_max_len = 2
        embed.add_field(
            name="주거 (SRM)",
            value=f"{np.round(np.mean(T_RESIDENTIAL),float_max_len)} / {np.round(np.mean(RESIDENTIAL), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="기업 (SCM)",
            value=f"{np.round(np.mean(T_CORPORATE),float_max_len)} / {np.round(np.mean(CORPORATE), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="산업 (SIM)",
            value=f"{np.round(np.mean(T_INDUSTRIAL),float_max_len)} / {np.round(np.mean(INDUSTRIAL), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="자연 (SNM)",
            value=f"{np.round(np.mean(T_NATURAL),float_max_len)} / {np.round(np.mean(NATURAL), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="교통 (STM)",
            value=f"{np.round(np.mean(T_TRAFFIC),float_max_len)} / {np.round(np.mean(TRAFFIC), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="치안 (SSM)",
            value=f"{np.round(np.mean(T_SECURITY),float_max_len)} / {np.round(np.mean(SECURITY), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="병원 (SHM)",
            value=f"{np.round(np.mean(T_HOSPITAL),float_max_len)} / {np.round(np.mean(HOSPITAL), float_max_len)} (전체 평균)",
            inline=True,
        )
        embed.add_field(
            name="여가 (SLM)",
            value=f"{np.round(np.mean(T_LEISURE),float_max_len)} / {np.round(np.mean(LEISURE), float_max_len)} (전체 평균)",
            inline=True,
        )
        await self.context.send(embed=embed, file=file)


class StateInfoOptionsView(discord.ui.View):
    def __init__(self, bot, author, context):
        super().__init__()
        self.author = author
        self.add_item(StatesInfoOptions(bot, context))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


class HouseInfoOptions(discord.ui.Select):
    def __init__(self, bot, context):
        self.bot = bot
        self.context = context
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
        house_data = json_open(
            f"{self.bot.abs_path}/database/residential/{self.context.author.id}/{user_choice}.json"
        )
        embed = discord.Embed(
            title=f"주택: {user_choice}", description="", color=self.bot.color_main
        )
        embed.add_field(
            name="주택 위치",
            value=f"{house_data['region']}",
            inline=True,
        )
        embed.add_field(
            name="주택 종류",
            value=f"{house_data['house_type']}",
            inline=True,
        )
        embed.add_field(
            name="주택 가격",
            value=f"{house_data['cost']}",
            inline=True,
        )
        await interaction.response.edit_message(embed=embed, content=None, view=None)


class HouseInfoView(discord.ui.View):
    def __init__(self, bot, author, context):
        super().__init__()
        self.author = author
        self.add_item(HouseInfoOptions(bot, context))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


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
            view = HouseInfoView(self.bot, context.author, context)
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
            view = StateInfoOptionsView(self.bot, context.author, context)
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
