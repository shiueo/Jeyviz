import json
import os
import random

import discord

from discord.ext import commands
from discord.ext.commands import Context

from essentials.user import create_user


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


class Userdata(commands.Cog, name="userdata"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="sid",
        description="SID를 생성하거나 제거, 수정을 요청합니다.",
    )
    async def sid(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @sid.command(name="신청", description="Natzhashite에서의 신분증과 같은 SID 부여를 신청합니다.")
    async def signup(self, context: Context):
        if not os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            embed = discord.Embed(
                title="SID 부여",
                description="SID는 Natzhashite에서의 신분증과 같습니다.",
                color=self.bot.color_main,
            )
            embed.add_field(
                name="Terms Of Service", value="솔직히 아직 여기 뭐 적을지 모르겠음.", inline=True
            )

            choice = YesOrNo(context.author)
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                create_user(
                    self.bot.abs_path,
                    self.bot.config,
                    self.bot.logger,
                    context.author.id,
                    context.author.name,
                )
                embed = discord.Embed(
                    title="성공",
                    description="성공적으로 SID를 부여하였습니다!",
                    color=self.bot.color_success,
                )
                await message.edit(embed=embed, view=None, content=None)
                announce_channel = self.bot.get_channel(self.bot.announce_channel)
                await announce_channel.send(
                    f"{context.author.name}님께서 Natzhashite에 정착하셨습니다!"
                )
            else:
                embed = discord.Embed(
                    title="취소", description="취소하셨습니다.", color=self.bot.color_cancel
                )
                await message.edit(embed=embed, view=None, content=None)
        else:
            embed = discord.Embed(
                title="동일한 SID가 확인되었습니다.",
                description="SID 삭제를 위해서는 ``sid_삭제_요청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @sid.command(name="삭제", description="SID 삭제를 요청합니다.")
    @commands.cooldown(1, 14400, commands.BucketType.user)
    async def signout(self, context: Context):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            embed = discord.Embed(
                title="SID 삭제 요청",
                description="Natzhashite에서의 모든 행적 및 기록이 삭제됩니다.",
                color=self.bot.color_main,
            )
            choice = YesOrNo(context.author)
            message = await context.send(embed=embed, view=choice)
            await choice.wait()
            if choice.value:
                target_del_house = []
                with open(
                    f"{self.bot.abs_path}/database/users/{context.author.id}.json", "r"
                ) as f:
                    data = json.load(f)
                    if data["primary_house"]:
                        target_del_house.append(data["primary_house"])
                    if data["owned_house"]:
                        for i in data["owned_house"]:
                            target_del_house.append(i)

                if target_del_house:
                    for i in target_del_house:
                        with open(
                            f"{self.bot.abs_path}/database/states/{i[0]}.json", "r"
                        ) as f:
                            data2 = json.load(f)
                            if [i[1], i[2]] in data2["residential"]:
                                data2["residential"].remove([i[1], i[2]])

                        with open(
                            f"{self.bot.abs_path}/database/states/{i[0]}.json", "w"
                        ) as f:
                            json.dump(data2, f)

                os.remove(
                    f"{self.bot.abs_path}/database/users/{context.author.id}.json"
                )
                embed = discord.Embed(
                    title="성공",
                    description="성공적으로 SID를 삭제하였습니다.",
                    color=self.bot.color_success,
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
                description="SID 요청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Userdata(bot))
