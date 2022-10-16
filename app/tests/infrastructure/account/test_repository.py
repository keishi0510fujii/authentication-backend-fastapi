import unittest
import asyncio
from config.unittest_rdb import MysqlConfig
from aiomysql.sa.connection import SAConnection
from domain.account.repository import AccountRepository
from domain.account.model import Account
from infrastructure.mysql.account.repository import AccountRepositoryMysql


class TestAccountRepositoryMysql(unittest.IsolatedAsyncioTestCase):
    __repository: AccountRepository
    __connection: SAConnection

    async def asyncSetUp(self) -> None:
        #   repositoryにconnectionをセット
        config = MysqlConfig()
        await config.connect()
        self.__connection = config.get_connection()
        self.__repository = AccountRepositoryMysql(self.__connection)

    async def asyncTearDown(self) -> None:
        transaction = await self.__connection.begin()
        await self.__connection.execute("DELETE FROM accounts;")
        await transaction.commit()
        await self.__connection.close()

    async def test_save(self):
        email = "hogehoge@example.come"
        plain_password = "hogeH0G="
        new_account = Account.create_new(email, plain_password, plain_password)
        await self.__repository.save(new_account)

        #   登録したAccountを復元
        restored_account: Account = await self.__repository.find_by_email(email)
        #   保存前に生成したAccountと復元したAccountのプロパティが同じであることをテスト
        self.assertEqual(new_account.serialize(), restored_account.serialize())

    async def test_find_by_email(self):
        hoge_email = "hogehoge@example.come"
        fuga_email = "fugafuga@example.come"
        plain_password = "hogeH0G="

        #   2レコード分のデータを保存
        hoge_account = Account.create_new(hoge_email, plain_password, plain_password)
        fuga_account = Account.create_new(fuga_email, plain_password, plain_password)
        await self.__repository.save(hoge_account)
        await self.__repository.save(fuga_account)

        #   hoge_accountを復元
        restored_hoge: Account = await self.__repository.find_by_email(hoge_email)
        #   複数のレコードからhoge_accountのみを取得できたことをテスト
        self.assertEqual(hoge_account.serialize(), restored_hoge.serialize())


if __name__ == '__main__':
    unittest.main()
