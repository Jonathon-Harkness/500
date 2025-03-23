import sqlite3
from dto.server_dto import ServerDto

conn = sqlite3.connect('500.db')
c = conn.cursor()


class ServerRepository:

    @staticmethod
    def getAllServersWithExpiredActiveTime():
        servers = c.execute(f"SELECT * FROM SERVER WHERE TIME_ACTIVE <= CURRENT_TIMESTAMP")
        return servers.fetchall()

    @staticmethod
    def getServerInfo(guild_id):
        game = c.execute(f"SELECT * FROM SERVER WHERE GUILD_ID={guild_id}")
        maybeGame = game.fetchone()
        return ServerDto(*maybeGame) if maybeGame else None

    @staticmethod
    def insertServer(server: ServerDto, cursor):
        cursor.execute("INSERT INTO SERVER (GUILD_ID, CHANNEL_ID, BALL_STATUS, BALL_VALUE, THROW_TYPE, TIME_ACTIVE, CURRENT_THROWER)"
                  "VALUES (?, ?, ?, ?, ?, ?, ?)", (server.guild_id,
                                                server.channel_id,
                                                server.ball_status,
                                                server.ball_value,
                                                server.throw_type,
                                                server.time_active,
                                                server.current_thrower))
        return

    @staticmethod
    def updateServer(server: ServerDto, cursor):
        cursor.execute(f"UPDATE SERVER "
                  f"SET BALL_STATUS=?, BALL_VALUE=?, THROW_TYPE=?, TIME_ACTIVE=?, CURRENT_THROWER=? "
                  f"WHERE GUILD_ID=?", (server.ball_status,
                                        server.ball_value,
                                        server.throw_type,
                                        server.time_active,
                                        server.current_thrower,
                                        server.guild_id))
        return
