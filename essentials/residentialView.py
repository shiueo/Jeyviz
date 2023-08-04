import os

import discord

from essentials.json_util import json_open
from essentials.residential import edit_house_cost, edit_house_name
from essentials.utils_numunit import format_number_with_units


class HouseNameOptions(discord.ui.Select):
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
            description=None,
            color=self.bot.color_success,
        )
        embed.add_field(name="수정 전", value=f"{user_choice}")
        embed.add_field(name="수정 후", value=f"{self.new_name}")
        await interaction.response.edit_message(embed=embed, content=None, view=None)
        announce_channel = self.bot.get_channel(self.bot.announce_channel)
        await announce_channel.send(
            f":house: The name of ``{user_choice} ({house_type})`` in the ``{house_region}`` region, owned by ``{self.context.author.name}``, has been changed to ``{self.new_name}``."
        )


class HouseNameView(discord.ui.View):
    def __init__(self, bot, author, context, new_name):
        super().__init__()
        self.author = author
        self.add_item(HouseNameOptions(bot, context, new_name))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


class HouseCostOptions(discord.ui.Select):
    def __init__(self, bot, context, new_cost):
        self.bot = bot
        self.context = context
        self.new_cost = new_cost
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
        house_region, house_type, old_cost = edit_house_cost(
            target_house_path=f"{self.bot.abs_path}/database/residential/{self.context.author.id}/{user_choice}.json",
            new_cost=self.new_cost
        )
        embed = discord.Embed(
            title=f"{user_choice} 수정 완료.",
            description=None,
            color=self.bot.color_success,
        )
        embed.add_field(name="수정 전", value=f"{format_number_with_units(bot=self.bot, number=old_cost)}")
        embed.add_field(name="수정 후", value=f"{format_number_with_units(bot=self.bot, number=self.new_cost)}")
        await interaction.response.edit_message(embed=embed, content=None, view=None)
        announce_channel = self.bot.get_channel(self.bot.announce_channel)
        await announce_channel.send(
            f":house: The price of ``{user_choice} ({house_type})`` in the ``{house_region}`` region, owned by ``{self.context.author.name}``, has been changed to ``{format_number_with_units(bot=self.bot, number=self.new_cost)}``."
        )


class HouseCostView(discord.ui.View):
    def __init__(self, bot, author, context, new_cost):
        super().__init__()
        self.author = author
        self.add_item(HouseCostOptions(bot, context, new_cost))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


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
            value=f"{format_number_with_units(bot=self.bot, number=house_data['cost'])}",
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
