import aiomysql
from domain.account.repository import AccountRepository
from domain.account.model import Account
from pypika import Table, MySQLQuery
from aiomysql import Connection, Cursor
from typing import List
from infrastructure.mysql.base import AttrDict


class AccountsTableRecord(aiomysql.DictCursor):
    id: str
    email: str
    hashed_password: str
    activate: int
    #   object.{key_name}で推論が聞くように、dict_typeを変更している
    dict_type = AttrDict


class AccountRepositoryMysql(AccountRepository):
    __table: Table
    __connection: Connection

    def __init__(self, conn: Connection):
        self.__table = Table('accounts')
        self.__connection = conn

    async def find_all(self) -> List[Account]:
        query = (
            MySQLQuery
            .from_(self.__table)
            .select('id', 'email', 'hashed_password', 'activate')
        )
        cursor: Cursor = await self.__connection.cursor(AccountsTableRecord)
        await cursor.execute(str(query))
        query_result: List[AccountsTableRecord] = await cursor.fetchall()
        await cursor.close()
        self.__connection.close()
        return [self.__convert_to_entity(record) for record in query_result]

    async def find_by_email(self, email: str) -> Account:
        query = (
            MySQLQuery
            .from_(self.__table)
            .select('id', 'email', 'hashed_password', 'activate')
            .where(self.__table.email == email)
        )
        cursor: Cursor = await self.__connection.cursor(AccountsTableRecord)
        await cursor.execute(str(query))
        record = await cursor.fetchone()
        await cursor.close()
        self.__connection.close()
        return self.__convert_to_entity(record)

    async def save(self, account: Account):
        cursor: Cursor = await self.__connection.cursor()
        await self.__connection.begin()
        try:
            command = self.__convert_to_insert_command(account)
            await cursor.execute(command)
            await self.__connection.commit()
        except:
            await self.__connection.rollback()
            raise Exception('error save account')
        finally:
            await cursor.close()
            self.__connection.close()

    async def update(self, account: Account):
        cursor: Cursor = await self.__connection.cursor()
        await self.__connection.begin()
        try:
            command = self.__convert_to_update_command(account)
            await cursor.execute(command)
            await self.__connection.commit()

        except:
            await self.__connection.rollback()
            raise Exception('error update account')
        finally:
            await cursor.close()
            self.__connection.close()

    def __convert_to_insert_command(self, account: Account) -> str:
        account_id, email, hashed_password, activate = account.serialize()
        query = (
            MySQLQuery
            .into(self.__table)
            .columns('id', 'email', 'hashed_password', 'activate')
            .insert(account_id, email, hashed_password, int(activate))
        )

        return str(query)

    def __convert_to_update_command(self, account: Account) -> str:
        account_id, mail_address, hashed_password, activate = account.serialize()
        query = (
            MySQLQuery
            .update(self.__table)
            .set(self.__table.email, mail_address)
            .set(self.__table.hashed_password, hashed_password)
            .set(self.__table.activate, int(activate))
            .where(self.__table.id == account_id))

        return str(query)

    @staticmethod
    def __convert_to_entity(record: AccountsTableRecord) -> Account:
        return Account.restore(
            record.id,
            record.email,
            record.hashed_password,
            bool(record.activate),
        )
