from classes.database_manager import DBManager
from get_data_and_push import get_data_and_push


def main():
    while True:
        database = DBManager()

        user_input = input("""Выберите, что хотите сделать:
                1 - Загрузить данные о компаниях в базу данных
                2 - получить список всех кампаний и кол-во их вакансий
                3 - получить список всех вакансий с названием кампаний,
                    вакансий, зарплатой и ссылкой
                4 - получить среднюю зарплату по вакансиям
                5 - получить список всех вакансий, у которых зарплата
                    выше средней
                6 - получить список всех вакансий по указанному Вами слову
                7 - выйти из программы
                """)

        data = None

        if user_input == "1":
            user_request = input("Введите ключевое слово для поиска 10 компаний: ")

            get_data_and_push(user_request)
        elif user_input == "2":
            data = database.get_companies_and_vacancies_count()
        elif user_input == "3":
            data = database.get_all_vacancies()
        elif user_input == "4":
            data = database.get_avg_salary()
        elif user_input == "5":
            data = database.get_vacancies_with_higher_salary()
        elif user_input == "6":
            keyword = input("Введите слово, по которому хотите найти вакансии: ").lower()

            data = database.get_vacancies_with_keyword(keyword)
        elif user_input == "7":
            break
        else:
            print("Неверный ввод")
            continue

        if type(data) is int:
            print(f"Средняя зарплата: {data}")
        elif data is None:
            continue
        else:
            print("Получены следующие данные")
            for d in data:
                print(d)


if __name__ == "__main__":
    main()
