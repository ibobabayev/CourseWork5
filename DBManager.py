import psycopg2
import json
from config import config


class DBManager:
    """Класс для подключения к БД PostgreSQL"""
    def __init__(self):
        self.params = config()
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True

        self.cur = self.conn.cursor()

    def create_database(self):
        """Функция для создания базы данных"""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(f"""drop database if exists course_work""")
        self.cur.execute(f"""create database course_work""")

    def create_table(self):
        """Функция для создания таблицу"""
        self.params.update({'dbname': 'course_work'})
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(f"""drop table if exists head_hunter_vacancies """)
        self.cur.execute(f"""create table head_hunter_vacancies (
                vacancy_id int,
                vacancy_title text,
                vacancy_url text,
                vacancy_experience text,
                company_name text,
                vacancy_salary int,
                vacancy_currency text,
                vacancy_description text)""")

    def insert_into_table(self):
        """Функция, которая получает данные с JSON файла и вставления их в таблицу"""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        with open('hh.json', 'r',encoding="utf-8") as file:
            data = json.load(file)
            for row in data:
                self.cur.execute(f"""insert into head_hunter_vacancies (vacancy_id,vacancy_title,vacancy_url,
                company_name,vacancy_salary,vacancy_currency,vacancy_description,vacancy_experience) 
                values(%s,%s,%s,%s,%s,%s,%s,%s)""", (row['ID'], row["Должность"], row["Ссылка"],
                                                                   row["Компания"], row["Зарплата"], row["Валюта"],
                                                                   row["Описание"], row["Опыт"]))

    def get_companies_and_vacancies_count(self):
        """Функция возвращает список всех компаний и количество вакансий у каждой компании."""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(f"""select company_name,count(*) from head_hunter_vacancies
        group by company_name""")
        data = self.cur.fetchall()
        new_list = []
        for row in data:
            new_list.append(row)
        return new_list
    def get_all_vacancies(self):
        """Функция возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(f"""select company_name,vacancy_title,vacancy_salary,vacancy_url from head_hunter_vacancies""")
        data = self.cur.fetchall()
        new_list = []
        for row in data:
            new_list.append(row)
        return new_list
    def get_avg_salary(self):
        """Функция возвращает среднюю зарплату по вакансиям"""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(f"""select avg(vacancy_salary) from head_hunter_vacancies""")
        data = self.cur.fetchall()
        return round(data[0][0])

    def get_vacancies_with_higher_salary(self):
        """ Функция возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(
            f"""select vacancy_title,vacancy_salary from head_hunter_vacancies where vacancy_salary > (select avg(vacancy_salary) from head_hunter_vacancies) order by vacancy_salary""")
        data = self.cur.fetchall()
        higher_salary_vacancies = []
        for i in data:
            higher_salary_vacancies.append(i)
        return higher_salary_vacancies

    def get_vacancies_with_keyword(self, word):
        """ Функция возвращает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(f"""select vacancy_title,company_name,vacancy_salary,vacancy_description from head_hunter_vacancies
        where vacancy_title like '%{word}%'""")
        rows = self.cur.fetchall()
        new_list=[]
        if rows:
            print("По вашему запросу нашлись следующие вакансии с названием вакансии,названием работодателя,зарплатой и описанием")
            for row in range(len(rows)):
                new_list.append(rows[row])
            return new_list
        else:
            return "Нету подходящих результатов"
