import asyncio
from aiomysql.sa import create_engine
from aiomysql.sa.engine import Engine
from aiomysql.sa.connection import SAConnection, Transaction
import pytest

DB_NAME_PREFIX = 'test-'

DATABASE = 'sample-authentication'
HOST = 'test-rdb'
USER = 'testuser'
PASSWORD = 'testsecret'
PORT = 3306


async def get_engine() -> Engine:
    return await create_engine(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        db=DATABASE
    )


async def get_connection() -> SAConnection:
    engine = await get_engine()
    return await engine.acquire()


async def execute_command(command: str):
    connection: SAConnection = await get_connection()
    transaction: Transaction = await connection.begin()
    await connection.execute(command)
    await transaction.commit()


async def execute_query(query: str):
    connection: SAConnection = await get_connection()
    return await connection.execute(query)


class MySqlUnitTestHelper:
    __db_name: str
    __engine: Engine
    __connection: SAConnection

    async def create_database(self, test_class_name: str):
        self.__db_name = DB_NAME_PREFIX + test_class_name
        self.__engine: Engine = await create_engine(
            user='root',
            password='root',
            host='test-rdb',
            port=3306,
        )
        self.__connection = await self.__engine.acquire()
        #   テストクラス毎にデータベースを作成
        await self.__connection.execute(f"CREATE DATABASE IF NOT EXISTS `{self.__db_name}`")
        await self.__connection.close()
        self.__engine.close()

    async def connect(self):
        self.__engine: Engine = await create_engine(
            user='testuser',
            password='testsecret',
            host='test-rdb',
            port=3306,
            db=self.__db_name
        )
        self.__connection = await self.__engine.acquire()

    async def close(self):
        await self.__connection.execute(f"DROP DATABASE {self.__db_name}")
        await self.__connection.close()
        await self.__engine.close()
