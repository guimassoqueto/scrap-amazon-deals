import asyncpg
from playwright_amazon.settings import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    POSTGRES_PORT,
    POSTGRES_DB,
)


async def upsert_data(table: str, item: dict) -> None:
    """
    Upsert data into a postgres table.

    Args:
        table (string): The name of the table that the data will be inserted.
        data (dict): The data that will populate the table.

    Returns:
        None.

    Example:
        >>> INSERT INTO products(id,title,category,reviews) VALUES('B0BTRPDWTB','Guilherme','Categoria Guilherme',666) ON CONFLICT (id) DO UPDATE SET id = 'B0BTRPDWTB',title = 'Guilherme',category = 'Categoria Guilherme',reviews = 666;
    """
    connection = await asyncpg.connect(
        user=POSTGRES_USER,
        port=POSTGRES_PORT,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
    )

    await connection.execute(upsert_query(table, item))
    await connection.close()


def upsert_query(table: str, item: dict) -> str:
    insert = f"INSERT INTO {table}("
    values = "VALUES("
    on_conflict = "ON CONFLICT (id)\nDO UPDATE SET "
    for key, value in item.items():
        insert += f"{key},"

        if isinstance(value, str):
            values += f"'{value}',"
            on_conflict += f"{key} = '{value}',"
        else:
            values += f"{value},"
            on_conflict += f"{key} = {value},"

    insert += "updated_at)\n"
    values += f"NOW())\n"
    on_conflict += f"updated_at = NOW();"

    return insert + values + on_conflict
