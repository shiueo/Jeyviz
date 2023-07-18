import json
import os

import discord

from discord.ext import commands
from discord.ext.commands import Context


class YesOrNo(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

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


class Userdata(commands.Cog, name="userdata"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="sid_요청", description="Natzhashite에서의 신분증과 같은 SID를 요청합니다."
    )
    async def signup(self, context: Context):
        if not os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
            embed = discord.Embed(
                title="SID 부여", description="SID는 Natzhashite에서의 신분증과 같습니다.", color=self.bot.color_main
            )
            embed.add_field(name="Terms Of Service", value="솔직히 아직 여기 뭐 적을지 모르겠음.", inline=True)

            choice = YesOrNo()
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                data = {
                    'dev': 0,
                    'name': context.author.name,
                    'money': 0,
                    'owned_company': [],
                    'employed_company': [],
                    'job': [],
                }
                with open(f"{self.bot.abs_path}/database/users/{context.author.id}.json", 'w') as f:
                    json.dump(data, f)
                embed = discord.Embed(
                    title="성공", description="성공적으로 SID를 부여하였습니다!", color=self.bot.color_success
                )
                await message.edit(embed=embed, view=None, content=None)
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)
        else:
            embed = discord.Embed(
                title="동일한 SID가 확인되었습니다.", description="SID 삭제를 위해서는 ``sid_삭제_요청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="sid_삭제_요청", description="SID 삭제를 요청합니다."
    )
    async def signout(self, context: Context):
        if os.path.isfile(f"{self.bot.abs_path}/database/users/{context.author.id}.json"):
            embed = discord.Embed(
                title="SID 삭제 요청", description="Natzhashite에서의 모든 행적 및 기록이 삭제됩니다.", color=self.bot.color_main
            )
            choice = YesOrNo()
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                os.remove(f"{self.bot.abs_path}/database/users/{context.author.id}.json")
                embed = discord.Embed(
                    title="성공", description="성공적으로 SID를 삭제하였습니다.", color=self.bot.color_success
                )
                await message.edit(embed=embed, view=None, content=None)
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 요청을 위해서는 ``sid_요청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Userdata(bot))
