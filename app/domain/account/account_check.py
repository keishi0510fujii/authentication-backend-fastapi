from domain.account.service import IAccountCheck
from domain.account.repository import AccountRepository
from typing import List, Union
from domain.account.model import Account


class AccountCheck(IAccountCheck):
    __repository: AccountRepository

    def __init__(self, repo: AccountRepository):
        self.__repository = repo

    @staticmethod
    def __exists_account(email: str, account_list: List[Account]) -> bool:
        if len(account_list) == 0:
            return False

        email_list = [a.serialize()[1] for a in account_list]
        return email in email_list

    async def can_create_account(self, email: str) -> bool:
        account_list: List[Account] = await self.__repository.find_all()
        is_exist: bool = self.__exists_account(email, account_list)
        return not is_exist
