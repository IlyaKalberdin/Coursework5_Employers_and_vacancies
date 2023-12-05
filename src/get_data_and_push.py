from classes.headhunter_api import HeadHunterApi
from classes.database_manager import DBManager


def get_data_and_push():
    """Функция для получения работодателей и вакансий с hh.ru
    и их отправки в базу данных"""
    hh = HeadHunterApi()

    user_request = input("Введите ключевое слово для поиска компаний: ")

    employers = hh.get_employers(user_request)

    employers_info = []
    vacancies = []

    for employer in employers[:10]:
        employer_info = hh.get_info_employer(employer["id"])
        employers_info.append(employer_info)

        vacancy = hh.get_employer_vacancies(employer["id"])
        vacancies.extend(vacancy)

    areas = []

    for vacancy in vacancies:
        areas.append(vacancy["area"])

    for employer in employers_info:
        if employer["area"] not in areas:
            areas.append(employer["area"])

    dbm = DBManager()

    for area in areas:
        dbm.push_area(area)

    for employer in employers_info:
        dbm.push_employer(employer)

    for vacancy in vacancies:
        dbm.push_vacancy(vacancy)


if __name__ == "__main__":
    get_data_and_push()
