from rdb.migrations.migrator import Migrator
from aiomysql.sa.connection import SAConnection


class CreateAccountsTable(Migrator):
    __connection: SAConnection

    def __init__(self, conn: SAConnection):
        self.__connection = conn

    async def up(self):
        await self.__connection.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
        id VARCHAR(26) PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        hashed_password VARCHAR(255),
        activate TINYINT UNSIGNED,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
        """)

    async def down(self):
        await self.__connection.execute("""
        DROP TABLE IF EXISTS accounts
        """)
