import json
import os

import discord
import numpy as np

from essentials.draw_regions import draw_regions
from essentials.json_util import json_open


class DisplayHouseInfoOptions(discord.ui.Select):
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


class DisplayHouseInfoView(discord.ui.View):
    def __init__(self, bot, author, context):
        super().__init__()
        self.author = author
        self.add_item(DisplayHouseInfoOptions(bot, context))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


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


class DisplayStateInfoOptionsView(discord.ui.View):
    def __init__(self, bot, author, context):
        super().__init__()
        self.author = author
        self.add_item(StatesInfoOptions(bot, context))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id