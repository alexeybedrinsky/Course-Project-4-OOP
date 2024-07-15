from abc import ABC, abstractmethod
import requests


class AbstractVacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, search_query, per_page=100):
        pass


class HeadHunterAPI(AbstractVacancyAPI):
    def get_vacancies(self, query, per_page=100):
        url = f'https://api.hh.ru/vacancies?text={query}&per_page={per_page}'
        response = requests.get(url)

        # Проверка успешности запроса
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            response.raise_for_status()  # Поднимаем исключение в случае ошибки


# Пример использования
if __name__ == "__main__":
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python developer")
    for vacancy in vacancies:
        print(vacancy)
