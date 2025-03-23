import sqlite3
from dto.server_dto import Server

conn = sqlite3.connect('500.db')
c = conn.cursor()


class ServerRepository:

    @staticmethod
    def getServerInfo(guild_id, ball_status, ball_value, throw_type, time_active, player_id):
        game = c.execute(f"SELECT * FROM SERVER WHERE GUILD_ID={guild_id}")
        maybeGame = game.fetchone()
        if not maybeGame:
            current_game = Server(guild_id, ball_status, ball_value, throw_type, time_active, player_id)
            ServerRepository.insertNewGame(current_game)
        else:
            current_game = Server(*maybeGame)
        return current_game

    @staticmethod
    def insertNewGame(server: Server):
        c.execute("INSERT INTO SERVER (GUILD_ID, BALL_STATUS, BALL_VALUE, THROW_TYPE, TIME_ACTIVE, CURRENT_THROWER)"
                  "VALUES (?, ?, ?, ?, ?, ?)",
                  (server.guild_id, server.ball_status, server.ball_value, server.throw_type, server.time_active,
                   server.current_thrower))
        conn.commit()
        return

    @staticmethod
    def updateGame(server: Server):
        c.execute(f"UPDATE SERVER "
                  f"SET BALL_STATUS='{server.ball_status}', "
                  f"BALL_VALUE='{server.ball_value}', "
                  f"THROW_TYPE='{server.throw_type}', "
                  f"TIME_ACTIVE='{server.time_active}', "
                  f"CURRENT_THROWER='{server.current_thrower}' "
                  f"WHERE GUILD_ID='{server.guild_id}'")
        conn.commit()
        return
