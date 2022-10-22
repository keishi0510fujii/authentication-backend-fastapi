from typing import List

import aiomysql
import ulid
from passlib.hash import pbkdf2_sha256
from tests.helper.infrastructure.rdb.base import RdbTestTablePersist, RdbTestTableQuery, RdbTestDataFactory, \
    get_connection
from aiomysql import Connection, Cursor


class AccountDto:
    id: str
    email: str
    hashed_password: str
    activate: int

    def __init__(self):
        self.id = ulid.new().str
        self.email = f"{ulid.new().str}@example.come"
        self.hashed_password = pbkdf2_sha256.hash("hogeH0G=")
        self.activate = 1


class AttrDict(dict):
    """Dict that can get attribute by dot, and doesn't raise KeyError"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None


class AttrDictCursor(aiomysql.DictCursor):
    dict_type = AttrDict


class AccountDtoListFactory(RdbTestDataFactory):
    @staticmethod
    async def make(num: int) -> List[AccountDto]:
        return [AccountDto() for i in range(num)]


class AccountsTablePersist(RdbTestTablePersist):

    @staticmethod
    async def save_by_dto_list(dto_list: List[AccountDto]):
        insert_values = (
            f"('{v.id}', '{v.email}', '{v.hashed_password}', '{v.activate}')" for v in dto_list
        )
        command_values = ", ".join(insert_values)
        command = f"INSERT INTO accounts (id, email, hashed_password, activate) VALUES {command_values}"
        conn: Connection = await get_connection()
        cursor: Cursor = await conn.cursor()
        await conn.begin()
        await cursor.execute(command)
        await conn.commit()
        await cursor.close()
        conn.close()

    @staticmethod
    async def delete_by_dto_list(dto_list: List[AccountDto]):
        #   delete文（command）を生成
        command_emails = (f"email='{r.email}'" for r in dto_list)
        where_statement = " OR ".join(command_emails)
        command = f"DELETE FROM accounts WHERE {where_statement}"
        #   DBに接続し、コマンドを実行
        conn: Connection = await get_connection()
        cursor: Cursor = await conn.cursor()
        await conn.begin()
        await cursor.execute(command)
        await conn.commit()
        #   DBを切断
        await cursor.close()
        conn.close()


class AccountsTableQuery(RdbTestTableQuery):
    @staticmethod
    async def find_by_unique_value(unique_value: str) -> AccountDto:
        conn: Connection = await get_connection()
        cursor: Cursor = await conn.cursor(AttrDictCursor)
        query = f"SELECT id, email, hashed_password, activate FROM accounts WHERE email='{unique_value}'"
        await cursor.execute(query)
        record: AccountDto = await cursor.fetchone()
        await cursor.close()
        conn.close()
        return record
