import pytest
from domain.account.model import Account

HOGE_EMAIL = 'hogehoge@example.come'
FUGA_EMAIL = 'fugafuga@example.come'
HOGE_PASSWORD = 'hogeH0g='
INVALID_HOGE_PASSWORD = 'hogEH0g='
FUGA_PASSWORD = 'fuga2Ug@'
INVALID_FUGA_PASSWORD = 'fuga2UG@'


def test_create_new_exception_by_password_is_not_equal_confirm():
    #   passwordとpassword_confirmが同じ値ではないためエラーとなる
    with pytest.raises(Exception):
        account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, INVALID_HOGE_PASSWORD)


def test_serialize():
    account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, HOGE_PASSWORD)
    #   ULIDで自動生成したIDとなるため固定値での判定は難しく、長さだけをテストしている
    assert 26 == len(account.serialize()[0])
    #   登録したemailを取得できることをテストしている
    assert HOGE_EMAIL == account.serialize()[1]
    #   パスワードはハッシュ化されるため、取得した際に平文ではないことをテストしている
    assert HOGE_PASSWORD != account.serialize()[2]
    #   activateの初期値がFalseになっていることをテストしている
    assert not account.serialize()[3]


def test_change_password_exception_by_new_password_is_not_equal_confirm():
    account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, HOGE_PASSWORD)
    #   passwordとpassword_confirmが同じ値ではないためエラーとなる
    with pytest.raises(Exception):
        account.change_password(FUGA_PASSWORD, INVALID_FUGA_PASSWORD)


def test_change_password():
    account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, HOGE_PASSWORD)
    old_hashed_password = account.serialize()[2]
    #   パスワード変更時にactivateがFalseとなることを確認するため、ここでTrueにしておく
    account.active()
    account.change_password(FUGA_PASSWORD, FUGA_PASSWORD)
    #   パスワードのハッシュ値が変更されていることをテストしている
    assert old_hashed_password != account.serialize()[2]
    #   パスワードを変更すると、activateがFalseになっていることをテストしている
    assert not account.serialize()[3]


def test_change_email_exception_by_new_email_is_equal_old_email():
    account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, HOGE_PASSWORD)
    #   既存のemailと新しいemailが同じ値であるためエラーとなる
    with pytest.raises(Exception):
        account.change_email(HOGE_EMAIL)


def test_change_email():
    account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, HOGE_PASSWORD)
    #   email変更時にactivateがFalseになることを確認するため、ここでTrueにしておく
    account.active()
    account.change_email(FUGA_EMAIL)
    #   emailが変更されていることをテストする
    assert FUGA_EMAIL == account.serialize()[1]
    #   activateがFalseになっていることをテストする
    assert not account.serialize()[3]


def test_restore():
    account = Account.create_new(HOGE_EMAIL, HOGE_PASSWORD, HOGE_PASSWORD)
    account_id, email, hashed_password, activate = account.serialize()
    restored_account = Account.restore(account_id, email, hashed_password, activate)
    #   元の値からAccountを復元できることをテストしている
    assert restored_account.serialize() == account.serialize()
