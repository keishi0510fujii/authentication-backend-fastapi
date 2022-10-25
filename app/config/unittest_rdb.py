import asyncio
import aiomysql
from aiomysql.connection import Connection
from aiomysql.sa.engine import Engine
from aiomysql.sa import create_engine
from aiomysql.sa.connection import SAConnection


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
