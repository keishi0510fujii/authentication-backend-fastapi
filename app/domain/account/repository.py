import abc
from domain.account.model import Account
from typing import List


class AccountRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def find_all(self) -> List[Account]:
        pass

    @abc.abstractmethod
    async def find_by_email(self, email: str) -> Account:
        pass

    @abc.abstractmethod
    async def save(self, account: Account):
        pass

    @abc.abstractmethod
    async def update(self, account: Account):
        pass
