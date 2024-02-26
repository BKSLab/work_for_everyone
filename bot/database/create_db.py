from environs import Env
from psycopg2 import connect


def create_db():
    """Установление первого соединения и создание БД."""
    env = Env()
    env.read_env()
    conn = connect(
        host=env('DB_HOST'),
        user=env('POSTGRES_USER'),
        password=env('POSTGRES_PASSWORD'),
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT datname FROM pg_catalog.pg_database
        WHERE datname = %s
        """,
        (env('DB_NAME'),),
    )
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f'CREATE DATABASE {env("DB_NAME")}')
    conn.close()
