import mysql.connector

import constants

if constants.env == 'prod':
    db_host = constants.db_host_prod
    db_username = constants.db_username_prod
    db_password = constants.db_password_prod
else:
    db_host = constants.db_host_dev
    db_username = constants.db_username_dev
    db_password = constants.db_password_dev

db = mysql.connector.connect(
    host=db_host,
    user=db_username,
    password=db_password,
    database="500"
)
cursor = db.cursor(buffered=True)
