from sqlalchemy import create_engine
from config_reader import config

user = config.user.get_secret_value()
host = config.host.get_secret_value()
password = config.password.get_secret_value()
port = config.port.get_secret_value()
database = config.database.get_secret_value()


def get_connection():
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
