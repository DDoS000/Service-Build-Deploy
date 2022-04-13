import databases
import sqlalchemy
from config import cfg
from models import metadata


def database_pgsql_url_config():
    return str(cfg.DB_CONNECTION + "://" + cfg.DB_USERNAME + ":" + cfg.DB_PASSWORD +
               "@" + cfg.DB_HOST + ":" + cfg.DB_PORT + "/" + cfg.DB_DATABASE)

database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
metadata.create_all(engine)