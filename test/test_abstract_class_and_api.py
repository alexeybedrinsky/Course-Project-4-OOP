import pytest
import requests
from unittest.mock import patch
from src.Abstract_class_and_API import HeadHunterAPI

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

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python developer")
    assert len(vacancies) > 0
    assert vacancies[0]['id'] == "102058778"

# Тестирование ошибки при выполнении запроса
def test_request_failure(mock_requests_get):
    mock_requests_get.return_value.status_code = 404
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

    api = HeadHunterAPI()
    with pytest.raises(requests.exceptions.HTTPError):
        api.get_vacancies("Python developer")
