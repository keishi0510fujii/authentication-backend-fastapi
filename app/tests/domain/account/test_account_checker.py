import pytest
import ulid
from typing import List
from passlib.hash import pbkdf2_sha256
from tests.infrastructure.helper.unittest_rdb import get_cursor, execute_command, get_connection
from aiomysql.cursors import Cursor
from domain.account.repository import AccountRepository
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from domain.account.service import IAccountChecker
from domain.account.account_checker import AccountChecker


class __InsertRecord:
    id: str
    email: str
    hashed_password: str
    activate: int


def create_insert_records(record_count: int) -> List[__InsertRecord]:
    records = []
    for i in range(record_count):
        r = __InsertRecord()
        r.id = ulid.new().str
        r.email = f"{ulid.new().str}@example.come"
        r.hashed_password = pbkdf2_sha256.hash("hogeH0G=")
        r.activate = 1
        records.append(r)
    return records


def convert_to_insert_values(records: List[__InsertRecord]) -> str:
    value_list = (f"('{r.id}', '{r.email}', '{r.hashed_password}', {r.activate})" for r in records)
    return ", ".join(value_list)


async def get_service() -> IAccountChecker:
    conn = await get_connection()
    repo = AccountRepositoryMysql(conn)
    return AccountChecker(repo)


async def get_repository() -> AccountRepository:
    conn = await get_connection()
    return AccountRepositoryMysql(conn)


@pytest.mark.asyncio
async def test_can_create_account_is_not_ok():
    #   事前データの挿入
    records: List[__InsertRecord] = create_insert_records(5)
    values: str = convert_to_insert_values(records)
    command = f"INSERT INTO accounts (id, email, hashed_password, activate) VALUES {values}"
    await execute_command(command)
    #   挿入した事前データと同じemailを含むデータが登録できないことをテスト
    target_record = records[0]
    service = await get_service()
    is_ok = await service.can_create_account(target_record.email)
    assert not is_ok


@pytest.mark.asyncio
async def test_can_create_account_is_ok():
    #   事前データの挿入
    records: List[__InsertRecord] = create_insert_records(5)
    values: str = convert_to_insert_values(records)
    command = f"INSERT INTO accounts (id, email, hashed_password, activate) VALUES {values}"
    await execute_command(command)
    new_email = "test_can_create_account_is_ok@example.come"
    service = await get_service()
    is_ok = await service.can_create_account(new_email)
    assert is_ok
