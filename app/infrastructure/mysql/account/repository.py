from domain.account.repository import AccountRepository
from domain.account.model import Account
from pypika import Table, MySQLQuery
from aiomysql.sa.connection import SAConnection


class AccountRepositoryMysql(AccountRepository):
    __root_table: Table
    __connection: SAConnection

    def __init__(self, conn: SAConnection):
        self.__root_table = Table('accounts')
        self.__connection = conn

    async def save(self, account: Account):
        transaction = await self.__connection.begin()
        try:
            query = self.__convert_to_insert_query(account)
            await self.__connection.execute(query)
            await transaction.commit()
        except:
            transaction.rollback()
            raise Exception('error save accounts')

    async def find_by_email(self, email: str) -> Account:
        query = MySQLQuery\
            .from_(self.__root_table)\
            .select('id', 'email', 'hashed_password', 'activate')\
            .where(self.__root_table.email == email)
        query_result = await self.__connection.execute(str(query))
        record = await query_result.first()
        return self.__convert_to_entity(record)

    def __convert_to_insert_query(self, account: Account) -> str:
        account_id, email, hashed_password, activate = account.serialize()
        query = MySQLQuery.into(
            self.__root_table
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

    @staticmethod
    def __convert_to_entity(record) -> Account:
        return Account.restore(
            record[0],
            record[1],
            record[2],
            bool(record[3]),
        )
