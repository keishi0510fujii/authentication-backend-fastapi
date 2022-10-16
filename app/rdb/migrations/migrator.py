import abc


class Migrator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def up(self):
        pass

    @abc.abstractmethod
    async def down(self):
        pass
