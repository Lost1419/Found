import time
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}\nCurrent Activity Name & Type: {self.bot.activity.name}, {self.bot.activity.type}")

def setup(bot):
    bot.add_cog(Events(bot))
