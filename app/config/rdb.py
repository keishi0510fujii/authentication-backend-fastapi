import asyncio
import aiomysql
from aiomysql.connection import Connection

DATABASE = 'sample-authentication'
HOST = 'rdb'
USER = 'devuser'
PASSWORD = 'devsecret'
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


async def close_connection():
    conn: Connection = await get_connection()
    conn.close()
