class Server:

    def __init__(self, guild_id, ball_status, ball_value, throw_type, time_active, current_thrower):
        self.guild_id = guild_id
        self.ball_status = ball_status
        self.ball_value = ball_value
        self.throw_type = throw_type
        self.time_active = time_active
        self.current_thrower = current_thrower
