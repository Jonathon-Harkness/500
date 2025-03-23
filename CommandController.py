import discord
from datetime import datetime, timedelta
from discord.ext import commands
import sqlite3
from game import Game
from player import Player
from repository import ServerRepository

conn = sqlite3.connect('500.db')
c = conn.cursor()


class FiveHundred(commands.Cog):
    BALL_STATUS = {'ACTIVE', 'INACTIVE'}
    THROW_TYPE = {'ALIVE', 'DEAD'}

    def __init__(self, bot):
        self.bot = bot
        self.throw_types = {'ALIVE', 'DEAD'}

    @commands.hybrid_command(name="throw", with_app_command=True)
    async def throw(self, ctx, points, throw_type):
        """throws the ball (usage: /throw <0-500> <ALIVE, DEAD>)"""

        throw_type = throw_type.upper()
        if throw_type not in self.throw_types:
            await ctx.send(f'{throw_type} is not a valid Throw Type')
            return

        # keep the ball alive for 300 seconds or 20 seconds if dead
        time_active = 300 if throw_type == 'ALIVE' else 20

        insert = False
        # get server
        guild_id = ctx.author.guild.id
        player_id = ctx.author.id
        ball_status = 'INACTIVE'
        current_game = ServerRepository.getServerInfo(guild_id, ball_status, 0, throw_type, time_active, player_id)

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
        current_game.time_active = datetime.now() + timedelta(seconds=time_active)

        # update game
        ServerRepository.updateGame(current_game)

        throw_type_message = f"You have {time_active / 60} minutes to catch it!" if throw_type == 'ALIVE' else f"You must wait {time_active / 60} minutes before catching it"
        await ctx.send(f'{ctx.author.nick} threw the ball for {points} points {throw_type}! {throw_type_message}')

    @commands.hybrid_command(name="catch", with_app_command=True)
    async def catch(self, ctx):
        """catch the ball"""

        # get server
        guild_id = ctx.author.guild.id
        current_player_id = ctx.author.id

        # get current game
        game = c.execute(f"SELECT * FROM SERVER WHERE GUILD_ID={guild_id}")
        maybeGame = game.fetchone()
        if not maybeGame:
            await ctx.send(f"No active ball to throw!")
            return

        current_game = Game(*maybeGame)

        if current_game.ball_status == 'INACTIVE':
            await ctx.send(f'No active ball to throw!')
            return

        if current_game.current_thrower == ctx.author.id and ctx.author.nick != 'Jon':
            await ctx.send(f'You\'re the active thrower!')
            return

        # get players
        query = c.execute(f"SELECT * FROM PLAYER WHERE GUILD_ID={guild_id}")
        players_tuple = query.fetchall()
        players = {}
        for player in players_tuple:
            p = Player(*player)
            players[p.player_id] = p

        if current_player_id not in players:
            new_player = True
            current_player_points = current_game.ball_value
        else:
            new_player = False
            current_player_points = players[current_player_id].points + current_game.ball_value

        current_game.ball_status = 'INACTIVE'
        current_game.current_thrower = None

        if new_player is True:
            c.execute("INSERT INTO PLAYER (GUILD_ID, PLAYER_ID, POINTS, STATUS_EFFECT, USERNAME, NICKNAME)"
                      "VALUES (?, ?, ?, ?, ?, ?)", (guild_id, current_player_id, current_player_points, None, ctx.author.name, ctx.author.nick))
        else:
            c.execute(f"UPDATE PLAYER "
                      f"SET POINTS='{current_player_points}', NICKNAME='{ctx.author.nick}', STATUS_EFFECT=NULL "
                      f"WHERE GUILD_ID='{guild_id}' AND PLAYER_ID='{current_player_id}'")

        c.execute(f"UPDATE SERVER "
                  f"SET BALL_STATUS='{current_game.ball_status}', BALL_VALUE='{0}', CURRENT_THROWER=NULL "
                  f"WHERE GUILD_ID='{guild_id}'")

        await ctx.send(f'{ ctx.author.nick } captured the ball at { current_game.ball_value } points!')

        if current_player_points >= 500:
            c.execute(f"UPDATE PLAYER "
                      f"SET POINTS='{0}'"
                      f"WHERE GUILD_ID='{guild_id}'")
            await ctx.send(f'🎉 {ctx.author.nick} has won 500! 🎉')

        conn.commit()

    @commands.hybrid_command(name="leaderboard", with_app_command=True)
    async def leaderboard(self, ctx):
        """show current standings"""
        leaderboard = '----- LEADERBOARD -----\n'

        # get server
        guild_id = ctx.author.guild.id

        # get players
        query = c.execute(f"SELECT * FROM PLAYER WHERE GUILD_ID={guild_id}")
        players_tuple = query.fetchall()
        players = []
        for player in players_tuple:
            cur_player = Player(*player)
            players.append([cur_player.points, cur_player.nickname])

        players.sort(reverse=True)
        for player in players:
            leaderboard += f'**{player[1]}**: {player[0]}\n'

        await ctx.send(leaderboard)
