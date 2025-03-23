from datetime import datetime, timedelta
from discord.ext import commands, tasks
import sqlite3
from repository import ServerRepository, PlayerRepository
from dto import PlayerDto, ServerDto


class FiveHundred(commands.Cog):
    BALL_STATUS = {'ACTIVE', 'INACTIVE'}
    THROW_TYPE = {'ALIVE', 'DEAD'}

    def __init__(self, bot):
        self.bot = bot
        self.throw_types = {'ALIVE', 'DEAD'}
        self.updateServersWithExpiredActiveTime.start()

    def cog_unload(self):
        self.updateServersWithExpiredActiveTime.cancel()

    @tasks.loop(seconds=5.0)
    async def updateServersWithExpiredActiveTime(self):
        expiredActiveServers = ServerRepository.getAllServersWithExpiredActiveTime()
        for server in expiredActiveServers:
            serverDto = ServerDto(*server)
            if serverDto.throw_type == 'ALIVE':
                serverDto.ball_status = 'INACTIVE'
                serverDto.ball_value = 0
                serverDto.current_thrower = None
                serverDto.throw_type = None
                serverDto.time_active = None
                channel = self.bot.get_channel(serverDto.channel_id)
                await channel.send("Ball is No Longer Active")
                ServerRepository.updateServer(serverDto)

    @commands.hybrid_command(name="throw", with_app_command=True)
    async def throw(self, ctx: commands.Context, points, throw_type):
        """throws the ball (usage: /throw <0-500> <ALIVE, DEAD>)"""

        with sqlite3.connect('500.db') as conn:
            cursor = conn.cursor()
            throw_type = throw_type.upper()
            if throw_type not in self.throw_types:
                await ctx.send(f'{throw_type} is not a valid Throw Type')
                return

            # keep the ball alive for 300 seconds or 20 seconds if dead
            print(throw_type)
            time_active = 300 if throw_type == 'ALIVE' else 20

            # get server
            guild_id = ctx.author.guild.id
            channel_id = ctx.channel.id
            player_id = ctx.author.id
            ball_status = 'INACTIVE'
            current_game = ServerRepository.getServerInfo(guild_id)

            if not current_game:
                ServerRepository.insertServer(
                    ServerDto(guild_id, channel_id, ball_status, points, throw_type, datetime.now(), player_id), cursor)
                current_game = ServerDto(guild_id, channel_id, ball_status, points, throw_type, datetime.now(), player_id)

            # print(current_game.guild_id)
            # print(current_game.ball_status)
            # print(current_game.ball_value)
            # print(current_game.current_thrower)

            if current_game.ball_status == 'ACTIVE':
                await ctx.send(f'Ball is currently active!')
                return

            if current_game.current_thrower != ctx.author.id and current_game.current_thrower is not None:
                await ctx.send(f'Your not the active thrower!')
                return

            if not points or not points.isnumeric() or int(points) < 0 or int(points) > 500:
                await ctx.send(f'{points} is not a number under 500!')
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

        with sqlite3.connect('500.db') as conn:
            cursor = conn.cursor()
            # get server
            guild_id = ctx.author.guild.id
            current_player_id = ctx.author.id
            channel_id = ctx.channel.id

            # get current game
            server = ServerRepository.getServerInfo(guild_id)
            if not server:
                await ctx.send(f"No active ball to throw!")
                return

            current_game = server

            if current_game.ball_status == 'INACTIVE':
                await ctx.send(f'No active ball to throw!')
                return

            if current_game.current_thrower == ctx.author.id and ctx.author.nick != 'Jon':
                await ctx.send(f'You\'re the active thrower!')
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
