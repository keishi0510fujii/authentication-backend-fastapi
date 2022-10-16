import unittest
import ulid
from aiomysql.sa.connection import SAConnection
from domain.account.repository import AccountRepository
from domain.account.model import Account
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from tests.infrastructure.helper.unittest_rdb import get_connection


class TestAccountRepositoryMysql(unittest.IsolatedAsyncioTestCase):
    __repository: AccountRepository
    __connection: SAConnection

    async def asyncSetUp(self) -> None:
        #   repositoryにconnectionをセット
        self.__connection = await get_connection()
        self.__repository = AccountRepositoryMysql(self.__connection)

    async def test_save(self):
        email = f"{ulid.new().str}@example.come"
        plain_password = "hogeH0G="
        new_account = Account.create_new(email, plain_password, plain_password)
        await self.__repository.save(new_account)

        #   登録したAccountを復元
        restored_account: Account = await self.__repository.find_by_email(email)
        #   他のテストに影響を与えないために、復元後は登録したレコードを削除
        transaction = await self.__connection.begin()
        await self.__connection.execute(f"DELETE FROM accounts WHERE email='{email}'")
        await transaction.commit()
        #   保存前に生成したAccountと復元したAccountのプロパティが同じであることをテスト
        self.assertEqual(new_account.serialize(), restored_account.serialize())

    async def test_find_by_email(self):
        #   並列に処理した時に、他のテストで登録したemailと重複しないようにulidで毎回ユニークな値を生成している
        hoge_email = f"{ulid.new().str}@example.come"
        fuga_email = f"{ulid.new().str}@example.come"
        plain_password = "hogeH0G="

        #   2レコード分のデータを保存
        hoge_account = Account.create_new(hoge_email, plain_password, plain_password)
        fuga_account = Account.create_new(fuga_email, plain_password, plain_password)
        await self.__repository.save(hoge_account)
        await self.__repository.save(fuga_account)

        #   hoge_accountを復元
        restored_hoge: Account = await self.__repository.find_by_email(hoge_email)
        #   他のテストに影響を与えないために、復元後は登録したレコードを削除
        transaction = await self.__connection.begin()
        await self.__connection.execute(f"DELETE FROM accounts WHERE email='{hoge_email}' OR email='{fuga_email}'")
        await transaction.commit()
        #   複数のレコードからhoge_accountのみを取得できたことをテスト
        self.assertEqual(hoge_account.serialize(), restored_hoge.serialize())


if __name__ == '__main__':
    unittest.main()
