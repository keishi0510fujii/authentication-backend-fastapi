import pytest
import asyncio
from config.unittest_rdb import MysqlConfig
from aiomysql.sa.connection import SAConnection
from domain.account.repository import AccountRepository
from domain.account.model import Account
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from tests.infrastructure.helper.unittest_rdb import MySqlUnitTestHelper
from tests.infrastructure.helper.unittest_rdb import get_connection

#
# @pytest.mark.asyncio
# async def test_save():
#     conn = await get_connection()
#     repo = AccountRepositoryMysql(conn)
#
#     email = "hogehoge@example.come"
#     plain_password = "hogeH0G="
#     new_account = Account.create_new(email, plain_password, plain_password)
#     await repo.save(new_account)
#     assert 1 == 1
