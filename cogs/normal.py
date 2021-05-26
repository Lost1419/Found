from discord.ext import commands


class Normal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.send(f"{msg}")

    @commands.command()
    async def purge(self, ctx, amount: int):
        if amount > 1:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"**{amount}** messages have been deleted")
        elif amount == 1:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"**{amount}** message have been deleted")
        else:
            await ctx.send(f"Please enter a number **above** 0")

def setup(bot):
    bot.add_cog(Normal(bot))
