import pytest
import ulid
from typing import Tuple
from application.account.interfaces import ICreateAccountUseCase
from application.account.create_account_use_case import CreateAccountUseCase
from domain.account.repository import AccountRepository
from tests.infrastructure.helper.unittest_rdb import get_connection, execute_command, execute_query
from infrastructure.mysql.account.repository import AccountRepositoryMysql


async def get_repository() -> AccountRepository:
    connection = await get_connection()
    return AccountRepositoryMysql(connection)


@pytest.mark.asyncio
async def test_execute():
    #   インスタンスの生成
    repo: AccountRepository = await get_repository()
    use_case: ICreateAccountUseCase = CreateAccountUseCase(repo)
    #   テストデータを生成して、ユースケースの結果を取得
    email, password = f"{ulid.new().str}@example.come", "hogeH0G="
    account_id = await use_case.execute(email, password, password)
    #   挿入されたレコードをを取得
    query = f"SELECT id, email, hashed_password, activate FROM accounts WHERE email='{email}';"
    query_result = await execute_query(query)
    record = await query_result.first()
    #   取得したレコードのidと、ユースケースの結果が一致することをテスト
    assert account_id == record[0]
