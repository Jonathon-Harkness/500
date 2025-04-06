from dto.server_dto import ServerDto


class ServerRepository:

    @staticmethod
    def getAllServersWithExpiredActiveTimeAlive(cursor):
        cursor.execute(f"SELECT * FROM SERVER "
                       f"WHERE TIME_ACTIVE <= CURRENT_TIMESTAMP "
                       f"AND TIME_ACTIVE IS NOT NULL "
                       f"AND THROW_TYPE='ALIVE' ")
        servers = cursor.fetchall()
        return servers

    @staticmethod
    def getAllServersWithExpiredActiveTimeDead(cursor):
        cursor.execute(f"SELECT * FROM SERVER "
                       f"WHERE TIME_ACTIVE <= CURRENT_TIMESTAMP "
                       f"AND TIME_ACTIVE IS NOT NULL "
                       f"AND THROW_TYPE='DEAD' "
                       f"AND THROW_TYPE_CHECK=0 ")
        servers = cursor.fetchall()
        return servers

    @staticmethod
    def getServerInfo(guild_id, channel_id, cursor):
        cursor.execute("SELECT * FROM SERVER WHERE GUILD_ID=%s AND CHANNEL_ID=%s", (guild_id, channel_id))
        maybeGame = cursor.fetchone()
        return ServerDto(*maybeGame) if maybeGame else None

    @staticmethod
    def insertServer(server: ServerDto, cursor):
        cursor.execute(
            "INSERT INTO SERVER (GUILD_ID, CHANNEL_ID, BALL_STATUS, BALL_VALUE, THROW_TYPE, TIME_ACTIVE, CURRENT_THROWER, SPECIAL_EFFECT)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (server.guild_id,
                                                        server.channel_id,
                                                        server.ball_status,
                                                        server.ball_value,
                                                        server.throw_type,
                                                        server.time_active,
                                                        server.current_thrower,
                                                        server.special_effect))

    @staticmethod
    def updateServer(server: ServerDto, cursor):
        cursor.execute(f"UPDATE SERVER "
                       f"SET BALL_STATUS=%s, BALL_VALUE=%s, THROW_TYPE=%s, THROW_TYPE_CHECK=%s, TIME_ACTIVE=%s, CURRENT_THROWER=%s, SPECIAL_EFFECT=%s "
                       f"WHERE GUILD_ID=%s", (server.ball_status,
                                              server.ball_value,
                                              server.throw_type,
                                              server.throw_type_check,
                                              server.time_active,
                                              server.current_thrower,
                                              server.special_effect,
                                              server.guild_id))
