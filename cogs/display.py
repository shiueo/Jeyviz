import json
import os
import platform
import discord

from PIL import Image
from discord.ext import commands
from discord.ext.commands import Context

from utils.utils_numunit import number_formatter


class StatesInfoOptions(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Ashan", description="something"
            ),
            discord.SelectOption(
                label="Cronokz", description="something"
            ),
            discord.SelectOption(
                label="Esteny", description="something"
            ),
            discord.SelectOption(
                label="Ghranten", description="something"
            ),
            discord.SelectOption(
                label="Khachlen", description="something"
            ),
            discord.SelectOption(
                label="Novorsk", description="something"
            ),
            discord.SelectOption(
                label="Quadrian",
                description="Quadrian은 Natzhashite의 서남부에 자리한 매우 발전된 지역 중 하나로, 탄탄한 기반시설과 다양한 편의시설을 제공합니다."
            ),
            discord.SelectOption(
                label="Realmz", description="something"
            ),
            discord.SelectOption(
                label="Rocktz", description="something"
            ),
            discord.SelectOption(
                label="Schtarn", description="Schtarn은 Natzhashite의 중심부에 자리 잡은 매우 현대적이고 번화한 도심 지역입니다."
            ),
            discord.SelectOption(
                label="Tetrin", description="something"
            ),
            discord.SelectOption(
                label="Utenie", description="something"
            ),
            discord.SelectOption(
                label="Zhalka", description="Zhalka는 Natzhashite의 변두리에 위치한 지역으로, 경제적으로 유리한 면을 갖추고 있습니다."
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

        with open(f"{self.bot.abs_path}/database/states/{user_choice}.json", 'r') as f:
            data = json.load(f)

            embed = discord.Embed(
                title=f"{user_choice} 주의 정보", description="", color=self.bot.color_main
            )

            embed.add_field(
                name="초기 정착 지원 자금",
                value=f"{number_formatter(str(data['initial_support_money']))} {self.bot.money_unit}", inline=True
            )
            embed.add_field(
                name="주 전체 면적", value=f"{(data['grid_x'] + 1) * (data['grid_y'] + 1)} S2DU", inline=True
            )
            embed.add_field(
                name="사용된 부지 면적", value=f"{len(data['residential']) + len(data['corporate']) + len(data['industrial']) + len(data['natural']) + len(data['traffic']) + len(data['security'])} S2DU", inline=True
            )

            await interaction.response.edit_message(
                embed=embed, content=None, view=None
            )


class StateInfoOptionsView(discord.ui.View):
    def __init__(self, bot, author):
        super().__init__()
        self.author = author
        self.add_item(StatesInfoOptions(bot))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


class StatesVisualizeOptions(discord.ui.Select):
    def __init__(self, bot, context):
        self.bot = bot
        self.context = context
        options = [
            discord.SelectOption(
                label="Ashan", description="something"
            ),
            discord.SelectOption(
                label="Cronokz", description="something"
            ),
            discord.SelectOption(
                label="Esteny", description="something"
            ),
            discord.SelectOption(
                label="Ghranten", description="something"
            ),
            discord.SelectOption(
                label="Khachlen", description="something"
            ),
            discord.SelectOption(
                label="Novorsk", description="something"
            ),
            discord.SelectOption(
                label="Quadrian",
                description="Quadrian은 Natzhashite의 서남부에 자리한 매우 발전된 지역 중 하나로, 탄탄한 기반시설과 다양한 편의시설을 제공합니다."
            ),
            discord.SelectOption(
                label="Realmz", description="something"
            ),
            discord.SelectOption(
                label="Rocktz", description="something"
            ),
            discord.SelectOption(
                label="Schtarn", description="Schtarn은 Natzhashite의 중심부에 자리 잡은 매우 현대적이고 번화한 도심 지역입니다."
            ),
            discord.SelectOption(
                label="Tetrin", description="something"
            ),
            discord.SelectOption(
                label="Utenie", description="something"
            ),
            discord.SelectOption(
                label="Zhalka", description="Zhalka는 Natzhashite의 변두리에 위치한 지역으로, 경제적으로 유리한 면을 갖추고 있습니다."
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

        with open(f"{self.bot.abs_path}/database/states/{user_choice}.json", 'r') as f:
            data = json.load(f)

            image = Image.new('RGB', (data['grid_x'] + 1, data['grid_y'] + 1), color=tuple(int(self.bot.visualize_nothing_block[i:i + 2], 16) for i in (0, 2, 4)))
            px_image = image.load()

            for i in data['residential']:
                px_image[i[0], i[1]] = tuple(int(self.bot.visualize_residential_block[i:i + 2], 16) for i in (0, 2, 4))
            for i in data['corporate']:
                px_image[i[0], i[1]] = tuple(int(self.bot.visualize_corporate_block[i:i + 2], 16) for i in (0, 2, 4))
            for i in data['industrial']:
                px_image[i[0], i[1]] = tuple(int(self.bot.visualize_industrial_block[i:i + 2], 16) for i in (0, 2, 4))
            for i in data['natural']:
                px_image[i[0], i[1]] = tuple(int(self.bot.visualize_natural_block[i:i + 2], 16) for i in (0, 2, 4))
            for i in data['traffic']:
                px_image[i[0], i[1]] = tuple(int(self.bot.visualize_traffic_block[i:i + 2], 16) for i in (0, 2, 4))
            for i in data['security']:
                px_image[i[0], i[1]] = tuple(int(self.bot.visualize_security_block[i:i + 2], 16) for i in (0, 2, 4))

            file_name = f"{self.bot.abs_path}/database/visualize/{user_choice}_viz.png"
            image = image.resize((1000, 1000), Image.Resampling.NEAREST)
            image.save(file_name)

            file = discord.File(file_name)
            embed = discord.Embed(title=f"{user_choice} Visualization", description=None, color=self.bot.color_main)
            embed.add_field(name="공터", value="⬛", inline=True)
            embed.add_field(name="교통", value="🟪", inline=True)
            embed.add_field(name="주거", value="🟧", inline=True)
            embed.add_field(name="산업", value="🟫", inline=True)
            embed.add_field(name="기업", value="🟦", inline=True)
            embed.add_field(name="자연", value="🟩", inline=True)
            embed.add_field(name="치안", value="🟥", inline=True)
            embed.set_image(url=f'attachment://{user_choice}_viz.png')

            await interaction.response.edit_message(
                content=f"{user_choice} 주의 시각화 자료를 생성중입니다.", view=None
            )
            await self.context.send(embed=embed, file=file)


class StateVisualizeOptionsView(discord.ui.View):
    def __init__(self, bot, author, context):
        super().__init__()
        self.author = author
        self.add_item(StatesVisualizeOptions(bot, context))

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
        if os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
            with open(f"{self.bot.abs_path}/database/users/{context.author.id}.json", 'r') as f:
                data = json.load(f)
                embed = discord.Embed(
                    title=f"{data['name']}의 SID를 조회합니다.",
                    color=self.bot.color_main,
                )
                embed.set_thumbnail(url=context.author.avatar.url)
                embed.add_field(
                    name="이름", value=data['name']
                )
                embed.add_field(
                    name="재산", value=f"{number_formatter(str(data['money']))} {self.bot.money_unit}", inline=True
                )
                if data['primary_house']:
                    primary_house = data['primary_house']
                    embed.add_field(
                        name="현 거주지", value=f"{primary_house[0]}-X{primary_house[1]}Y{primary_house[2]}"
                    )
                else:
                    embed.add_field(
                        name="현 거주지", value="None"
                    )
                if data['owned_house']:
                    owned_house = ', '.join(data['owned_house'])
                else:
                    owned_house = "None"
                embed.add_field(
                    name="추가적 주택", value=owned_house
                )
                if data['owned_company']:
                    owned_company = ', '.join(data['owned_company'])
                else:
                    owned_company = None
                embed.add_field(
                    name="소유한 회사", value=owned_company
                )
                if data['employed_company']:
                    employed_company = ', '.join(data['employed_company'])
                else:
                    employed_company = "None"
                embed.add_field(
                    name="채용된 회사", value=employed_company
                )

                embed.add_field(
                    name="행복도", value=data['happiness']
                )

                embed.add_field(
                    name="건강도", value=data['health']
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 신청을 위해서는 ``sid_신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @view.command(
        name="주",
        description="특정 주의 정보를 조회합니다.",
    )
    async def view_state_info(self, context: Context):
        if os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
            view = StateInfoOptionsView(self.bot, context.author)
            await context.send("조회할 주를 선택해주세요.", view=view)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 신청을 위해서는 ``sid_신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @view.command(
        name="주_시각화",
        description="특정 주의 현 상황을 시각화합니다.",
    )
    async def view_state_visualize(self, context: Context):
        if os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
            view = StateVisualizeOptionsView(self.bot, context.author, context)
            await context.send("시각화할 주를 선택해주세요.", view=view)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 신청을 위해서는 ``sid_신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Display(bot))
