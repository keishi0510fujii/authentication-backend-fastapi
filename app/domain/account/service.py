import abc


class IAccountChecker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def can_create_account(self, email: str) -> bool:
        pass
