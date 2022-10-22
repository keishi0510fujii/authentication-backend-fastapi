import abc

import aiomysql
from aiomysql import Connection
import asyncio

DATABASE = 'sample-authentication'
HOST = 'test-rdb'
USER = 'testuser'
PASSWORD = 'testsecret'
PORT = 3306

loop = asyncio.get_event_loop()


async def get_connection() -> Connection:
    return await aiomysql.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        db=DATABASE,
        loop=loop
    )


#   データ生成用クラス
class RdbTestDataFactory(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    async def make(num: int):
        pass


#   データ更新用クラス
class RdbTestTablePersist(metaclass=abc.ABCMeta):

    #   DBへデータを挿入
    @staticmethod
    @abc.abstractmethod
    async def save_by_dto_list(dto_list):
        pass

    #   DBのデータを削除
    @staticmethod
    @abc.abstractmethod
    async def delete_by_dto_list(dto_list):
        pass


#   データ参照用クラス
class RdbTestTableQuery(metaclass=abc.ABCMeta):

    #   DBのデータを取得
    @staticmethod
    @abc.abstractmethod
    async def find_by_unique_value(unique_value: str):
        pass
