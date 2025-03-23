from datetime import datetime, timedelta
from discord.ext import commands, tasks
import sqlite3
from repository import ServerRepository, PlayerRepository
from dto import PlayerDto, ServerDto
from constants import THROW_TYPE, BallStatus
from service import CatchValidationService, ThrowValidationService
import os

path = os.path.dirname(os.path.realpath("500 V3"))


class FiveHundred(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.updateServersWithExpiredActiveTime.start()

    def cog_unload(self):
        self.updateServersWithExpiredActiveTime.cancel()

    @tasks.loop(seconds=5.0)
    async def updateServersWithExpiredActiveTime(self):
        with sqlite3.connect(path + "/500.db") as conn:
            cursor = conn.cursor()
            expiredActiveServers = ServerRepository.getAllServersWithExpiredActiveTime(cursor)
            for server in expiredActiveServers:
                serverDto = ServerDto(*server)
                serverDto.ball_status = BallStatus.INACTIVE
                serverDto.ball_value = 0
                serverDto.current_thrower = None
                serverDto.throw_type = None
                serverDto.time_active = None
                channel = self.bot.get_channel(serverDto.channel_id)
                await channel.send("Ball is No Longer Active")
                ServerRepository.updateServer(serverDto, cursor)

    @commands.hybrid_command(name="throw", with_app_command=True)
    async def throw(self, ctx: commands.Context, points, throw_type):
        """throws the ball (usage: /throw <-2000 - 500> <ALIVE, DEAD>)"""

        with sqlite3.connect(path + "/500.db") as conn:
            cursor = conn.cursor()
            throw_type = throw_type.upper()
            if throw_type not in THROW_TYPE:
                await ctx.send(f'{throw_type} is not a valid Throw Type')
                return

            # keep the ball alive for 300 seconds or 20 seconds if dead
            time_active = 300 if throw_type == 'ALIVE' else 20

            # get server
            guild_id = ctx.author.guild.id
            channel_id = ctx.channel.id
            player_id = ctx.author.id
            ball_status = 'INACTIVE'
            current_game = ServerRepository.getServerInfo(guild_id, cursor)

            if not current_game:
                ServerRepository.insertServer(
                    ServerDto(guild_id, channel_id, ball_status, points, throw_type, datetime.now(), player_id), cursor)
                current_game = ServerDto(guild_id, channel_id, ball_status, points, throw_type, datetime.now(), player_id)

            # validate input
            try:
                ThrowValidationService.checkBallActive(current_game.ball_status)
                ThrowValidationService.checkActiveThrower(current_game.current_thrower, ctx.author.id)
                ThrowValidationService.checkValidPointInput(points)
            except Exception as error:
                await ctx.send(str(error))
                return

            current_game.guild_id = guild_id
            current_game.ball_value = int(points)
            current_game.ball_status = 'ACTIVE'
            current_game.current_thrower = player_id
            current_game.throw_type = throw_type
            current_game.time_active = datetime.utcnow() + timedelta(seconds=time_active)

            # update game
            ServerRepository.updateServer(current_game, cursor)

            throw_type_message = f"You have {time_active / 60.0} minutes to catch it!" if throw_type == 'ALIVE' else ''
            await ctx.send(f'{ctx.author.nick} threw the ball for {points} points {throw_type}! {throw_type_message}')

    @commands.hybrid_command(name="catch", with_app_command=True)
    async def catch(self, ctx):
        """catch the ball"""

        with sqlite3.connect(path + "/500.db") as conn:
            cursor = conn.cursor()

            # get server
            guild_id = ctx.author.guild.id
            current_player_id = ctx.author.id
            channel_id = ctx.channel.id

            # get current game
            current_game = ServerRepository.getServerInfo(guild_id, cursor)

            # perform validation checks
            try:
                CatchValidationService.checkServerExists(current_game)
                CatchValidationService.checkBallActive(current_game.ball_status)
                CatchValidationService.checkActiveThrower(current_game.current_thrower, ctx.author)
            except Exception as error:
                await ctx.send(str(error))
                return

            # get players
            players_tuple = PlayerRepository.getAllPlayersFromServer(guild_id)
            players = {}
            for player in players_tuple:
                p = PlayerDto(*player)
                players[p.player_id] = p

            if current_player_id not in players:
                players[current_player_id] = PlayerDto(guild_id, channel_id, current_player_id, current_game.ball_value, None, ctx.author.name, ctx.author.nick)
                PlayerRepository.insertPlayer(guild_id, channel_id, current_player_id, ctx.author.name, ctx.author.nick, cursor)
            else:
                players[current_player_id].points += current_game.ball_value

            await ctx.send(f'{ ctx.author.nick } captured the ball at { current_game.ball_value } points!')

            current_game.ball_status = 'INACTIVE'
            current_game.current_thrower = None
            current_game.ball_value = 0
            current_game.time_active = None

            PlayerRepository.updatePlayer(players[current_player_id], cursor)
            ServerRepository.updateServer(current_game, cursor)

            if players[current_player_id].points >= 500:
                PlayerRepository.resetAllPlayerPointsFromServer(guild_id,cursor)
                await ctx.send(f'🎉 {ctx.author.nick} has won 500! 🎉')

    @commands.hybrid_command(name="leaderboard", with_app_command=True)
    async def leaderboard(self, ctx):
        """show current standings"""
        leaderboard = '----- LEADERBOARD -----\n'

        # get server
        guild_id = ctx.author.guild.id

        players_tuple = PlayerRepository.getAllPlayersFromServer(guild_id)
        players = []
        for player in players_tuple:
            cur_player = PlayerDto(*player)
            players.append([cur_player.points, cur_player.nickname])

        players.sort(reverse=True)
        for player in players:
            leaderboard += f'**{player[1]}**: {player[0]}\n'

        await ctx.send(leaderboard)
