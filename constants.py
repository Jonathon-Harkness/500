from enum import Enum

TOKEN = "TOKEN"
THROW_MIN = -500
THROW_MAX = 500
THROW_TYPE = {'ALIVE', 'DEAD'}
SPECIAL_THROWS = {'CHERRY BOMB'}


class SpecialThrows(Enum):
    CHERRY_BOMB = 'CHERRY BOMB'


class BallStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


