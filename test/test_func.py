import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем путь к src в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from func import interact_with_user
from Vacancy import Vacancy
from JSONVacancyStorage import JSONVacancyStorage
from Abstract_class_and_API import HeadHunterAPI

@patch('builtins.input', side_effect=["Python developer", "3", "опыт"])
@patch('func.HeadHunterAPI.get_vacancies', new_callable=MagicMock)
@patch('func.JSONVacancyStorage.save_vacancies', new_callable=MagicMock)
@patch('func.JSONVacancyStorage.find_vacancies_with_keyword', new_callable=MagicMock)
def test_interact_with_user(mock_find, mock_save, mock_get_vacancies, mock_input):
    mock_get_vacancies.return_value = [
        {
            'name': 'Python Developer',
            'employer': {'name': 'Some Company'},
            'salary': {'from': 100000, 'to': 150000, 'currency': 'руб.'},
            'snippet': {'requirement': 'Опыт работы с Python'},
            'alternate_url': 'http://example.com'
        },
        {
            'name': 'Java Developer',
            'employer': {'name': 'Another Company'},
            'salary': {'from': 120000, 'to': 180000, 'currency': 'руб.'},
            'snippet': {'requirement': 'Опыт работы с Java'},
            'alternate_url': 'http://example.com'
        },
        {
            'name': 'C++ Developer',
            'employer': {'name': 'Yet Another Company'},
            'salary': {'from': 110000, 'to': 160000, 'currency': 'руб.'},
            'snippet': {'requirement': 'Опыт работы с C++'},
            'alternate_url': 'http://example.com'
        }
    ]

    mock_find.return_value = [
        Vacancy("Python Developer", "Some Company", "100000 - 150000 руб.", "Опыт работы с Python", "http://example.com"),
        Vacancy("Java Developer", "Another Company", "120000 - 180000 руб.", "Опыт работы с Java", "http://example.com")
    ]

    with patch('builtins.print') as mock_print:
        interact_with_user("vacancies.json")

    # Проверка вызовов методов
    mock_get_vacancies.assert_called_once_with("Python developer", per_page=100)
    assert mock_save.called
    assert mock_find.called

    # Проверка вывода
    mock_print.assert_any_call("Топ 3 вакансий по зарплате:")
    mock_print.assert_any_call("Vacancy(title=Java Developer, company=Another Company, salary=120000 - 180000 руб., description=Опыт работы с Java, link=http://example.com)")
    mock_print.assert_any_call("Vacancy(title=C++ Developer, company=Yet Another Company, salary=110000 - 160000 руб., description=Опыт работы с C++, link=http://example.com)")
    mock_print.assert_any_call("Vacancy(title=Python Developer, company=Some Company, salary=100000 - 150000 руб., description=Опыт работы с Python, link=http://example.com)")
    mock_print.assert_any_call("Вакансии с ключевым словом 'опыт' в описании:")
    mock_print.assert_any_call("Vacancy(title=Python Developer, company=Some Company, salary=100000 - 150000 руб., description=Опыт работы с Python, link=http://example.com)")
    mock_print.assert_any_call("Vacancy(title=Java Developer, company=Another Company, salary=120000 - 180000 руб., description=Опыт работы с Java, link=http://example.com)")

if __name__ == "__main__":
    pytest.main()
