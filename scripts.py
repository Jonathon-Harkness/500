import sqlite3


def run():
    conn = sqlite3.connect('500.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS SERVER "
              "(GUILD_ID INTEGER, "
              "CHANNEL_ID INTEGER, "
              "BALL_STATUS TEXT, "
              "BALL_VALUE INTEGER, "
              "THROW_TYPE TEXT, "
              "THROW_TYPE_CHECK INTEGER DEFAULT 0, "
              "TIME_ACTIVE DATETIME, "
              "CURRENT_THROWER INTEGER, "
              "SPECIAL_EFFECT TEXT DEFAULT NULL, "
              "PRIMARY KEY (GUILD_ID, CHANNEL_ID))")
    c.execute("CREATE TABLE IF NOT EXISTS PLAYER "
              "(GUILD_ID INTEGER, "
              "CHANNEL_ID INTEGER, "
              "PLAYER_ID INTEGER, "
              "POINTS INTEGER, "
              "STATUS_EFFECT TEXT, "
              "USERNAME TEXT, "
              "NICKNAME TEXT, "
              "PRIMARY KEY (GUILD_ID, PLAYER_ID, CHANNEL_ID))")
    c.execute("CREATE TABLE IF NOT EXISTS SPECIAL_THROW "
              "(SPECIAL_THROW TEXT PRIMARY KEY, "
              "SPECIAL_THROW_DESCRIPTION TEXT, "
              "POINTS_REQUIRED INTEGER DEFAULT 0)")
    c.execute("INSERT OR IGNORE INTO SPECIAL_THROW (SPECIAL_THROW, SPECIAL_THROW_DESCRIPTION)"
              "VALUES (?, ?)",
              ("CHERRY_BOMB", "player who catches will have their point total set to zero"))
    c.execute("INSERT OR IGNORE INTO SPECIAL_THROW (SPECIAL_THROW, SPECIAL_THROW_DESCRIPTION, POINTS_REQUIRED)"
              "VALUES (?, ?, ?)",
              ("STINKY_GLUE", "player will be crazy smelly. This might distract other players", 1))
    c.execute("INSERT OR IGNORE INTO SPECIAL_THROW (SPECIAL_THROW, SPECIAL_THROW_DESCRIPTION, POINTS_REQUIRED)"
              "VALUES (?, ?, ?)",
              ("STICKY_GLUE", "player will be sticky. They won't be able to catch the ball next round", 1))
    conn.commit()
