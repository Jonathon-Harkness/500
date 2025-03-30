from discord.ext import commands, tasks
import asyncio
import sqlite3
from repository import ServerRepository, PlayerRepository
from dto import PlayerDto, ServerDto
from constants import BallStatus
from service import ThrowService, CatchService
import os

path = os.path.dirname(os.path.realpath("500 V3"))


class FiveHundred(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.updateServersWithExpiredActiveTimeAlive.start()
        self.server_semaphores = {}
        self.semaphore_size = 1

    def cog_unload(self):
        self.updateServersWithExpiredActiveTimeAlive.cancel()

    @tasks.loop(seconds=5.0)
    async def updateServersWithExpiredActiveTimeAlive(self):
        with sqlite3.connect(path + "/500.db") as conn:

            cursor = conn.cursor()

            # For Alive
            expiredActiveServersAlive = ServerRepository.getAllServersWithExpiredActiveTimeAlive(cursor)
            for server in expiredActiveServersAlive:
                serverDto = ServerDto(*server)
                serverDto.ball_status = str(BallStatus.INACTIVE)
                serverDto.ball_value = 0
                serverDto.current_thrower = None
                serverDto.throw_type = None
                serverDto.time_active = None
                serverDto.throw_type_check = 0
                channel = self.bot.get_channel(serverDto.channel_id)
                await channel.send("Ball is No Longer Active")
                ServerRepository.updateServer(serverDto, cursor)

            # For Dead
            expiredActiveServersDead = ServerRepository.getAllServersWithExpiredActiveTimeDead(cursor)
            for server in expiredActiveServersDead:
                serverDto = ServerDto(*server)
                serverDto.throw_type_check = 1
                channel = self.bot.get_channel(serverDto.channel_id)
                await channel.send("Ball can now be retrieved!")
                ServerRepository.updateServer(serverDto, cursor)

    @commands.hybrid_command(name="throw", with_app_command=True)
    async def throw(self, ctx: commands.Context, points, throw_type, mystery_box=False):
        """throws the ball. For standard throws (usage: /throw <-500 - 500> <ALIVE, DEAD> <TRUE / FALSE>)"""

        guild_id = ctx.author.guild.id
        channel_id = ctx.channel.id
        if guild_id not in self.server_semaphores:
            self.server_semaphores[(guild_id, channel_id)] = asyncio.Semaphore(self.semaphore_size)

        async with self.server_semaphores[(guild_id, channel_id)]:
            if mystery_box:
                await ctx.send("You threw a mystery box! Let's see what happens 😈", ephemeral=True)
                await ctx.channel.send(ThrowService.processStandardThrow(ctx, points, throw_type, mystery_box))
            else:
                await ctx.send(ThrowService.processStandardThrow(ctx, points, throw_type, mystery_box))

    @commands.hybrid_command(name="throw_special", with_app_command=True)
    async def throw_special(self, ctx: commands.Context, special_effect, throw_type, points=None, mystery_box=False):
        """throws the ball. For special throws"""

        guild_id = ctx.author.guild.id
        channel_id = ctx.channel.id
        if guild_id not in self.server_semaphores:
            self.server_semaphores[(guild_id, channel_id)] = asyncio.Semaphore(self.semaphore_size)

        async with self.server_semaphores[(guild_id, channel_id)]:
            if mystery_box:
                await ctx.send("You threw a mystery box! Let's see what happens 😈", ephemeral=True)
                await ctx.channel.send(ThrowService.processSpecialThrow(ctx, special_effect, throw_type, points, mystery_box))
            else:
                await ctx.send(ThrowService.processSpecialThrow(ctx, special_effect, throw_type, points, mystery_box))

    @commands.hybrid_command(name="catch", with_app_command=True)
    async def catch(self, ctx):
        """catch the ball"""

        guild_id = ctx.author.guild.id
        channel_id = ctx.channel.id
        if guild_id not in self.server_semaphores:
            self.server_semaphores[(guild_id, channel_id)] = asyncio.Semaphore(self.semaphore_size)

        async with self.server_semaphores[(guild_id, channel_id)]:
            await CatchService.processCatch(ctx)

    # TODO embed the leaderboard
    @commands.hybrid_command(name="leaderboard", with_app_command=True)
    async def leaderboard(self, ctx):
        """show current standings"""

        conn = sqlite3.connect(path + "/500.db")
        cursor = conn.cursor()

        leaderboard = '----- LEADERBOARD -----\n'

        # get server
        guild_id = ctx.author.guild.id

        players_tuple = PlayerRepository.getAllPlayersFromServer(guild_id, cursor)
        players = []
        for player in players_tuple:
            cur_player = PlayerDto(*player)
            players.append([cur_player.points, cur_player.nickname])

        players.sort(reverse=True)
        for player in players:
            leaderboard += f'**{player[1]}**: {player[0]}\n'

        await ctx.send(leaderboard)
