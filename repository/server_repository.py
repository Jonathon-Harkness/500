import sqlite3
from dto.server_dto import ServerDto

conn = sqlite3.connect('500.db')
c = conn.cursor()


class ServerRepository:

    @staticmethod
    def getServerInfo(guild_id):
        game = c.execute(f"SELECT * FROM SERVER WHERE GUILD_ID={guild_id}")
        maybeGame = game.fetchone()
        return ServerDto(*maybeGame) if maybeGame else None

    @staticmethod
    def insertServer(server: ServerDto):
        c.execute("INSERT INTO SERVER (GUILD_ID, BALL_STATUS, BALL_VALUE, THROW_TYPE, TIME_ACTIVE, CURRENT_THROWER)"
                  "VALUES (?, ?, ?, ?, ?, ?)",
                  (server.guild_id, server.ball_status, server.ball_value, server.throw_type, server.time_active,
                   server.current_thrower))
        conn.commit()
        return

    @staticmethod
    def updateServer(server: ServerDto):
        c.execute(f"UPDATE SERVER "
                  f"SET BALL_STATUS=?, "
                  f"BALL_VALUE=?, "
                  f"THROW_TYPE=?, "
                  f"TIME_ACTIVE=?, "
                  f"CURRENT_THROWER=? "
                  f"WHERE GUILD_ID=?", (server.ball_status, server.ball_value, server.throw_type, server.time_active, server.current_thrower, server.guild_id))
        conn.commit()
        return
