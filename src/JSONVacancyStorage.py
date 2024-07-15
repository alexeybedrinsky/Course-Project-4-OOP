import json
from src.Vacancy import Vacancy

class JSONVacancyStorage:
    def __init__(self, file_path='data/vacancies.json'):
        self.file_path = file_path

    def get_vacancies(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

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
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return []
        except json.JSONDecodeError:
            print("Error: JSON decode error. Please check the JSON file format.")
            return []

    def save_vacancies(self, vacancies):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([vacancy.__dict__ for vacancy in vacancies], file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data = [v for v in data if v['title'] != vacancy.title or v['company'] != vacancy.company]

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def find_vacancies_with_keyword(self, keyword):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            matching_vacancies = []
            for vacancy in data:
                if keyword.lower() in vacancy.get('description', '').lower():
                    matching_vacancies.append(Vacancy(
                        title=vacancy.get('title', ''),
                        company=vacancy.get('company', ''),
                        salary=vacancy.get('salary', 'Не указана'),
                        description=vacancy.get('description', ''),
                        link=vacancy.get('link', '')
                    ))
            return matching_vacancies
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return []
        except json.JSONDecodeError:
            print("Error: JSON decode error. Please check the JSON file format.")
            return []
