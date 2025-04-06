import sqlite3
from dto import PlayerDto

conn = sqlite3.connect('500.db')
c = conn.cursor()


class PlayerRepository:

    @staticmethod
    def getSinglePlayerInfo():
        pass

    @staticmethod
    def getAllPlayersFromServer(guild_id, channel_id, cursor):
        cursor.execute("SELECT * FROM PLAYER "
                       "WHERE GUILD_ID=%s "
                       "AND CHANNEL_ID=%s ",
                       (guild_id, channel_id))
        players_tuple = cursor.fetchall()
        return players_tuple

    @staticmethod
    def insertPlayer(guild_id, channel_id, current_player_id, username, nickname, cursor, points=0, status_effect=None):
        cursor.execute("INSERT INTO PLAYER (GUILD_ID, CHANNEL_ID, PLAYER_ID, POINTS, STATUS_EFFECT, USERNAME, NICKNAME)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (guild_id, channel_id, current_player_id, points, status_effect, username, nickname))

    @staticmethod
    def updatePlayer(player: PlayerDto, cursor):
        cursor.execute(f"UPDATE PLAYER "
                       f"SET POINTS=%s, NICKNAME=%s, STATUS_EFFECT=%s "
                       f"WHERE GUILD_ID=%s AND PLAYER_ID=%s",
                       (player.points, player.nickname, player.status_effect, player.guild_id, player.player_id))

    @staticmethod
    def updatePlayerStatusToNull(guild_id, channel_id, cursor):
        cursor.execute(f"UPDATE PLAYER "
                       f"SET STATUS_EFFECT=NULL "
                       f"WHERE GUILD_ID='{guild_id}' "
                       f"AND CHANNEL_ID='{channel_id}' ")

    @staticmethod
    def resetAllPlayerPointsFromServer(guild_id, channel_id, cursor):
        cursor.execute(f"UPDATE PLAYER "
                       f"SET POINTS={0} "
                       f"WHERE GUILD_ID='{guild_id}' "
                       f"AND CHANNEL_ID='{channel_id}' ")
