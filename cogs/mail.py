import os
import natsort
import discord

from typing import Any, Optional
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from functools import cached_property
from discord.ui import View
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.ui.button import button

from essentials.json_util import json_open
from essentials.mail import send_mail


class Mail_Paginator(View):
    def __init__(
        self,
        bot,
        author,
        embeds,
        timeout=120,
    ):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.embeds = embeds
        self.author = author
        self.index = 0
        self.selected = False

    @cached_property
    def total(self) -> int:
        return len(self.embeds)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id

    @button(label="이전", style=ButtonStyle.primary)
    async def prev(self, interaction: Interaction, _: Any) -> None:
        self.index -= 1

        if self.index < 0:
            self.index = self.total - 1

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @button(label="다음", style=ButtonStyle.primary)
    async def next(self, interaction: Interaction, _: Any) -> None:
        self.index += 1

        if self.index >= self.total:
            self.index = 0

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @button(label="닫기", style=ButtonStyle.danger)
    async def close(self, interaction: Interaction, _: Any) -> None:
        embed = discord.Embed(
            title="Schtarn Mail",
            description="오늘도 저희 서비스를 이용해주셔서 감사합니다.",
            color=self.bot.color_thank,
        )
        embed.set_image(url=self.bot.config["mailing_system_logo_url"])
        embed.set_footer(
            text="This service is operated with support of Schtarn.",
            icon_url=self.bot.config["manager_organization_logo_url"],
        )
        await interaction.response.edit_message(embed=embed, content=None, view=None)
        self.stop()


class Mail(commands.Cog, name="mail"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="메일",
        description="Natzhashite 내의 데이터 중 일부를 조회합니다.",
    )
    async def mail(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @mail.command(
        name="조회",
        description="자신의 메일을 조회합니다.",
    )
    async def view_mail(self, context: Context):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            mails = natsort.natsorted(
                os.listdir(f"{self.bot.abs_path}/database/mails/{context.author.id}")
            )[::-1]
            if len(mails) == 0:
                embed = discord.Embed(
                    title="아무것도 없습니다! 아무것도요!",
                    description="아무것도 없어요!",
                    color=self.bot.color_cancel,
                )

                await context.send(embed=embed)

            else:
                embeds = []
                index = 1
                for mail in mails:
                    data = json_open(
                        f"{self.bot.abs_path}/database/mails/{context.author.id}/{mail}"
                    )
                    embed = discord.Embed(
                        title=f"{data['title']} - {index} / {len(mails)}",
                        description=None,
                        color=self.bot.color_main,
                    )
                    embed.add_field(name="From", value=data["from"], inline=False)
                    embed.add_field(name="Date", value=data["date"], inline=False)
                    embed.add_field(name="Content", value=data["content"], inline=False)
                    embed.set_footer(
                        text="This service is operated with support of Schtarn.",
                        icon_url=self.bot.config["manager_organization_logo_url"],
                    )
                    if data["image"]:
                        embed.set_image(url=data["image"])

                    embeds.append(embed)
                    index += 1
                mail_view = Mail_Paginator(self.bot, context.author, embeds)
                await context.send(embed=embeds[0], view=mail_view)
        else:
            embed = discord.Embed(
                title="SID가 존재하지 않습니다.",
                description="SID 신청을 위해서는 ``sid 신청`` 명령어를 사용해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @mail.command(name="발송", description="주어진 사람에게 메일을 발송합니다.")
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def send_mail(
        self,
        context: Context,
        receiver_id: str,
        title: app_commands.Range[str, 1, 256],
        content: app_commands.Range[str, 1, 1024],
        image_url: Optional[str] = "",
    ):
        if os.path.isfile(
            f"{self.bot.abs_path}/database/users/{context.author.id}.json"
        ):
            if os.path.isfile(f"{self.bot.abs_path}/database/users/{receiver_id}.json"):
                send_mail(
                    path=self.bot.abs_path,
                    title=title,
                    content=content,
                    sender=context.author,
                    receiver_id=receiver_id,
                    image=image_url,
                )
                embed = discord.Embed(
                    title="성공",
                    description="성공적으로 메일을 발송하였습니다.",
                    color=self.bot.color_success,
                )
                embed.set_footer(
                    text="This service is operated with support of Schtarn.",
                    icon_url=self.bot.config["manager_organization_logo_url"],
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="오류",
                    description="Natzhashite에 정착하신 분들 중에서만 메일을 발송할 수 있습니다.",
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
    await bot.add_cog(Mail(bot))
