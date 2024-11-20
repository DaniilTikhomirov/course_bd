from typing import Any, List, Tuple

import psycopg2
from src.Vacancy import Vacancy


class DBManager:
    """
    класс для работы с postgresSQL
    """

    def __init__(self, data_base_name: str, params: dict) -> None:
        """
        иницализация класса и проверка на то что такая бд уже существует
        :param data_base_name:имя бд
        :param params:параметры
        """
        self.params = params
        self.data_base_name = data_base_name
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{data_base_name}'")
            if cur.fetchone()[0]:
                cur.execute(f"CREATE DATABASE {data_base_name}")
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

    def create_table(self, table_name: str) -> None:
        """создание таблицы в бд"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                            id serial PRIMARY KEY,
                            name TEXT NOT NULL,
                            salary bigint NOT NULL,
                            url varchar(255),
                            id_vacancy varchar(255),
                            employer_name varchar(255)
                            )""")
                conn.commit()

                cur.execute(f"""CREATE TABLE IF NOT EXISTS employer (
                                            id serial PRIMARY KEY,
                                            employer_name varchar(255),
                                            employer_url varchar(255)
                                            )""")
                conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    def add_to_table(self, table_name: str, vacancy: Vacancy) -> None:
        """добавление в таблицу"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"""INSERT INTO {table_name} (name,
                    salary,
                    url,
                    id_vacancy,
                    employer_name,) 
                    VALUES (%s, %s, %s, %s, %s) returning *""", [vacancy.name,
                                                                     vacancy.salary,
                                                                     vacancy.url,
                                                                     vacancy.id,
                                                                     vacancy.employer_name])
                cur.execute(f"""INSERT INTO  employer (employer_name, employer_url)
                                VALUES (%s, %s)""", [vacancy.employer_name, vacancy.employer_link])
                conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    def add_list_to_table(self, table_name: str, vacancies: list[Vacancy]) -> None:
        """добавление в таблицу пачку данных"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                for vacancy in vacancies:
                    cur.execute(f"""INSERT INTO {table_name} (name,
                            salary,
                            url,
                            id_vacancy,
                            employer_name) 
                            VALUES (%s, %s, %s, %s, %s) returning *""", [vacancy.name,
                                                                             vacancy.salary,
                                                                             vacancy.url,
                                                                             vacancy.id,
                                                                             vacancy.employer_name])
                    cur.execute(f"""INSERT INTO  employer (employer_name, employer_url)
                                                    VALUES (%s, %s)""", [vacancy.employer_name, vacancy.employer_link])
                conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    def clear_table(self, table_name: str) -> None:
        """очистка таблицы"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY")
                cur.execute(f"TRUNCATE TABLE employer RESTART IDENTITY")
                conn.commit()
        except Exception as e:
            raise e

        finally:
            conn.close()

    def get_companies_and_vacancies_count(self, table_name: str) -> list[tuple[Any, ...]]:
        """возврощает сгрупированные вакансии"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT {table_name}.employer_name, COUNT(*) FROM {table_name}
                                    GROUP BY employer_name""")

                return cur.fetchall()

        except Exception as e:
            raise e

        finally:
            conn.close()

    def get_all_vacancies(self, table_name: str) -> list[tuple[Any, ...]]:
        """возврощает все вакансии"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT {table_name}.employer_name, name, salary, url, employer_url FROM {table_name} 
                INNER JOIN employer ON employer.employer_name = {table_name}.employer_name""")
                return cur.fetchall()

        except Exception as e:
            raise e

        finally:
            conn.close()

    def get_avg_salary(self, table_name: str) -> int:
        """возврощает среднию зп"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT AVG(salary) FROM {table_name}")
                return int(cur.fetchall()[0][0])

        except Exception as e:
            raise e

        finally:
            conn.close()

    def get_vacancies_with_higher_salary(self, table_name: str) -> list[tuple[Any, ...]]:
        """возврощает вакансии выше средний зп"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT * FROM {table_name} WHERE salary > (SELECT AVG(salary) FROM {table_name})""")
                return cur.fetchall()

        except Exception as e:
            raise e

        finally:
            conn.close()

    def get_vacancies_with_keyword(self, table_name: str, word: str) -> list[tuple[Any, ...]]:
        """возврощает вакансии с ключевым словом в имени"""
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table_name} WHERE name LIKE '%{word}%'")
                return cur.fetchall()

        except Exception as e:
            raise e

        finally:
            conn.close()

