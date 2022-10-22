from application.account.interfaces import ICreateAccountUseCase
from domain.account.repository import AccountRepository
from domain.account.service import IAccountChecker
from domain.account.model import Account


class CreateAccountUseCase(ICreateAccountUseCase):
    __repository: AccountRepository
    __account_checker: IAccountChecker

    def __init__(self, repo: AccountRepository, account_checker: IAccountChecker):
        self.__repository = repo
        self.__account_checker = account_checker

    async def execute(self, email: str, plain_password: str, password_confirm) -> str:
        if not self.__account_checker.can_create_account(email):
            raise Exception('can not create account. email: ', email)

        account: Account = Account.create_new(email, plain_password, password_confirm)
        await self.__repository.save(account)
        return account.serialize()[0]
