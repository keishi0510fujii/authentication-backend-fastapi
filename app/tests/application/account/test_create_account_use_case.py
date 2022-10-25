import pytest
import ulid
from application.account.interfaces import ICreateAccountUseCase
from application.account.create_account_use_case import CreateAccountUseCase
from domain.account.repository import AccountRepository
from domain.account.service import IAccountCheck
from domain.account.account_check import AccountCheck
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from tests.helper.infrastructure.rdb.base import get_connection
from tests.helper.infrastructure.rdb.account import AccountDto
from tests.helper.infrastructure.rdb.account import AccountsTableQuery, AccountsTablePersist


async def get_repository() -> AccountRepository:
    connection = await get_connection()
    return AccountRepositoryMysql(connection)


async def get_account_checker() -> IAccountCheck:
    repo = await get_repository()
    return AccountCheck(repo)


async def get_use_case() -> ICreateAccountUseCase:
    repository: AccountRepository = await get_repository()
    account_checker: IAccountCheck = await get_account_checker()
    return CreateAccountUseCase(repository, account_checker)


@pytest.mark.asyncio
async def test_execute():
    use_case = await get_use_case()
    email, password = f"{ulid.new().str}@example.come", "hogeH0G="
    account_id = await use_case.execute(email, password, password)

    dto: AccountDto = await AccountsTableQuery.find_by_unique_value(email)
    #   取得したレコードのidと、ユースケースの結果が一致することをテスト
    assert dto.id == account_id

    await AccountsTablePersist.delete_by_dto_list([dto])
