import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TODO: pull the commands from all cogs
    # TODO: pull special list from database
    @commands.hybrid_command(name="help_extended", with_app_command=True)
    async def help_extended(self, ctx: commands.Context):
        """Displays the detailed help menu"""
        embed = discord.Embed(
            color=discord.Color.dark_teal(),
            title="Commands"
        )
        embed.add_field(
            name="/throw",
            value="Throws the ball. For standard throws.\n"
                  "Parameters:\n"
                  " 1. points: integer value between -500 and 500\n"
                  " 2. throw_type: one of the following: (ALIVE, DEAD)\n"
                  " 3. mystery_box (optional): (True/False)\n"
                  "Example:\n"
                  " { /throw 200 ALIVE True } will throw a mystery box for 200 points alive",
            inline=False)
        embed.add_field(
            name="/throw_special",
            value="Throws the ball. For special throws. \n"
                  "Parameters:\n"
                  " 1. special_effect: one of the following: (CHERRY_BOMB, STICKY_GLUE, STINKY_GLUE)\n"
                  " 2. throw_type: one of the following: (ALIVE, DEAD)\n"
                  " 3. points (optional): integer value between -500 and 500\n"
                  " 4. mystery_box (optional): (True/False)",
            inline=False)
        embed.add_field(
            name="/catch",
            value="Catches the ball\n",
            inline=False
        )
        embed.add_field(
            name="/leaderboard",
            value="Displays the leaderboard for the match\n",
            inline=False
        )
        embed.add_field(
            name="/help",
            value="Displays the help menu\n",
            inline=False
        )
        embed.add_field(
            name="/help_extended",
            value="Displays the detailed help menu\n",
            inline=False
        )
        embed.set_footer(text="for a simplified help menu, use /help")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="help", with_app_command=True)
    async def help(self, ctx: commands.Context):
        """Displays the help menu"""
        embed = discord.Embed(
            color=discord.Color.dark_teal(),
            title="Commands"
        )
        embed.add_field(
            name="/throw",
            value="Throws the ball. For standard throws.",
            inline=False)
        embed.add_field(
            name="/throw_special",
            value="Throws the ball. For special throws.\n",
            inline=False)
        embed.add_field(
            name="/catch",
            value="Catches the ball\n",
            inline=False
        )
        embed.add_field(
            name="/leaderboard",
            value="Displays the leaderboard for the match\n",
            inline=False
        )
        embed.add_field(
            name="/help",
            value="Displays the help menu\n",
            inline=False
        )
        embed.add_field(
            name="/help_extended",
            value="Displays the detailed help menu\n",
            inline=False
        )
        embed.set_footer(text="for a detailed help menu, use /help_extended")
        await ctx.send(embed=embed)
