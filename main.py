from src.Vacancy import fetch_and_save_vacancies, get_top_vacancies_by_salary, search_vacancies_by_keyword


def main():
    """
    Основная функция программы для работы с вакансиями.

    Выполняет следующие действия:
    1. Запрашивает у пользователя поисковый запрос для получения вакансий с hh.ru.
    2. Получает и сохраняет вакансии в JSON.
    3. Выводит топ N вакансий по зарплате.
    4. Ищет вакансии по ключевому слову в описании.
    Файл для хранения вакансий: "data/vacancies.json"
    """
    file_path = "data/vacancies.json"

    query = input("Введите поисковый запрос для запроса вакансий с hh.ru: ")
    vacancies = fetch_and_save_vacancies(file_path, query)

    try:
        top_n = int(input("Введите количество вакансий для вывода топ N по зарплате: "))
    except ValueError:
        print("Ошибка: введите числовое значение.")
        return

    sorted_vacancies = get_top_vacancies_by_salary(vacancies, top_n)
    print(f"Топ {top_n} вакансий по зарплате:")
    for vacancy in sorted_vacancies:
        print(vacancy)

    keyword = input("Введите ключевое слово для поиска вакансий по описанию: ")
    matching_vacancies = search_vacancies_by_keyword(file_path, keyword)
    print(f"Вакансии с ключевым словом '{keyword}' в описании:")
    for vacancy in matching_vacancies:
        print(vacancy)


if __name__ == "__main__":
    main()
