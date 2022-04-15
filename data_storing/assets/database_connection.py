import os
from data_storing.assets.base import Base as assets_base
from sqlalchemy import create_engine
from utilities import log
from utilities.log import root_folder_all_code

# INSTALL https://sqlitebrowser.org/dl/
# sudo apt-get install sqlitebrowser
dir_path = os.path.dirname(os.path.realpath(__file__))

db_directory = "db"
name_database_file = "assets.sqlite"
dir_root = dir_path.split(root_folder_all_code, 1)[0]
db_path = os.path.join(dir_root, root_folder_all_code, db_directory)
db_file_path = os.path.join(db_path, name_database_file)

# Global Variables
SQLITE = 'sqlite'
DB_ENGINE: str = f'sqlite:///{db_file_path}'
db_engine = create_engine(DB_ENGINE,
                          connect_args={'check_same_thread': False})


class Connection:
    def __init__(self):
        log.info(db_engine)

    def generate_assets_db_from_scratch(self):
        try:
            assets_base.metadata.create_all(db_engine)
            log.info("Assets tables created")
        except Exception as e:
            log.error("Error occurred during Table creation!")
            log.error(e)

db_assets = Connection()
# Create Tables
db_assets.generate_assets_db_from_scratch()

