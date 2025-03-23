import sqlite3
from dto import PlayerDto

conn = sqlite3.connect('500.db')
c = conn.cursor()


class PlayerRepository:

    @staticmethod
    def getSinglePlayerInfo():
        pass

    @staticmethod
    def getAllPlayersFromServer(guild_id):
        query = c.execute(f"SELECT * FROM PLAYER WHERE GUILD_ID={guild_id}")
        players_tuple = query.fetchall()
        return players_tuple

    @staticmethod
    def insertPlayer(guild_id, current_player_id, username, nickname, points=0, status_effect=None):
        c.execute("INSERT INTO PLAYER (GUILD_ID, PLAYER_ID, POINTS, STATUS_EFFECT, USERNAME, NICKNAME)"
                  "VALUES (?, ?, ?, ?, ?, ?)",
                  (guild_id, current_player_id, points, status_effect, username, nickname))
        conn.commit()
        return

    @staticmethod
    def updatePlayer(player: PlayerDto):
        c.execute(f"UPDATE PLAYER "
                  f"SET POINTS='{player.points}', NICKNAME='{player.nickname}', STATUS_EFFECT=NULL "
                  f"WHERE GUILD_ID='{player.guild_id}' AND PLAYER_ID='{player.player_id}'")
        conn.commit()
        return

    @staticmethod
    def resetAllPlayerPointsFromServer(guild_id):
        c.execute(f"UPDATE PLAYER "
                  f"SET POINTS='{0}'"
                  f"WHERE GUILD_ID='{guild_id}'")
        conn.commit()
        return
