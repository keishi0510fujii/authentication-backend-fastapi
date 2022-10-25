from rdb.migrations.migrator import Migrator
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor


class CreateAccountsTable(Migrator):
    __connection: Connection

    def __init__(self, conn: Connection):
        self.__connection = conn

    async def up(self):
        cursor: Cursor = await self.__connection.cursor()
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
        id VARCHAR(26) PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        hashed_password VARCHAR(255),
        activate TINYINT UNSIGNED,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
        """)
        await cursor.close()
        self.__connection.close()

    async def down(self):
        cursor: Cursor = await self.__connection.cursor()
        await cursor.execute("""
        DROP TABLE IF EXISTS accounts
        """)
        await cursor.close()
        self.__connection.close()
