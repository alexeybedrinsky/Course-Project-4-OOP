import requests
import json
import os
from abc import ABC, abstractmethod

# Абстрактный класс для работы с файлами
class FileHandler(ABC):
    """
    Абстрактный класс для обработки файлов.
    """
    @abstractmethod
    def read(self):
        """
        Чтение данных из файла.
        """
        pass

    @abstractmethod
    def write(self, data):
        """
        Запись данных в файл.
        """
        pass

    @abstractmethod
    def append(self, data):
        """
        Добавление данных в файл.
        """
        pass


class JSONFileHandler(FileHandler):
    """
    Класс для обработки JSON файлов.
    """
    def __init__(self, filename):
        self._filename = filename

    def read(self):
        """
        Чтение данных из JSON файла.
        :return: Данные из файла или пустой список, если файл не существует или содержит некорректные данные.
        """
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Если файл пуст или содержит некорректные данные -> возвращаем пустой список
                return []
        return []

    def write(self, data):
        """
        Запись данных в файл.
        """
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def append(self, data):
        """
        Добавление данных в файл.
        """
        current_data = self.read()
        current_data.extend(data)
        self.write(current_data)

# URL API для поиска вакансий на hh.ru
url = 'https://api.hh.ru/vacancies'

# Параметры запроса
params = {
    'text': 'Python developer',  # Ключевые слова для поиска
    'area': 1,  # Регион (1 - Москва)
    'page': 0,  # Номер страницы (начинаем с 0)
    'per_page': 10  # Количество вакансий на одной странице
}

# Выполнение GET запроса
response = requests.get(url, params=params)

# Проверка успешности запроса
if response.status_code == 200:
    vacancies = response.json().get('items', [])

    # Абсолютный путь к файлу JSON
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'vacancies.json')

    # Создание объекта JSONFileHandler
    json_handler = JSONFileHandler(json_path)

    # Добавление данных в файл JSON
    json_handler.append(vacancies)

    print(f"Данные успешно добавлены в файл {json_path}")
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
