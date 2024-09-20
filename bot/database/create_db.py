import logging
from psycopg2 import (
    DatabaseError,
    OperationalError,
    ProgrammingError,
    connect,
)
from config_data.config import load_config


logger_db = logging.getLogger(__name__)
config = load_config()


def create_db() -> dict:
    """Установление первого соединения и создание БД."""
    try:
        conn = connect(
            host=config.db.host,
            user=config.db.user,
            password=config.db.password,
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT datname FROM pg_catalog.pg_database
            WHERE datname = %s
            """,
            (config.db.name,),
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {config.db.name}')
            text_msg = (
                f'База данных с именем {config.db.name} '
                'успешно создана.'
            )
            logger_db.info(text_msg)
            conn.close()
            return {'status': True, 'text_msg': text_msg}
        conn.close()
        text_msg = (
            f'База данных с именем {config.db.name} '
            'уже существует.'
        )
        logger_db.info(text_msg)
        return {'status': True, 'text_msg': text_msg}
    except (OperationalError, DatabaseError, ProgrammingError) as error:
        text_msg = (
            'При подключении к Postgres произошла ошибка.'
            f'произошла ошибка. Текст ошибки: {error}. '
            f'Тип ошибки: {type(error).__name__}.'
        )
        logger_db.exception(text_msg)
        conn.close()
        return {'status': False, 'error': text_msg}
    except Exception as error:
        text_msg = (
            'В ходе работы функции create_db произошла ошибка.'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        conn.close()
        logger_db.exception(text_msg)
        return {'status': False, 'error': text_msg}
