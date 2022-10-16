import unittest

from domain.account.model import Account


class TestAccount(unittest.TestCase):
    def test_init_exception_password_is_not_equal_confirm(self):
        email = 'hoge@example.come'
        plain_password = 'hogehoge'
        password_confirm = 'hogehogeh'

        with self.assertRaises(Exception):
            # plain_passwordとpassword_confirmが同じ値ではないためエラーとなる
            Account.create_new(plain_password, password_confirm)

    def test_serialize(self):
        email = 'hoge@example.come'
        plain_password = 'hogehoge'
        password_confirm = 'hogehoge'

        account = Account.create_new(email, plain_password, password_confirm)
        account_id, mail_address, hashed_password, activate = account.serialize()
        # idがulidでユニークな値を生成するため、26文字かどうかを判定する
        self.assertEqual(26, len(account_id))
        # mail_addressはemailと同じ値であることを判定する
        self.assertEqual(email, mail_address)
        # 出力されるパスワードはハッシュ化されたものであるため、plain_passwordとは異なることを判定する
        self.assertNotEqual(plain_password, hashed_password)
        # 初めて生成されたAccountの場合、activateはFalseになる
        self.assertFalse(activate)


if __name__ == '__main__':
    unittest.main()
