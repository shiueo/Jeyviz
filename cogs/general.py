import os
import platform
import discord

from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="명령어", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context):
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=self.bot.color_main
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            jeyviz_commands = cog.get_commands()
            data = []
            for command in jeyviz_commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="정보",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context):
        embed = discord.Embed(
            description="[디스코드 안 작은 세상! 가상세계 Natzhashite로 Jeyviz가 여러분을 초대합니다!](https://jeyviz.vercel.app/)",
            color=self.bot.color_main,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(
            name="Prefix:", value="/ (Slash Commands) or +", inline=True
        )
        embed.add_field(
            name="Written in:", value=f"Python {platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Running on:", value=f"{platform.system()} {platform.release()} ({os.name})", inline=True
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="개발자",
        description="Jeyviz의 제작자들",
    )
    async def dev(self, context: Context):
        embed = discord.Embed(
            description="Jeyviz 제작에 기여하신 분들입니다.",
            color=self.bot.color_main,
        )
        embed.set_author(name="Dev")
        embed.set_image(url="https://github.com/shiueo/shiueo/raw/main/pfp/shiueo_wallpaper_v4.png")
        embed.add_field(name="Head", value="[shiueo](https://www.youtube.com/@shiueo)", inline=True)
        embed.add_field(name="Contributors", value="", inline=True)
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
