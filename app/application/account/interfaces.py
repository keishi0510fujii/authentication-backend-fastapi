import abc


class ICreateAccountUseCase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def execute(self, email: str, plain_password: str, password_confirm) -> str:
        pass
