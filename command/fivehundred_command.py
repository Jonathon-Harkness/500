from datetime import datetime
from dateutil import parser
from discord.ext import commands, tasks
import asyncio
import sqlite3
from repository import ServerRepository, PlayerRepository
from dto import PlayerDto, ServerDto
from constants import BallStatus
from service import CatchValidationService, ThrowService, CatchService
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
        if guild_id not in self.server_semaphores:
            self.server_semaphores[guild_id] = asyncio.Semaphore(self.semaphore_size)

        async with self.server_semaphores[guild_id]:
            if mystery_box:
                await ctx.send("You threw a mystery box! Let's see what happens 😈", ephemeral=True)
                await ctx.channel.send(ThrowService.processStandardThrow(ctx, points, throw_type, mystery_box))
            else:
                await ctx.send(ThrowService.processStandardThrow(ctx, points, throw_type, mystery_box))

    @commands.hybrid_command(name="throw_special", with_app_command=True)
    async def throw_special(self, ctx: commands.Context, special_effect, throw_type, points=None, mystery_box=False):
        """throws the ball. For special throws"""

        if mystery_box:
            await ctx.send("You threw a mystery box! Let's see what happens 😈", ephemeral=True)
            await ctx.channel.send(ThrowService.processSpecialThrow(ctx, special_effect, throw_type, points, mystery_box))
        else:
            await ctx.send(ThrowService.processSpecialThrow(ctx, special_effect, throw_type, points, mystery_box))

    @commands.hybrid_command(name="catch", with_app_command=True)
    async def catch(self, ctx):
        """catch the ball"""

        guild_id = ctx.author.guild.id
        if guild_id not in self.server_semaphores:
            self.server_semaphores[guild_id] = asyncio.Semaphore(self.semaphore_size)

        async with self.server_semaphores[guild_id]:
            await CatchService.processCatch(ctx)
        #
        # with sqlite3.connect(path + "/500.db") as conn:
        #     cursor = conn.cursor()
        #
        #     # get server
        #     guild_id = ctx.author.guild.id
        #     current_player_id = ctx.author.id
        #     channel_id = ctx.channel.id
        #
        #     # get current game
        #     current_game = ServerRepository.getServerInfo(guild_id, cursor)
        #
        #     # perform validation checks
        #     try:
        #         CatchValidationService.checkServerExists(current_game)
        #         CatchValidationService.checkBallActive(current_game.ball_status)
        #         CatchValidationService.checkActiveThrower(current_game.current_thrower, ctx.author)
        #     except Exception as error:
        #         await ctx.send(str(error))
        #         return
        #
        #     print(parser.parse(current_game.time_active))
        #     print(datetime.utcnow())
        #     if current_game.throw_type == "DEAD" and parser.parse(current_game.time_active) > datetime.utcnow():
        #         current_game.ball_status = str(BallStatus.INACTIVE)
        #         current_game.ball_value = 0
        #         current_game.current_thrower = None
        #         current_game.throw_type = None
        #         current_game.time_active = None
        #         current_game.throw_type_check = 0
        #         await ctx.send("You tried to catch a dead ball before it dropped! Ball can no longer be caught")
        #         ServerRepository.updateServer(current_game, cursor)
        #         return
        #
        #     # get players
        #     players_tuple = PlayerRepository.getAllPlayersFromServer(guild_id, cursor)
        #     players = {}
        #     for player in players_tuple:
        #         p = PlayerDto(*player)
        #         players[p.player_id] = p
        #
        #     if current_player_id not in players:
        #         players[current_player_id] = PlayerDto(guild_id, channel_id, current_player_id, current_game.ball_value, None, ctx.author.name, ctx.author.nick)
        #         PlayerRepository.insertPlayer(guild_id, channel_id, current_player_id, ctx.author.name, ctx.author.nick, cursor)
        #     else:
        #         players[current_player_id].points += current_game.ball_value
        #
        #     await ctx.send(f'{ ctx.author.nick } captured the ball at { current_game.ball_value } points!')
        #
        #     current_game.ball_status = str(BallStatus.INACTIVE)
        #     current_game.current_thrower = None
        #     current_game.ball_value = 0
        #     current_game.time_active = None
        #     current_game.throw_type_check = 0
        #
        #     PlayerRepository.updatePlayer(players[current_player_id], cursor)
        #     ServerRepository.updateServer(current_game, cursor)
        #
        #     if players[current_player_id].points >= 500:
        #         PlayerRepository.resetAllPlayerPointsFromServer(guild_id, cursor)
        #         await ctx.send(f'🎉 {ctx.author.nick} has won 500! 🎉')

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
