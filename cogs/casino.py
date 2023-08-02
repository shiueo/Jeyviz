import os
import platform
import random

import discord

from discord.ext import commands
from discord.ext.commands import Context

from essentials.json_util import json_open, json_dump


class Casino(commands.Cog, name="casino"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="도박",
        description="¯\\_(ツ)_/¯ 인생 한방",
    )
    async def casino(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @casino.command(name="플립", description="해봐해봐")
    async def bet_x2(self, context: Context, amount: int):
        if os.path.isfile(
                f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            user_data = json_open(f"{self.bot.abs_path}/database/users/{context.author.id}.json")
            natzhashite_data = json_open(f"{self.bot.abs_path}/database/natzhashite.json")
            if user_data['money'] >= amount > 0:
                user_data['money'] -= amount
                natzhashite_data['money'] += amount

                random_val = random.uniform(-2, 1.5)
                user_data['money'] += int(amount * random_val)
                if random_val > 0:
                    embed = discord.Embed(
                        title="대박!",
                        description=f"{amount * random_val} {self.bot.money_unit} 획득!",
                        color=self.bot.color_success,
                    )
                    await context.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="실패!",
                        description=f"{amount * random_val} {self.bot.money_unit}잃음...",
                        color=self.bot.color_cancel,
                    )
                    await context.send(embed=embed)
                json_dump(user_data, f"{self.bot.abs_path}/database/users/{context.author.id}.json")
                json_dump(natzhashite_data, f"{self.bot.abs_path}/database/natzhashite.json")
            else:
                embed = discord.Embed(
                    title="돈 없어요",
                    description="거지래요",
                    color=self.bot.color_cancel,
                )
                await context.send(embed=embed)

        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 신청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Casino(bot))
