from rdb.migrations.migrator_collection import MigratorCollection
from rdb.migrations.create_accounts_table import CreateAccountsTable
from config.rdb import MysqlConfig


async def migrate():
    config = MysqlConfig()
    await config.connect()
    connection = config.get_connection()
    migrator_collection = MigratorCollection([
        CreateAccountsTable(connection)
    ])
    await migrator_collection.up()


async def migrate_down():
    config = MysqlConfig()
    await config.connect()
    connection = config.get_connection()
    migrator_collection = MigratorCollection([
        CreateAccountsTable(connection)
    ])
    await migrator_collection.down()


if __name__ == '__main__':
    import asyncio
    import sys

    args = sys.argv
    if len(args) == 1:
        asyncio.run(migrate())
    elif args[1] == 'down':
        asyncio.run(migrate_down())
