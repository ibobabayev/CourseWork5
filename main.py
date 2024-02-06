from DBManager import DBManager
from hh_api import hh_api


def main():
    print("Добро пожаловать в программу по поиску вакансий на сайте hh.ru")
    hh_api()
    db = DBManager()
    db.create_database()
    print('База Данных "course_work" успешна создана')
    db.create_table()
    print('Таблица "head_hunter_vacancies" успешна создана')
    db.insert_into_table()
    print('Таблица "head_hunter_vacancies" заполнена данными')
    print("Если вы хотите посмотреть список всех вакансий,то нажмите на '1'.если вы хотите искать вакансии по ключевому слову,то нажмите на '2'")
    choice = input()
    if choice == '1':
        print(f'Список всех вакансий: {db.get_all_vacancies()}')
    elif choice == '2':
        word = input("Введите ключевое слово для поиска ").title()
        print(db.get_vacancies_with_keyword(word))
    else:
        print("Вы нажали неправильную кнопку,если хотите выйти,то нажмите на '1',а если хотите вернуться к поиску,то нажмите на '2'")
        choice2 = input()
        if choice2 == '1':
            quit()
        elif choice2 == '2':
             main()

    print(f'Список компаний с количеством их вакансий: {db.get_companies_and_vacancies_count()}')
    print(f"Средняя зарплата по данным вакансиям: {db.get_avg_salary()} рублей")
    print(f"Вакансии,зарплата которых больше среднего: {db.get_vacancies_with_higher_salary()}")


if __name__ == '__main__':
    main()
