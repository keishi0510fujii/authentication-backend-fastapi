import pytest
from aiomysql.connection import Connection
from typing import List
from tests.helper.infrastructure.rdb.base import get_connection
from tests.helper.infrastructure.rdb.account import AccountDto
from tests.helper.infrastructure.rdb.account import AccountsTablePersist, AccountDtoListFactory
from domain.account.repository import AccountRepository
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from domain.account.service import IAccountChecker
from domain.account.account_checker import AccountChecker


async def get_account_checker() -> IAccountChecker:
    conn: Connection = await get_connection()
    repo: AccountRepository = AccountRepositoryMysql(conn)
    return AccountChecker(repo)


@pytest.mark.asyncio
async def test_can_create_account_is_not_ok():
    dto_count: int = 5
    dto_list: List[AccountDto] = await AccountDtoListFactory.make(dto_count)
    await AccountsTablePersist.save_by_dto_list(dto_list)

    idx: int = 0
    dto: AccountDto = dto_list[idx]
    account_checker = await get_account_checker()
    is_ok = await account_checker.can_create_account(dto.email)
    #   重複するemailが存在する場合、アカウントを作成できない
    assert not is_ok

    await AccountsTablePersist.delete_by_dto_list(dto_list)


@pytest.mark.asyncio
async def test_can_create_account_is_ok():
    dto_count: int = 5
    dto_list: List[AccountDto] = await AccountDtoListFactory.make(dto_count)
    await AccountsTablePersist.save_by_dto_list(dto_list)

    new_email = "test_can_create_account_is_ok@example.come"
    account_checker = await get_account_checker()
    is_ok = await account_checker.can_create_account(new_email)
    #   重複しないemailであれば、アカウントを作成できる
    assert is_ok

    await AccountsTablePersist.delete_by_dto_list(dto_list)
