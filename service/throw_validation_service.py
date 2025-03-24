from constants import BallStatus, THROW_MIN, THROW_MAX


class ThrowValidationService:

    @staticmethod
    def checkBallActive(ball_status: str):
        if ball_status == BallStatus.ACTIVE:
            raise Exception("Ball is currently Active!")

    @staticmethod
    def checkActiveThrower(current_thrower, current_user):
        if current_thrower != current_user and current_thrower is not None:
            raise Exception("You're not the active thrower!")

    @staticmethod
    def checkValidPointInput(points):
        if not points or not points.isnumeric() or int(points) < THROW_MIN or int(points) > THROW_MAX:
            raise Exception(f"{points} must be between -2000 and 500")