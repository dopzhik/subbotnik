import psycopg2
import os
from psycopg2 import Error, sql


async def create_db():
    try:
        with psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
        ) as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute('''
                        CREATE TABLE IF NOT EXISTS clients (
                        id_client INTEGER,
                        name VARCHAR(20),
                        phone BIGINT,
                        address VARCHAR(50),
                        pollution VARCHAR(100),
                        clean_date VARCHAR(20)
                        );
                    ''')
                    conn.commit()
                except Error as e:
                    conn.rollback()
                    print(F"Произошла ошибка создания БД: {e.pgcode} - {e.pgerror}")

    except Exception as e:
        print(f"Ошибка поймана. Детали: {e}")


async def set_database(id_client, fsm_dict):
    try:
        with psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
        ) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("INSERT INTO clients VALUES (%s, %s, %s, %s, %s, %s);", (id_client, *fsm_dict.values()))
                    conn.commit()
                except Error as e:
                    conn.rollback()
                    print(F"Произошла ошибка записи: {e.pgcode} - {e.pgerror}")

    except Exception as e:
        print(f"Ошибка поймана. Детали: {e}")


def get_menu_database(client_id=None):
    try:
        with psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
        ) as conn:
            with conn.cursor() as cur:
                if client_id is None:
                    query = sql.SQL("SELECT {fields} FROM {table};").format(
                        fields=sql.SQL(', ').join([
                            sql.Identifier('id_client'),
                            sql.Identifier('name'),
                            sql.Identifier('phone'),
                            sql.Identifier('address'),
                            sql.Identifier('pollution'),
                            sql.Identifier('clean_date')
                        ]),
                        table=sql.Identifier('clients')
                    )
                    cur.execute(query)
                    result = cur.fetchall()
                else:
                    query = sql.SQL("SELECT {fields} FROM {table} WHERE {key} = %s;").format(
                        fields=sql.SQL(', ').join([
                            sql.Identifier('id_client'),
                            sql.Identifier('name'),
                            sql.Identifier('phone'),
                            sql.Identifier('address'),
                            sql.Identifier('pollution'),
                            sql.Identifier('clean_date')
                        ]),
                        table=sql.Identifier('clients'),
                        key=sql.Identifier('id_client')
                    )
                    cur.execute(query, (client_id,))
                    result = cur.fetchone()
                return result

    except Exception as e:
        print(f"Ошибка поймана. Детали: {e}")

# user_dict: dict = {}
