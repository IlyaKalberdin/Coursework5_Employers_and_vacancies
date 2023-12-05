import psycopg2
import os
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self):
        """Инициализация экземпляра класс"""
        self.__dbname = os.getenv("DBNAME")
        self.__user = os.getenv("USER")
        self.__password = os.getenv("PASSWORD")
        self.__host = os.getenv("HOST")

    def push_area(self, area):
        """Отправка информации о регионе в БД"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO area VALUES(%s, %s)",
                                   (area["id"], area["name"].lower()))
        except errors.lookup(UNIQUE_VIOLATION):
            print(f"{area['name']} уже есть")
        finally:
            conn.close()

    def push_employer(self, employer):
        """Отправка информации о работодатели в БД"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"INSERT INTO employers VALUES(%s, %s, %s, %s, %s, %s, %s)",
                                   (employer['id'].lower(),
                                    employer['name'].lower(),
                                    employer['area']['id'],
                                    employer['site_url'],
                                    employer['alternate_url'],
                                    employer['vacancies_url'],
                                    employer['description']))
        except errors.lookup(UNIQUE_VIOLATION):
            print(f"{employer['name']} уже есть")
        finally:
            conn.close()

    def push_vacancy(self, vacancy):
        """Отправка информации о вакансии в БД"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"INSERT INTO vacancies VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (vacancy["id"].lower(),
                                    vacancy["name"].lower(),
                                    vacancy["salary"]["from"],
                                    vacancy["snippet"]["requirement"],
                                    vacancy["snippet"]["responsibility"],
                                    vacancy["area"]["id"].lower(),
                                    vacancy["employer"]["id"].lower(),
                                    vacancy["contacts"],
                                    vacancy["created_at"].lower(),
                                    vacancy["alternate_url"]))
        except errors.lookup(UNIQUE_VIOLATION):
            print(f"{vacancy['name']} уже есть")
        finally:
            conn.close()

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и кол-во
        вакансий у каждой компании"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT employer_id, employer_name, employers.area_id, site_url, employers.alternate_url, "
                        "vacancies_url, COUNT(vacancy_id) as count_vacancies, description FROM employers "
                        "JOIN vacancies USING(employer_id)"
                        "GROUP BY employer_id")
                    employers = cursor.fetchall()
        finally:
            conn.close()

        return employers

    def get_all_vacancies(self):
        """Метод получает список всех вакансий с названием кампании,
        вакансии, зарплаты и ссылкой на вакансию"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT employer_name, vacancy_name, salary, vacancies.alternate_url FROM vacancies "
                        "JOIN employers USING(employer_id) "
                        "GROUP BY employer_name, vacancy_name, salary, vacancies.alternate_url "
                        "ORDER BY employer_name")
                    vacancies = cursor.fetchall()
        finally:
            conn.close()

        return vacancies

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT AVG(salary) FROM vacancies")
                    avg_salary = cursor.fetchall()
        finally:
            conn.close()

        return avg_salary[0][0]

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM vacancies "
                        "WHERE salary > (SELECT AVG(salary) FROM vacancies)")
                    vacancies = cursor.fetchall()
        finally:
            conn.close()

        return vacancies

    def get_vacancies_with_keyword(self, text):
        """Метод получает список всех вакансий,
        в названии которых содержаться переданные слова"""
        try:
            with psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                  host=self.__host) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{text}%'")
                    vacancies = cursor.fetchall()
        finally:
            conn.close()

        return vacancies
