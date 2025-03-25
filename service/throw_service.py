from discord.ext import commands
import sqlite3
import os
from constants import THROW_TYPE, BallStatus
from repository import ServerRepository, SpecialThrowRepository
from dto import ServerDto, SpecialEffectDto
from datetime import datetime, timedelta
from util import sanitize_input
from .throw_validation_service import ThrowValidationService

path = os.path.dirname(os.path.realpath("500 V3"))


class ThrowService:

    @staticmethod
    def processThrow():
        pass

    @staticmethod
    def processStandardThrow(ctx: commands.Context, points: int, throw_type: str, mystery_box: bool):
        with sqlite3.connect(path + "/500.db") as conn:
            cursor = conn.cursor()
            throw_type = throw_type.upper()
            if throw_type not in THROW_TYPE:
                return f'{throw_type} is not a valid Throw Type'

            # get server
            guild_id = ctx.author.guild.id
            channel_id = ctx.channel.id
            player_id = ctx.author.id
            ball_status = BallStatus.INACTIVE.value
            current_game = ServerRepository.getServerInfo(guild_id, cursor)

            if not current_game:
                ServerRepository.insertServer(
                    ServerDto(guild_id, channel_id, ball_status, points, throw_type, 0, datetime.now(), player_id),
                    cursor)
                current_game = ServerDto(guild_id, channel_id, ball_status, points, throw_type, 0, datetime.now(),
                                         player_id)

            # validate input
            try:
                ThrowValidationService.checkBallActive(current_game.ball_status)
                ThrowValidationService.checkActiveThrower(current_game.current_thrower, ctx.author.id)
                ThrowValidationService.checkValidPointInput(points)
            except Exception as error:
                return str(error)

            # keep the ball alive for 300 seconds or 20 seconds if dead
            time_active = 300 if throw_type == 'ALIVE' else 20

            current_game.guild_id = guild_id
            current_game.ball_value = int(points)
            current_game.ball_status = 'ACTIVE'
            current_game.current_thrower = player_id
            current_game.throw_type = throw_type
            current_game.time_active = datetime.utcnow() + timedelta(seconds=time_active)

            # update game
            ServerRepository.updateServer(current_game, cursor)

            throw_type_message = f"You have {time_active / 60.0} minutes to catch it!" if throw_type == 'ALIVE' else \
                f'You have to wait {time_active} seconds before you catch it!'

            if mystery_box:
                return f"{ctx.author.nick} threw a MYSTERY BOX {throw_type} 😈! {throw_type_message}"
            return f'{ctx.author.nick} threw the ball for {points} points {throw_type}! {throw_type_message}'

    @staticmethod
    def processSpecialThrow(ctx: commands.Context, special_effect: str, throw_type: str, points: int, mystery_box: bool):
        special_effect = sanitize_input(special_effect).upper()

        with sqlite3.connect(path + "/500.db") as conn:
            cursor = conn.cursor()
            throw_type = throw_type.upper()
            if throw_type not in THROW_TYPE:
                return f'{throw_type} is not a valid Throw Type'

            # get server
            guild_id = ctx.author.guild.id
            channel_id = ctx.channel.id
            player_id = ctx.author.id
            ball_status = str(BallStatus.INACTIVE)
            current_game = ServerRepository.getServerInfo(guild_id, cursor)

            if not current_game:
                ServerRepository.insertServer(
                    ServerDto(guild_id, channel_id, ball_status, points, throw_type, 0, datetime.now(), player_id, special_effect),
                    cursor)
                current_game = ServerDto(guild_id, channel_id, ball_status, points, throw_type, 0, datetime.now(),
                                         player_id, special_effect)

            # get special throw
            special_effect_entity = SpecialThrowRepository.getSpecialThrow(cursor, special_effect)
            if not special_effect_entity:
                return f"{special_effect} is not a valid special effect! "
            special_effect_dto = SpecialEffectDto(*special_effect_entity)

            # validate input
            try:
                ThrowValidationService.checkBallActive(current_game.ball_status)
                ThrowValidationService.checkActiveThrower(current_game.current_thrower, ctx.author.id)
                ThrowValidationService.checkIfSpecialThrowRequiresPoints(special_effect_dto, points)
            except Exception as error:
                return str(error)

            # keep the ball alive for 300 seconds or 20 seconds if dead
            time_active = 300 if throw_type == 'ALIVE' else 20

            current_game.guild_id = guild_id
            current_game.ball_value = points
            current_game.ball_status = 'ACTIVE'
            current_game.current_thrower = player_id
            current_game.throw_type = throw_type
            current_game.time_active = datetime.utcnow() + timedelta(seconds=time_active)
            current_game.special_effect = special_effect_dto.name

            # update game
            ServerRepository.updateServer(current_game, cursor)

            throw_type_message = f"You have {time_active / 60.0} minutes to catch it!" if throw_type == 'ALIVE' else \
                f'You have to wait {time_active} seconds before you catch it!'

            points = f"for {points} points" if special_effect_dto.points_required else ''
            if mystery_box:
                return f"{ctx.author.nick} threw a MYSTERY BOX {throw_type} 😈! {throw_type_message}"
            return f'{ctx.author.nick} threw {special_effect} {points} {throw_type}! {throw_type_message}'
