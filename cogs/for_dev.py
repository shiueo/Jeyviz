import os
import platform
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
                title="SID_삭제", description="해당 유저의 SID를 삭제합니다.", color=self.bot.color_main
            )
            choice = YesOrNo()
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


async def setup(bot):
    await bot.add_cog(ForDev(bot))
