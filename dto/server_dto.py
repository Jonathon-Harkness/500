class ServerDto:

    def __init__(self, guild_id, channel_id, ball_status, ball_value, throw_type, throw_type_check, time_active, current_thrower, special_effect=None):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.ball_status = ball_status
        self.ball_value = ball_value
        self.throw_type = throw_type
        self.throw_type_check = throw_type_check
        self.time_active = time_active
        self.current_thrower = current_thrower
        self.special_effect = special_effect
