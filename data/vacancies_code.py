import requests
import json
import os

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

    # Сохранение данных в файл JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)

    print(f"Данные успешно записаны в файл {json_path}")
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")

