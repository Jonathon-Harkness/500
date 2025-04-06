from enum import Enum

env = "prod"

db_host_dev = "devHost"
db_username_dev = "user"
db_password_dev = "pass"
db_port_dev = 0000

db_host_prod = "prodHost"
db_username_prod = "user"
db_password_prod = "pass"
db_port_prod = 0000


TOKEN = "TOKEN"
THROW_MIN = -500
THROW_MAX = 500
THROW_TYPE = {'ALIVE', 'DEAD'}


class BallStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


