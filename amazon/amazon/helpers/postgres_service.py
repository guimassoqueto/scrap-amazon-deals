from datetime import datetime
import psycopg


def upsert_item_query(table: str, item: dict) -> str:
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


def select_non_inserted_pids_query(pid_errors_file: str = "pid_errors.log") -> str:
    query_pids = []
    with open(pid_errors_file, "r", encoding="utf-8") as file:
        for product_id in file:
            product_id = product_id.strip()
            query_pids.append(f"('{product_id}')")
    query = "SELECT id\nFROM (VALUES \n"
    query += ", \n".join(query_pids)
    query += f") V(id) EXCEPT SELECT id FROM products WHERE updated_at BETWEEN '{datetime.today().strftime('%Y-%m-%d')}' AND NOW();"

    return query


class PostgresDB:
    def __init__(
        self, dbname: str, dbuser: str, dbpassword: str, dbhost: str, dbport: str
    ) -> None:
        self.conninfo = f"dbname={dbname} user={dbuser} password={dbpassword} host={dbhost} port={dbport}"

    async def upsert_item(self, table: str, item: dict) -> None:
        async with await psycopg.AsyncConnection.connect(self.conninfo) as aconn:
            async with aconn.cursor() as cur:
                await cur.execute(upsert_item_query(table, item))

    def select_non_inserted_ids(self, pid_errors_file: str) -> list:
        with psycopg.connect(self.conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(select_non_inserted_pids_query(pid_errors_file))
                non_inserted_ids = cur.fetchall()
                conn.commit()
                return non_inserted_ids
