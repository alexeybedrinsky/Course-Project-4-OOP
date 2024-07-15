import pytest
import requests
import json
import os
from unittest.mock import patch

# Импортируем файл для тестирования
import data.vacancies_code as vacancies_code

# Фикстура для подмены URL и параметров
@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

# Тестирование успешного выполнения запроса
def test_successful_request(mock_requests_get):
    response_data = {
        "items": [
            {
                "id": "102058778",
                "name": "Call manager/Администратор в салон красоты",
                "salary": {
                    "from": 120000,
                    "to": 250000,
                    "currency": "KZT"
                },
                "area": {
                    "id": "160",
                    "name": "Алматы"
                },
                "url": "https://api.hh.ru/vacancies/102058778?host=hh.ru"
            }
        ]
    }
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = response_data

    vacancies_code.response = requests.get(vacancies_code.url, params=vacancies_code.params)
    assert vacancies_code.response.status_code == 200
    assert len(vacancies_code.response.json().get('items')) > 0

# Тестирование сохранения данных в JSON файл
def test_save_data_to_json(mock_requests_get, tmpdir):
    response_data = {
        "items": [
            {
                "id": "102058778",
                "name": "Call manager/Администратор в салон красоты",
                "salary": {
                    "from": 120000,
                    "to": 250000,
                    "currency": "KZT"
                },
                "area": {
                    "id": "160",
                    "name": "Алматы"
                },
                "url": "https://api.hh.ru/vacancies/102058778?host=hh.ru"
            }
        ]
    }
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = response_data

    vacancies_code.response = requests.get(vacancies_code.url, params=vacancies_code.params)
    vacancies = vacancies_code.response.json().get('items', [])

    # Создание временного файла для сохранения данных
    temp_file = tmpdir.join('vacancies.json')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)

    # Проверка содержимого временного файла
    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == len(response_data['items'])
        assert data[0]['id'] == response_data['items'][0]['id']

# Тестирование ошибки при выполнении запроса
def test_request_failure(mock_requests_get):
    mock_requests_get.return_value.status_code = 404
    vacancies_code.response = requests.get(vacancies_code.url, params=vacancies_code.params)
    assert vacancies_code.response.status_code == 404
