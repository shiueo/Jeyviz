import json
import os
import platform
import discord

from discord.ext import commands
from discord.ext.commands import Context


class Display(commands.Cog, name="display"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="sid_조회",
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
                    name="재산", value=f"{data['money']}", inline=True
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
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.", description="SID 요청을 위해서는 ``sid_요청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Display(bot))
