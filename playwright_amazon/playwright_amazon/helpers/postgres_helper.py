import asyncpg
from playwright_amazon.settings import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    POSTGRES_PORT,
    POSTGRES_DB,
)


async def insert_into(table: str, data: dict) -> None:
    """
    Insert data into a postgres table.

    Args:
        table (string): The name of the table that the data will be inserted.
        data (dict): The data that will populate the table.

    Returns:
        None.

    Example:
        >>> insert_into("users", data: {"name": "John", "date_of_birth": datetime.date(1990, 1, 1)})
    """
    connection = await asyncpg.connect(
        user=POSTGRES_USER,
        port=POSTGRES_PORT,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
    )

    columns = ", ".join(data.keys())
    values = ", ".join(f"${i}" for i in range(1, len(data) + 1))

    await connection.execute(
        f"INSERT INTO {table}({columns}) VALUES({values})", *data.values()
    )
    await connection.close()
