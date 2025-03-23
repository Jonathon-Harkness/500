# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import sqlite3
import CommandController
import constants

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
conn = sqlite3.connect('500.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS SERVER "
          "(GUILD_ID INTEGER, "
          "CHANNEL_ID INTEGER, "
          "BALL_STATUS TEXT, "
          "BALL_VALUE INTEGER, "
          "THROW_TYPE TEXT, "
          "TIME_ACTIVE DATETIME, "
          "CURRENT_THROWER INTEGER, "
          "PRIMARY KEY (GUILD_ID, CHANNEL_ID))")
c.execute("CREATE TABLE IF NOT EXISTS PLAYER "
          "(GUILD_ID INTEGER, "
          "CHANNEL_ID INTEGER, "
          "PLAYER_ID INTEGER, "
          "POINTS INTEGER, "
          "STATUS_EFFECT TEXT, "
          "USERNAME TEXT, "
          "NICKNAME TEXT, "
          "PRIMARY KEY (GUILD_ID, PLAYER_ID, CHANNEL_ID))")
conn.commit()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.add_cog(CommandController.FiveHundred(bot))


@bot.command(name="sync")
async def sync(ctx):
    bot.tree.clear_commands(guild=ctx.author.guild)
    bot.tree.copy_global_to(guild=ctx.author.guild)
    synced = await bot.tree.sync(guild=ctx.author.guild)
    print(f"Synced {len(synced)} command(s).")

bot.run(constants.TOKEN)
