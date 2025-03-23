import sqlite3
from dto import PlayerDto

conn = sqlite3.connect('500.db')
c = conn.cursor()


class PlayerRepository:

    @staticmethod
    def getSinglePlayerInfo():
        pass

    @staticmethod
    def getAllPlayersFromServer(guild_id, cursor):
        query = cursor.execute(f"SELECT * FROM PLAYER WHERE GUILD_ID={guild_id}")
        players_tuple = query.fetchall()
        return players_tuple

    @staticmethod
    def insertPlayer(guild_id, channel_id, current_player_id, username, nickname, cursor, points=0, status_effect=None):
        cursor.execute("INSERT INTO PLAYER (GUILD_ID, CHANNEL_ID, PLAYER_ID, POINTS, STATUS_EFFECT, USERNAME, NICKNAME)"
                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (guild_id, channel_id, current_player_id, points, status_effect, username, nickname))

    @staticmethod
    def updatePlayer(player: PlayerDto, cursor):
        cursor.execute(f"UPDATE PLAYER "
                       f"SET POINTS='{player.points}', NICKNAME='{player.nickname}', STATUS_EFFECT=NULL "
                       f"WHERE GUILD_ID='{player.guild_id}' AND PLAYER_ID='{player.player_id}'")

    @staticmethod
    def resetAllPlayerPointsFromServer(guild_id, cursor):
        cursor.execute(f"UPDATE PLAYER "
                       f"SET POINTS={0} "
                       f"WHERE GUILD_ID='{guild_id}'")
