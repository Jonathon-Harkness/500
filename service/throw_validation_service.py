from constants import BallStatus, THROW_MIN, THROW_MAX, SPECIAL_THROWS, SpecialThrows
from dto import SpecialEffectDto
from util import is_integer


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
        if not points or not is_integer(points) or int(points) < THROW_MIN or int(points) > THROW_MAX:
            raise Exception(f"{points} must be an integer between -500 and 500")

    @staticmethod
    def checkIfSpecialThrowRequiresPoints(special_effect: SpecialEffectDto, points: int):
        if special_effect.points_required:
            if not points:
                raise Exception(f"{ special_effect.name } requires you to input points!")
            ThrowValidationService.checkValidPointInput(points)

