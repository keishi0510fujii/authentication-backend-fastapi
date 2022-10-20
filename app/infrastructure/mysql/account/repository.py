from domain.account.repository import AccountRepository
from domain.account.model import Account
from pypika import Table, MySQLQuery
from aiomysql.sa.connection import SAConnection
from typing import List


class AccountRepositoryMysql(AccountRepository):
    __table: Table
    __connection: SAConnection

    def __init__(self, conn: SAConnection):
        self.__table = Table('accounts')
        self.__connection = conn

    async def find_all(self) -> List[Account]:
        query = (MySQLQuery
                 .from_(self.__table)
                 .select('id', 'email', 'hashed_password', 'activate')
                 )
        query_result = await self.__connection.execute(str(query))
        return [self.__convert_to_entity(record) for record in await query_result.fetchall()]

    async def find_by_email(self, email: str) -> Account:
        query = (MySQLQuery
                 .from_(self.__table)
                 .select('id', 'email', 'hashed_password', 'activate')
                 .where(self.__table.email == email)
                 )
        query_result = await self.__connection.execute(str(query))
        record = await query_result.first()
        return self.__convert_to_entity(record)

    async def save(self, account: Account):
        transaction = await self.__connection.begin()
        try:
            query = self.__convert_to_insert_query(account)
            await self.__connection.execute(query)
            await transaction.commit()
        except:
            await transaction.rollback()
            raise Exception('error save account')

    async def update(self, account: Account):
        transaction = await self.__connection.begin()
        try:
            query = self.__convert_to_update_query(account)
            print('#### query: ', query)
            await self.__connection.execute(query)
            await transaction.commit()

        except:
            await transaction.rollback()
            raise Exception('error update account')

    def __convert_to_insert_query(self, account: Account) -> str:
        account_id, email, hashed_password, activate = account.serialize()
        query = MySQLQuery.into(
            self.__table
        ).columns(
            'id',
            'email',
            'hashed_password',
            'activate',
        ).insert(
            account_id,
            email,
            hashed_password,
            int(activate),
        )

        return str(query)

    def __convert_to_update_query(self, account: Account) -> str:
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
    def __convert_to_entity(record) -> Account:
        return Account.restore(
            record[0],
            record[1],
            record[2],
            bool(record[3]),
        )
