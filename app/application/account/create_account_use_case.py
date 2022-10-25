from application.account.interfaces import ICreateAccountUseCase
from domain.account.repository import AccountRepository
from domain.account.service import IAccountCheck
from domain.account.model import Account


class CreateAccountUseCase(ICreateAccountUseCase):
    __repository: AccountRepository
    __account_check: IAccountCheck

    def __init__(self, repo: AccountRepository, account_check: IAccountCheck):
        self.__repository = repo
        self.__account_check = account_check

    async def execute(self, email: str, plain_password: str, password_confirm) -> str:
        can_create: bool = await self.__account_check.can_create_account(email)
        if not can_create:
            raise Exception('can not create account. email: ', email)

        account: Account = Account.create_new(email, plain_password, password_confirm)
        await self.__repository.save(account)
        return account.serialize()[0]
