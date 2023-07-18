from discord.ext import commands


class Mail(commands.Cog, name="mail"):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Mail(bot))
