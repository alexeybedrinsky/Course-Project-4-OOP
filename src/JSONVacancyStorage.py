import json
from abc import ABC, abstractmethod
from src.Vacancy import Vacancy

# Абстрактный класс для работы с файлами
class FileHandler(ABC):
    """
    Абстрактный класс для обработки файлов.
    """
    @abstractmethod
    def read(self):
        """
        Чтение файла
        """
        pass

    @abstractmethod
    def write(self, data):
        """
        Запись в файл
        """
        pass

    @abstractmethod
    def append(self, data):
        """
        Добавление в файл
        """
        pass

# Класс для работы с JSON файлами, наследуемый от абстрактного класса
class JSONVacancyStorage(FileHandler):
    """
    Класс для работы с вакансиями в формате JSON.
    """
    def __init__(self, file_path='data/vacancies.json'):
        self._file_path = file_path  # Приватный атрибут

    def read(self):
        """
        Чтение из Джейсона
        """
        try:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File {self._file_path} not found.")
            return []
        except json.JSONDecodeError:
            print("Error: JSON decode error. Please check the JSON file format.")
            return []

    def write(self, data):
        """
        Запись в Джейсон
        """
        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def append(self, data):
        """
        Добавление в Лжейсон
        """
        current_data = self.read()
        current_data.extend(data)
        self.write(current_data)

    def get_vacancies(self):
        """
        Получение списка вакансий из Джейсона
        """
        data = self.read()
        vacancies = []
        for vacancy in data:
            if vacancy is None:
                print("Warning: Found NoneType vacancy. Skipping.")
                continue

            title = vacancy.get('title', '')
            company = vacancy.get('company', '')
            salary = vacancy.get('salary', 'Не указана')
            description = vacancy.get('description', '')
            link = vacancy.get('link', '')

            vacancies.append(Vacancy(
                title=title,
                company=company,
                salary=salary,
                description=description,
                link=link
            ))
        return vacancies

    def save_vacancies(self, vacancies):
        """
        Сохранение списка вакансий в Джейсон
        """
        self.write([vacancy.__dict__ for vacancy in vacancies])

    def delete_vacancy(self, vacancy):
        """
        Удаление вакансий из Джейсона
        """
        data = self.read()
        data = [v for v in data if v['title'] != vacancy.title or v['company'] != vacancy.company]
        self.write(data)

    def find_vacancies_with_keyword(self, keyword):
        """
        Поиск вакансий по ключслову в описании
        """
        data = self.read()
        matching_vacancies = []
        for vacancy in data:
            description = vacancy.get('description', '')
            if description and keyword.lower() in description.lower():
                matching_vacancies.append(Vacancy(
                    title=vacancy.get('title', ''),
                    company=vacancy.get('company', ''),
                    salary=vacancy.get('salary', 'Не указана'),
                    description=vacancy.get('description', ''),
                    link=vacancy.get('link', '')
                ))
        return matching_vacancies
