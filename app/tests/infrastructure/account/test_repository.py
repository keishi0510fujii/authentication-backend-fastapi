import pytest
import ulid
from typing import List, Tuple
from domain.account.repository import AccountRepository
from tests.infrastructure.helper.unittest_rdb import get_connection, execute_command, execute_query
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from domain.account.model import Account
from passlib.hash import pbkdf2_sha256


async def get_repository() -> AccountRepository:
    connection = await get_connection()
    return AccountRepositoryMysql(connection)


async def delete_records(email_list: List[str]):
    where_states = (f"email='{email}'" for email in email_list)
    where_condition = " OR ".join(where_states)
    query = f"DELETE FROM accounts WHERE {where_condition}"
    await execute_command(query)


class InsertRecord:
    id: str
    email: str
    hashed_password: str
    activate: int


def create_insert_records(record_count: int) -> List[InsertRecord]:
    records = []
    for i in range(record_count):
        r = InsertRecord()
        r.id = ulid.new().str
        r.email = f"{ulid.new().str}@example.come"
        r.hashed_password = pbkdf2_sha256.hash("hogeH0G=")
        r.activate = 1
        records.append(r)
    return records


def convert_to_insert_values(records: List[InsertRecord]) -> str:
    value_list = (f"('{r.id}', '{r.email}', '{r.hashed_password}', {r.activate})" for r in records)
    return ", ".join(value_list)


@pytest.mark.asyncio
async def test_save():
    #   並列テスト時に他のテストに影響を及ぼさないように、ユニークなemailはユニークな値を自動生成している
    email, password = f"{ulid.new().str}@example.come", "hogeH0g="
    account = Account.create_new(email, password, password)
    repo = await get_repository()
    await repo.save(account)
    #   登録できたか確認するため、メールアドレスを指定してrecordを取得
    query = f"SELECT id, email, hashed_password, activate FROM accounts WHERE email='{email}';"
    query_result = await execute_query(query)
    record = await query_result.first()
    #   登録した情報と復元した情報が一致することをテスト
    assert (record[0], record[1], record[2], bool(record[3])) == account.serialize()
    #   単体テストの時は毎回テーブルを空にするため、このスコープで登録したレコードは削除する
    await delete_records([email])


@pytest.mark.asyncio
async def test_find_by_email():
    #   引数の数値を変更すると挿入するレコードを増やせます
    records: List[InsertRecord] = create_insert_records(5)
    values: str = convert_to_insert_values(records)
    #   bulk insert
    command = f"INSERT INTO accounts (id, email, hashed_password, activate) VALUES {values}"
    await execute_command(command)
    #   index=2のemailを指定して、Accountを復元
    repo = await get_repository()
    record = records[2]
    account: Account = await repo.find_by_email(record.email)
    assert (record.id, record.email, record.hashed_password, bool(record.activate)) == account.serialize()
    #   単体テストの時は毎回テーブルを空にするため、このスコープで登録したレコードは削除する
    emails = [r.email for r in records]
    await delete_records(emails)


@pytest.mark.asyncio
async def test_update():
    #   数値を変更すると挿入するレコードを増やせます
    record_count = 5
    records: List[InsertRecord] = create_insert_records(record_count)
    #   `(id, email, hashed_password, activate), (id, email, hashed_password, activate), ...`の表記に変換
    value_list = (f"('{r.id}', '{r.email}', '{r.hashed_password}', {r.activate})" for r in records)
    values = ", ".join(value_list)
    #   bulk insert
    command = f"INSERT INTO accounts (id, email, hashed_password, activate) VALUES {values}"
    await execute_command(command)
    #   index=2の情報からmodelを生成して、emailを変更する
    record = records[2]
    account: Account = Account.restore(record.id, record.email, record.hashed_password, bool(record.activate))
    new_email = f"{ulid.new().str}@example.come"
    account.change_email(new_email)
    repo = await get_repository()
    await repo.update(account)
    #   更新後の情報を取得
    query = f"SELECT id, email, hashed_password, activate FROM accounts WHERE email='{new_email}';"
    query_result = await execute_query(query)
    #   emailのみ更新され、他は更新されていないことをテスト
    r = await query_result.first()
    assert (r[0], r[1], r[2], r[3]) == account.serialize()
