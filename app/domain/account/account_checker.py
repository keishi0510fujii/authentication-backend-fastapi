from domain.account.service import IAccountChecker
from domain.account.repository import AccountRepository
from typing import List
from domain.account.model import Account


class AccountChecker(IAccountChecker):
    __repository: AccountRepository

    def __init__(self, repo: AccountRepository):
        self.__repository = repo

    @staticmethod
    def __exists_account(email: str, account_list: List[Account]) -> bool:
        email_list = [a.serialize()[1] for a in account_list]
        return email in email_list

    async def can_create_account(self, email: str) -> bool:
        account_list: List[Account] = await self.__repository.find_all()
        return not self.__exists_account(email, account_list)
