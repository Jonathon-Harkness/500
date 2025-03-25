import sqlite3
import os
import asyncio
from repository import ServerRepository, PlayerRepository
from dto import PlayerDto
from .catch_validation_service import CatchValidationService
from dateutil import parser
from datetime import datetime
from constants import BallStatus


path = os.path.dirname(os.path.realpath("500 V3"))


class CatchService:

    @staticmethod
    async def processCatch(ctx):

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

            print(parser.parse(current_game.time_active))
            print(datetime.utcnow())
            if current_game.throw_type == "DEAD" and parser.parse(current_game.time_active) > datetime.utcnow():
                current_game.ball_status = str(BallStatus.INACTIVE)
                current_game.ball_value = 0
                current_game.current_thrower = None
                current_game.throw_type = None
                current_game.time_active = None
                current_game.throw_type_check = 0
                ServerRepository.updateServer(current_game, cursor)
                await ctx.send("You tried to catch a dead ball before it dropped! Ball can no longer be caught")

            # get players
            players_tuple = PlayerRepository.getAllPlayersFromServer(guild_id, cursor)
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

            current_game.ball_status = str(BallStatus.INACTIVE)
            current_game.current_thrower = None
            current_game.ball_value = 0
            current_game.time_active = None
            current_game.throw_type_check = 0

            PlayerRepository.updatePlayer(players[current_player_id], cursor)
            ServerRepository.updateServer(current_game, cursor)

            if players[current_player_id].points >= 500:
                PlayerRepository.resetAllPlayerPointsFromServer(guild_id, cursor)
                await ctx.send(f'🎉 {ctx.author.nick} has won 500! 🎉')

            await asyncio.sleep(5)