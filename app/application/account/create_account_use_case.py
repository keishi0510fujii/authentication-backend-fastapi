from application.account.interfaces import ICreateAccountUseCase
from domain.account.repository import AccountRepository
from domain.account.model import Account


class CreateAccountUseCase(ICreateAccountUseCase):
    __repository: AccountRepository

    def __init__(self, repo: AccountRepository):
        self.__repository = repo

    async def execute(self, email: str, plain_password: str, password_confirm) -> str:
        account: Account = Account.create_new(email, plain_password, password_confirm)
        await self.__repository.save(account)
        return account.serialize()[0]
