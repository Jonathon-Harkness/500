import sqlite3
from player import Player
from game import Game

conn = sqlite3.connect('500.db')
c = conn.cursor()


class Repository:

    @staticmethod
    def getServerInfo(guild_id, ball_status, ball_value, throw_type, time_active, player_id):
        game = c.execute(f"SELECT * FROM SERVER WHERE GUILD_ID={guild_id}")
        maybeGame = game.fetchone()
        if not maybeGame:
            current_game = Game(guild_id, ball_status, ball_value, throw_type, time_active, player_id)
            Repository.insertNewGame(current_game)
        else:
            current_game = Game(*maybeGame)
        return current_game

    def getPlayerServerInfo(self):
        pass

    @staticmethod
    def insertNewGame(game: Game):
        c.execute("INSERT INTO SERVER (GUILD_ID, BALL_STATUS, BALL_VALUE, THROW_TYPE, TIME_ACTIVE, CURRENT_THROWER)"
                  "VALUES (?, ?, ?, ?, ?, ?)",
                  (game.guild_id, game.ball_status, game.ball_value, game.throw_type, game.time_active,
                   game.current_thrower))
        conn.commit()
        return

    def insertNewPlayer(self):
        return

    @staticmethod
    def updateGame(game: Game):
        c.execute(f"UPDATE SERVER "
                  f"SET BALL_STATUS='{game.ball_status}', "
                  f"BALL_VALUE='{game.ball_value}', "
                  f"THROW_TYPE='{game.throw_type}', "
                  f"TIME_ACTIVE='{game.time_active}', "
                  f"CURRENT_THROWER='{game.current_thrower}' "
                  f"WHERE GUILD_ID='{game.guild_id}'")
        conn.commit()
        return

    def updatePlayer(self):
        pass
