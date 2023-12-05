import requests


class HeadHunterApi:
    """Класс для работы с API HH.ru
    Получает информацию о работодателях и их вакансиях"""

    def __init__(self) -> None:
        """Инициализация экземпляра класса"""
        self.employers_url = "https://api.hh.ru/employers"
        self.vacancies_url = "https://api.hh.ru/vacancies"

    def get_employers(self, text: str) -> list:
        """Метод для получения списка работодателей
        text: Ключевое слово для поиска"""
        employers = requests.get(self.employers_url, {"text": text,
                                                      "boolean": True,
                                                      "sort_by": "by_vacancies_open"})

        return employers.json()["items"]

    def get_info_employer(self, employer_id: str) -> dict:
        """Метод для получения информации о работодатели
        employer_id: id работодателя"""
        employer = requests.get(self.employers_url + f"/{employer_id}")

        return employer.json()

    def get_employer_vacancies(self, employer_id: str) -> list:
        """Метод для получения вакансий работодателя
        employer_id: id работодателя"""
        employer_vacancies = requests.get(self.vacancies_url,
                                          {"employer_id": employer_id, "only_with_salary": True})

        return employer_vacancies.json()["items"]
