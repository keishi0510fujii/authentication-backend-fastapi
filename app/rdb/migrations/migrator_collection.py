from typing import List
from rdb.migrations.migrator import Migrator
import warnings


class MigratorCollection:
    __migrator_list: List[Migrator] = []

    def __init__(self, migrator_list: List[Migrator]):
        self.__migrator_list.extend(migrator_list)

    async def up(self):
        warnings.filterwarnings('ignore', module=r"aiomysql")
        for migrator in self.__migrator_list:
            print("################## start  up:", migrator.__class__)
            await migrator.up()
            print("################## finish up:", migrator.__class__)

    async def down(self):
        warnings.filterwarnings('ignore', module=r"aiomysql")
        for migrator in reversed(self.__migrator_list):
            print("################## start  down:", migrator.__class__)
            await migrator.down()
            print("################## finish down:", migrator.__class__)
