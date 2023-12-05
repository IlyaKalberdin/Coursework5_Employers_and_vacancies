from classes.database_manager import DBManager


def main():
    while True:
        database = DBManager()

        print("""Выберите, что хотите сделать:
                1 - получить список всех кампаний и кол-во их вакансий
                2 - получить список всех вакансий с названием кампаний,
                    вакансий, зарплатой и ссылкой
                3 - получить среднюю зарплату по вакансиям
                4 - получить список всех вакансий, у которых зарплата
                    выше средней
                5 - получить список всех вакансий по указанному Вами слову
                6 - выйти из программы""")
        user_input = input()

        if user_input == "1":
            data = database.get_companies_and_vacancies_count()
        elif user_input == "2":
            data = database.get_all_vacancies()
        elif user_input == "3":
            data = database.get_avg_salary()
        elif user_input == "4":
            data = database.get_vacancies_with_higher_salary()
        elif user_input == "5":
            keyword = input("Введите слово, по которому хотите найти вакансии: ").lower()

            data = database.get_vacancies_with_keyword(keyword)
        elif user_input == "6":
            break
        else:
            print("Неверный ввод")
            continue

        if type(data) is int:
            print(f"Средняя зарплата: {data}")
        else:
            print("Получены следующие данные")
            for d in data:
                print(d)


if __name__ == "__main__":
    main()