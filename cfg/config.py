from os import getenv
from dotenv import load_dotenv

load_dotenv()


class LocalMachineConfig:
    SQLALCHEMY_DATABASE_URI = getenv("LOCAL_DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class GcpConfig:
    SQLALCHEMY_DATABASE_URI = getenv("CLOUD_SQL_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
