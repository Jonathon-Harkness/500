from db import cursor as c, db


def run():
    c.execute("CREATE TABLE IF NOT EXISTS SERVER "
              "(GUILD_ID VARCHAR(100), "
              "CHANNEL_ID VARCHAR(100), "
              "BALL_STATUS TEXT, "
              "BALL_VALUE INTEGER, "
              "THROW_TYPE TEXT, "
              "THROW_TYPE_CHECK INTEGER DEFAULT 0, "
              "TIME_ACTIVE DATETIME, "
              "CURRENT_THROWER VARCHAR(100), "
              "SPECIAL_EFFECT TEXT DEFAULT NULL, "
              "PRIMARY KEY (GUILD_ID, CHANNEL_ID))")
    c.execute("CREATE TABLE IF NOT EXISTS PLAYER "
              "(GUILD_ID VARCHAR(100), "
              "CHANNEL_ID VARCHAR(100), "
              "PLAYER_ID VARCHAR(100), "
              "POINTS INTEGER, "
              "STATUS_EFFECT TEXT, "
              "USERNAME TEXT, "
              "NICKNAME TEXT, "
              "PRIMARY KEY (GUILD_ID, PLAYER_ID, CHANNEL_ID))")
    c.execute("CREATE TABLE IF NOT EXISTS SPECIAL_THROW "
              "(SPECIAL_THROW VARCHAR(100) PRIMARY KEY, "
              "SPECIAL_THROW_DESCRIPTION TEXT, "
              "POINTS_REQUIRED INTEGER DEFAULT 0)")
    c.execute("INSERT IGNORE INTO SPECIAL_THROW (SPECIAL_THROW, SPECIAL_THROW_DESCRIPTION) "
              "VALUES (%s, %s)",
              ("CHERRY_BOMB", "player who catches will have their point total set to zero"))
    c.execute("INSERT IGNORE INTO SPECIAL_THROW (SPECIAL_THROW, SPECIAL_THROW_DESCRIPTION, POINTS_REQUIRED)"
              "VALUES (%s, %s, %s)",
              ("STINKY_GLUE", "player will be crazy smelly. This might distract other players", 1))
    c.execute("INSERT IGNORE INTO SPECIAL_THROW (SPECIAL_THROW, SPECIAL_THROW_DESCRIPTION, POINTS_REQUIRED)"
              "VALUES (%s, %s, %s)",
              ("STICKY_GLUE", "player will be sticky. They won't be able to catch the ball next round", 1))
    db.commit()
