import asyncio
from aiomysql.sa.engine import Engine
from aiomysql.sa import create_engine
from aiomysql.sa.connection import SAConnection


class MysqlConfig:
    __engine: Engine
    __connection: SAConnection

    async def connect(self):
        self.__engine = await create_engine(
            user='testuser',
            password='testsecret',
            host='test-rdb',
            port=3306,
            db='sample-authentication',
        )
        self.__connection = await self.__engine.acquire()

    def get_connection(self) -> SAConnection:
        return self.__connection

    def close(self):
        asyncio.run(self.__connection.close())
        asyncio.run(self.__engine.close())
