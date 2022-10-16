import abc
from domain.account.model import Account


class AccountRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def save(self, account: Account):
        pass

    @abc.abstractmethod
    async def find_by_email(self, email: str):
        pass
