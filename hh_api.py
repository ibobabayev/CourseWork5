import requests
import json

result = None
def hh_api():
    text = input("Выберите профессию: ")
    per_page = int(input("Введите желаемое количество результатов вакансии: "))
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": text,
        "areas": 113,
        "per_page": per_page
    }
    response = requests.get(url, params=params)
    user_vacancies = {}
    new_dict_list = []
    if response.status_code == 200:
        data = response.json()
        vacancies = {i: data[i] for i in ["items"]}
        # with open("new.json", 'w', encoding="utf-8") as file:
        #     json.dump(data, file, ensure_ascii=False, indent=4)
        if per_page is not None:
            counter = 0
            while True:
                for vacancy in vacancies["items"]:
                    if counter < per_page and vacancy.get("salary") is not None:
                        if isinstance(vacancy.get("salary", {}).get("from"), int) and isinstance(vacancy.get("salary", {}).get("to"), int):
                            if vacancy.get("salary", {}).get("currency") == 'RUR':
                                counter += 1
                                vacancy_id = vacancy.get("id")
                                vacancy_title = vacancy.get("name")
                                vacancy_url = vacancy.get("alternate_url")
                                vacancy_experience = vacancy.get("experience", {}).get("name")
                                company_name = vacancy.get("employer", {}).get("name")
                                vacancy_description = "Нету описания"
                                vacancy_currency = vacancy.get("salary", {}).get("currency")
                                vacancy_salary = int((vacancy.get("salary", {}).get("from")+vacancy.get("salary", {}).get("to"))/2)
                                if vacancy.get("address") is not None:
                                    if vacancy.get("address", {}).get("description") is not None:
                                        vacancy_description = vacancy.get("address", {}).get("description")
                                    else:
                                        vacancy_description = "Нету описания"

                                items = f'"ID": {vacancy_id},"Должность": {vacancy_title},"Ссылка": {vacancy_url},"Компания" :{company_name},"Зарплата": {vacancy_salary},"Валюта": {vacancy_currency},"Описание": {vacancy_description},"Опыт": {vacancy_experience}'
                                user_vacancies[items] = result
                                new_dict = {'ID': vacancy_id, 'Должность': vacancy_title, 'Ссылка': vacancy_url, 'Компания': company_name, 'Зарплата': vacancy_salary, 'Валюта': vacancy_currency, 'Описание': vacancy_description, 'Опыт': vacancy_experience}
                                new_dict_list.append(new_dict)
                else:
                    break
        with open("hh.json", 'w', encoding="utf-8") as file:
            json.dump(new_dict_list, file, ensure_ascii=False, indent=4)
        return user_vacancies
    else:
        print(f"Request failed with status code: {response.status_code}")
