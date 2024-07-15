import pytest
import os
import json
from src.JSONVacancyStorage import JSONVacancyStorage
from src.Vacancy import Vacancy


@pytest.fixture(scope='function')
def setup_vacancy_storage():
    file_path = 'test_vacancies.json'
    storage = JSONVacancyStorage(file_path)
    test_vacancies = [
        Vacancy(
            title='Test Vacancy 1',
            company='Test Company 1',
            salary='50000',
            description='This is a test vacancy 1',
            link='http://test1.com'
        ),
        Vacancy(
            title='Test Vacancy 2',
            company='Test Company 2',
            salary='60000',
            description='This is a test vacancy 2',
            link='http://test2.com'
        )
    ]
    test_data = [
        {
            'title': 'Test Vacancy 1',
            'company': 'Test Company 1',
            'salary': '50000',
            'description': 'This is a test vacancy 1',
            'link': 'http://test1.com'
        },
        {
            'title': 'Test Vacancy 2',
            'company': 'Test Company 2',
            'salary': '60000',
            'description': 'This is a test vacancy 2',
            'link': 'http://test2.com'
        }
    ]

    yield storage, test_vacancies, test_data, file_path

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass


def test_get_vacancies(setup_vacancy_storage):
    storage, _, test_data, file_path = setup_vacancy_storage
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, ensure_ascii=False, indent=4)

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0].title == 'Test Vacancy 1'
    assert vacancies[1].title == 'Test Vacancy 2'


def test_save_vacancies(setup_vacancy_storage):
    storage, test_vacancies, _, file_path = setup_vacancy_storage
    storage.save_vacancies(test_vacancies)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    assert len(data) == 2
    assert data[0]['title'] == 'Test Vacancy 1'
    assert data[1]['title'] == 'Test Vacancy 2'


def test_delete_vacancy(setup_vacancy_storage):
    storage, test_vacancies, test_data, file_path = setup_vacancy_storage
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, ensure_ascii=False, indent=4)

    vacancy_to_delete = test_vacancies[0]
    storage.delete_vacancy(vacancy_to_delete)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]['title'] == 'Test Vacancy 2'


def test_find_vacancies_with_keyword(setup_vacancy_storage):
    storage, _, test_data, file_path = setup_vacancy_storage
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, ensure_ascii=False, indent=4)

    matching_vacancies = storage.find_vacancies_with_keyword('test vacancy 1')
    assert len(matching_vacancies) == 1
    assert matching_vacancies[0].title == 'Test Vacancy 1'
