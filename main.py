import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", activity=discord.Activity(type=discord.ActivityType.watching, name="Matchey sleep"), status=discord.Status.idle, intents = discord.Intents.all(), owner_ids=[803765021712056340, 759579956140834826])

extensions = ["cogs.normal", "cogs.admin", "cogs.events", "cogs.economy"]
for extension in extensions:
    bot.load_extension(extension)

bot.run("")