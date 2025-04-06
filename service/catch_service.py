import random
from repository import ServerRepository, PlayerRepository, SpecialThrowRepository
from dto import PlayerDto, SpecialEffectDto
from .catch_validation_service import CatchValidationService
from db import db, cursor
from datetime import datetime
from constants import BallStatus
from collections import defaultdict


class CatchService:

    @staticmethod
    async def processCatch(ctx):

        # get server
        guild_id = str(ctx.author.guild.id)
        current_player_id = str(ctx.author.id)
        channel_id = str(ctx.channel.id)

        # get current game
        current_game = ServerRepository.getServerInfo(guild_id, channel_id, cursor)

        # perform validation checks
        try:
            CatchValidationService.checkServerExists(current_game)
            CatchValidationService.checkBallActive(current_game.ball_status)
            CatchValidationService.checkActiveThrower(current_game.current_thrower, ctx.author)
        except Exception as error:
            await ctx.send(str(error))
            return

        if current_game.throw_type == "DEAD" and current_game.time_active > datetime.utcnow():
            current_game.ball_status = BallStatus.INACTIVE.value
            current_game.ball_value = 0
            current_game.current_thrower = None
            current_game.throw_type = None
            current_game.time_active = None
            current_game.throw_type_check = 0
            ServerRepository.updateServer(current_game, cursor)
            db.commit()
            await ctx.send("You tried to catch a dead ball before it dropped! Ball can no longer be caught")
            return

        # get players
        players_tuple = PlayerRepository.getAllPlayersFromServer(guild_id, channel_id, cursor)
        players = {}
        status_dict = defaultdict(list)
        for player in players_tuple:
            p = PlayerDto(*player)
            players[p.player_id] = p
            status_dict[p.status_effect].append({"name": p.nickname if p.nickname else p.username, "status_effect": p.status_effect})

        # get special effect (if necessary)
        special_effect_dto = None
        if current_game.special_effect:
            special_effect = SpecialThrowRepository.getSpecialThrow(cursor, current_game.special_effect)
            special_effect_dto = SpecialEffectDto(*special_effect)
            if not special_effect_dto.points_required:
                current_game.ball_value = 0

        if current_player_id not in players:
            players[current_player_id] = PlayerDto(guild_id, channel_id, current_player_id, current_game.ball_value, None, ctx.author.name, ctx.author.nick)
            PlayerRepository.insertPlayer(guild_id, channel_id, current_player_id, ctx.author.name, ctx.author.nick, cursor)
        else:
            players[current_player_id].points += current_game.ball_value

        name = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
        if "STINKY_GLUE" in status_dict:
            for i in range(len(status_dict["STINKY_GLUE"])):
                rand = random.randint(1, 4)
                if rand == 1:
                    await ctx.send(f'{ name } attempted to capture the ball, but was distracted by { status_dict["STINKY_GLUE"][i]["name"] }\'s stink!')
                    return

        if players[current_player_id].status_effect == "STICKY_GLUE":
            await ctx.send(f'{ name } attempted to capture the ball but couldn\'t move due to the sticky glue!')
            return

        if not special_effect_dto:
            await ctx.send(f'{ name } captured the ball at { current_game.ball_value } points!')
            players[current_player_id].status_effect = None
        else:
            if special_effect_dto.name == "CHERRY_BOMB":
                players[current_player_id].points = 0
                await ctx.send(f'{ name } captured the ball with effect { current_game.special_effect }! They lose all their points! 🙀')
            elif special_effect_dto.name == "STINKY_GLUE":
                players[current_player_id].status_effect = "STINKY_GLUE"
                await ctx.send(f'{ name } captured the ball with effect { current_game.special_effect } for {current_game.ball_value} points! They\'re crazy stinky and will be until the end of the next catch.')
            elif special_effect_dto.name == "STICKY_GLUE":
                players[current_player_id].status_effect = "STICKY_GLUE"
                await ctx.send(f'{ name } captured the ball with effect { current_game.special_effect } for {current_game.ball_value} points! They\'re crazy sticky and won\'t be able to catch next round!')

        current_game.ball_status = BallStatus.INACTIVE.value
        current_game.current_thrower = None
        current_game.ball_value = 0
        current_game.time_active = None
        current_game.throw_type_check = 0
        current_game.special_effect = None

        # update nickname in case they've changed it since the last play
        players[current_player_id].nickname = ctx.author.nick
        PlayerRepository.updatePlayerStatusToNull(guild_id, channel_id, cursor)
        PlayerRepository.updatePlayer(players[current_player_id], cursor)
        ServerRepository.updateServer(current_game, cursor)
        db.commit()

        if players[current_player_id].points >= 500:
            PlayerRepository.resetAllPlayerPointsFromServer(guild_id, channel_id, cursor)
            await ctx.send(f'🎉 { name } has won 500! 🎉')
