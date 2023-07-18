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
        if os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
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
                        os.remove(f"{self.bot.abs_path}/database/users/{user.id}.json")
                        embed = discord.Embed(
                            title="삭제 완료.", description=f"성공적으로 {member}의 SID를 삭제하였습니다.", color=self.bot.color_success
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
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 요청을 위해서는 ``sid_요청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="dev_모든_주_초기화", description="모든 주의 변수를 초기 설정 값으로 되돌립니다."
    )
    async def dev_states_reset(self, context: Context):
        if os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
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
                            print(f"./database/users/{user_file}")
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
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 요청을 위해서는 ``sid_요청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ForDev(bot))
