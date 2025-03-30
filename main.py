import discord
from discord.ext import commands
import constants
import scripts
from cog import FiveHundred, Help

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)
scripts.run()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.add_cog(Help(bot))
    await bot.add_cog(FiveHundred(bot))


@bot.command(name="sync")
async def sync(ctx):
    bot.tree.clear_commands(guild=ctx.author.guild)
    bot.tree.copy_global_to(guild=ctx.author.guild)
    synced = await bot.tree.sync(guild=ctx.author.guild)
    print(f"Synced {len(synced)} command(s).")

bot.run(constants.TOKEN)
