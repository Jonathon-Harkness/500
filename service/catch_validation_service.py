from constants import BallStatus
from datetime import datetime

class CatchValidationService:

    @staticmethod
    def checkServerExists(server):
        if not server:
            raise Exception("No active ball to throw!")

    @staticmethod
    def checkBallActive(ball_status):
        if ball_status == BallStatus.INACTIVE:
            raise Exception("No active ball to throw!")

    @staticmethod
    def checkActiveThrower(current_thrower, current_user):
        if current_thrower == current_user.id and current_user.nick != 'Jon':
            raise Exception("You\'re the active thrower!")

    @staticmethod
    def checkDeadBallRetrievalPossible(throw_type: str, time_active):
        pass


