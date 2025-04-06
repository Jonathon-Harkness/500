from constants import BallStatus


class CatchValidationService:

    @staticmethod
    def checkServerExists(server):
        if not server:
            raise Exception("No active ball to throw!")

    @staticmethod
    def checkBallActive(ball_status):
        if ball_status == BallStatus.INACTIVE.value:
            raise Exception("No active ball to throw!")

    @staticmethod
    def checkActiveThrower(current_thrower, current_user):
        if current_thrower == current_user.id:
            raise Exception("You\'re the active thrower!")



