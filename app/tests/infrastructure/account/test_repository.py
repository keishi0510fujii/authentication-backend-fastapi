import pytest
import ulid
from typing import List
from domain.account.repository import AccountRepository
from domain.account.model import Account
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from tests.helper.infrastructure.rdb.base import get_connection
from tests.helper.infrastructure.rdb.account import AccountsTablePersist, AccountsTableQuery, AccountDto, \
    AccountDtoListFactory
from aiomysql import Connection


async def get_repository() -> AccountRepository:
    conn: Connection = await get_connection()
    return AccountRepositoryMysql(conn)


@pytest.mark.asyncio
async def test_save():
    #   並列テスト時に他のテストに影響を及ぼさないように、ユニークなemailはユニークな値を自動生成している
    email, password = f"{ulid.new().str}@example.come", "hogeH0g="
    new_account = Account.create_new(email, password, password)
    repository = await get_repository()
    await repository.save(new_account)
    #   登録できたことをテスト
    dto: AccountDto = await AccountsTableQuery.find_by_unique_value(unique_value=email)
    assert dto.email == email

    await AccountsTablePersist.delete_by_dto_list([dto])


@pytest.mark.asyncio
async def test_find_by_email():
    #   並列テスト時に他のテストに影響を及ぼさないように、emailはユニークな値を自動生成し、重複しないようにしている
    dto_count: int = 5
    dto_list: List[AccountDto] = await AccountDtoListFactory.make(dto_count)
    await AccountsTablePersist.save_by_dto_list(dto_list)
    #   Accountが復元できることをテスト
    idx = 2
    dto = dto_list[idx]
    repository: AccountRepository = await get_repository()
    account: Account = await repository.find_by_email(dto.email)
    assert (dto.id, dto.email, dto.hashed_password, bool(dto.activate)) == account.serialize()

    await AccountsTablePersist.delete_by_dto_list(dto_list)


@pytest.mark.asyncio
async def test_update():
    #   並列テスト時に他のテストに影響を及ぼさないように、emailはユニークな値を自動生成し、重複しないようにしている
    dto_count: int = 5
    dto_list: List[AccountDto] = await AccountDtoListFactory.make(dto_count)
    await AccountsTablePersist.save_by_dto_list(dto_list)
    #   更新できることをテスト
    idx: int = 2
    dto = dto_list.pop(idx)
    account: Account = Account.restore(dto.id, dto.email, dto.hashed_password, bool(dto.activate))
    new_email = f"{ulid.new().str}@example.come"
    account.change_email(new_email)
    repository = await get_repository()
    await repository.update(account)
    re_dto: AccountDto = await AccountsTableQuery.find_by_unique_value(new_email)
    assert (re_dto.id, re_dto.email, re_dto.hashed_password, bool(re_dto.activate)) == account.serialize()

    dto_list.append(re_dto)
    await AccountsTablePersist.delete_by_dto_list(dto_list)


@pytest.mark.asyncio
async def test_find_all():
    #   並列テスト時に他のテストに影響を及ぼさないように、emailはユニークな値を自動生成し、重複しないようにしている
    dto_count: int = 10
    dto_list: List[AccountDto] = await AccountDtoListFactory.make(dto_count)
    await AccountsTablePersist.save_by_dto_list(dto_list)
    #   登録したレコード全てを取得
    repository: AccountRepository = await get_repository()
    account_list: List[Account] = await repository.find_all()
    #   全てのデータが取得でき、Accountとして復元できていることをテスト
    for i, account in enumerate(account_list):
        dto = dto_list[i]
        assert (dto.id, dto.email, dto.hashed_password, bool(dto.activate)) == account.serialize()
    #   テーブルを初期化するため、レコードを全て削除
    await AccountsTablePersist.delete_by_dto_list(dto_list)
