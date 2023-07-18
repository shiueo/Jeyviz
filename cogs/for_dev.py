import json
import os
import platform
import discord

from discord.ext import commands
from discord.ext.commands import Context


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


class ForDev(commands.Cog, name="for_dev"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="dev_sid_삭제", description="해당 유저의 SID를 삭제합니다."
    )
    async def dev_sid_delete(self, context: Context, user: discord.User):
        if str(context.author.id) in self.bot.owners:
            member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
            embed = discord.Embed(
                title="SID_삭제", description=f"{member}의 SID를 삭제합니다.", color=self.bot.color_main
            )
            choice = YesOrNo(context.author)
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                if os.path.isfile(f"{self.bot.abs_path}/database/users/{user.id}.json"):
                    target_del_house = []
                    with open(f"{self.bot.abs_path}/database/users/{user.id}.json", 'r') as f:
                        data = json.load(f)
                        if data['primary_house']:
                            target_del_house.append(data['primary_house'])
                        if data['owned_house']:
                            target_del_house.append(data['owned_house'])

                    if target_del_house:
                        state = target_del_house[0][0]
                        for i in target_del_house:
                            with open(f"{self.bot.abs_path}/database/states/{i[0]}.json", 'r') as f:
                                data2 = json.load(f)
                                data2['occupied_coordinates'].remove([i[1], i[2]])

                        with open(f"{self.bot.abs_path}/database/states/{state}.json", 'w') as f:
                            json.dump(data2, f)

                    os.remove(f"{self.bot.abs_path}/database/users/{user.id}.json")
                    embed = discord.Embed(
                        title="성공", description="성공적으로 SID를 삭제하였습니다.", color=self.bot.color_success
                    )
                    await message.edit(embed=embed, view=None, content=None)
                else:
                    embed = discord.Embed(
                        title="오류.", description=f"{member}의 SID는 존재하지 않습니다.", color=self.bot.color_cancel
                    )
                    await message.edit(embed=embed, view=None, content=None)
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)
        else:
            embed = discord.Embed(
                title="오류.", description="당신은 DEV계열이 아닙니다.", color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="dev_모든_주_초기화", description="모든 주의 변수를 초기 설정 값으로 되돌립니다."
    )
    async def dev_states_reset(self, context: Context):
        if str(context.author.id) in self.bot.owners:
            embed = discord.Embed(
                title="모든 주 초기화", description="모든 주의 변수를 초기 설정 값으로 되돌립니다.", color=self.bot.color_main
            )
            choice = YesOrNo(context.author)
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                for state in self.bot.states:
                    data = {
                        "initial_support_money": eval(f"self.bot.{state}_initial_money"),
                        "grid_x": 0,
                        "grid_y": 0,
                        "occupied_coordinates": []
                    }
                    with open(f"{self.bot.abs_path}/database/states/{state}.json", 'w') as f:
                        json.dump(data, f)

                for user_file in os.listdir(f"{self.bot.abs_path}/database/users/"):
                    if user_file.endswith(".json"):
                        with open(f"./database/users/{user_file}", 'r') as file:
                            data = json.load(file)
                            data['primary_house'] = []
                            data['owned_house'] = []
                        with open(f"./database/users/{user_file}", 'w') as file:
                            json.dump(data, file)

                    self.bot.logger.info(f"{state} 초기화 완료.")

                    embed = discord.Embed(
                        title="초기화 완료.", description=f"모든 주의 변수가 초기 값으로 돌아갔습니다.", color=self.bot.color_success
                    )
                    await message.edit(embed=embed, view=None, content=None)
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)
        else:
            embed = discord.Embed(
                title="오류.", description="당신은 DEV계열이 아닙니다.", color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="dev_sid_add_money", description="해당 유저의 SID에 주어진 수만큼 SCU를 추가합니다."
    )
    async def dev_sid_add_money(self, context: Context, user: discord.User, money: int):
        if str(context.author.id) in self.bot.owners:
            member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
            embed = discord.Embed(
                title="금액 충전", description=f"{member}의 SID에 {money}SCU를 추가합니다.", color=self.bot.color_main
            )
            choice = YesOrNo(context.author)
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                if os.path.isfile(f"{self.bot.abs_path}/database/users/{member.id}.json"):
                    with open(f"{self.bot.abs_path}/database/users/{member.id}.json", 'r') as f:
                        data = json.load(f)
                        data['money'] += money

                    with open(f"{self.bot.abs_path}/database/users/{member.id}.json", 'w') as f:
                        json.dump(data, f)

                    embed = discord.Embed(
                        title="성공", description=f"성공적으로 {money}SCU를 {member}의 SID에 추가하였습니다.",
                        color=self.bot.color_success
                    )
                    await message.edit(embed=embed, view=None, content=None)
                else:
                    embed = discord.Embed(
                        title="오류.", description=f"{member}의 SID는 존재하지 않습니다.", color=self.bot.color_cancel
                    )
                    await message.edit(embed=embed, view=None, content=None)
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)
        else:
            embed = discord.Embed(
                title="오류.", description="당신은 DEV계열이 아닙니다.", color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="dev_natzhashite_dashboard", description="Natzhashite의 상태를 확인합니다."
    )
    async def dev_check_natzhashite(self, context: Context):
        if str(context.author.id) in self.bot.owners:
            embed = discord.Embed(
                title="Natzhashite 현 상황", description=None, color=self.bot.color_main
            )

            all_spaces = 0
            all_occupied_spaces = 0
            for state in self.bot.states:
                with open(f"{self.bot.abs_path}/database/states/{state}.json", 'r') as f:
                    data = json.load(f)
                    all_spaces += (data['grid_x']+1)*(data['grid_y']+1)
                    all_occupied_spaces += len(data['occupied_coordinates'])

            embed.add_field(name="Spaces", value=f"{all_occupied_spaces}/{all_spaces}", inline=True)

            embed.add_field(name="Users", value=len(os.listdir(f"{self.bot.abs_path}/database/users")), inline=True)

            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="오류.", description="당신은 DEV계열이 아닙니다.", color=self.bot.color_cancel
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ForDev(bot))
