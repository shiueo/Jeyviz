import os
import platform
import discord

from discord.ext import commands
from discord.ext.commands import Context


class Community(commands.Cog, name="community"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="dev_리스트", description="현재 존재하는 모든 DEV계열 인원을 조회합니다."
    )
    async def level_DEV_list(self, context: Context):
        embed = discord.Embed(
            title="DEV", description="현재 존재하는 모든 DEV계열의 단체샷입니다.", color=self.bot.color_main
        )
        embed.set_image(url=self.bot.dev_banner_url)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Community(bot))
