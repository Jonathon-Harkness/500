class PlayerDto:

    def __init__(self, guild_id, channel_id, player_id, points, status_effect, username="", nickname=""):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.player_id = player_id
        self.points = points
        self.status_effect = status_effect
        self.username = username
        self.nickname = nickname