import os

from progress.bar import IncrementalBar

from src.Vacancy import Vacancy
from src.HH import HeadHunterAPI
from src.DBManager import DBManager
from config.config import config

def main():
    params = config()

    hh = HeadHunterAPI()
    job_name = input("which job would you like to run? : ")
    pages = int(input("how many pages would you like to run? >=20: "))
    if pages > 20 or pages < 1:
        print("not valid number your number = 1")
        pages = 1
    hh.load_vacancies(job_name, pages)
    bd_name = input("which bd would you like to run? : ")
    bd = DBManager(bd_name, params)
    table_name = input("which table would you like to run? : ")
    bd.create_table(table_name)
    vacancies = []
    hh_vacancies = hh.vacancies
    bar = IncrementalBar("processing Data", max=len(hh_vacancies))
    for vacancy in hh_vacancies:
        vacancies.append(Vacancy.build_vacancies(vacancy))
        bar.next()
    bar.finish()
    bd.add_list_to_table(table_name, vacancies)
    if input("get all employer [y/n] ").lower().strip() == "y":
        print(bd.get_companies_and_vacancies_count(table_name))
    if input("get all vacancy [y/n] ").lower().strip() == "y":
        print(bd.get_all_vacancies(table_name))
    if input("get average salary [y/n] ").lower().strip() == "y":
        print(bd.get_avg_salary(table_name))
    if input("get higher vacancy [y/n] ").lower().strip() == "y":
        print(bd.get_vacancies_with_higher_salary(table_name))
    if input("get vacancy with word [y/n] ").lower().strip() == "y":
        word = input("your word : ")
        print(bd.get_vacancies_with_keyword(table_name=table_name, word=word))


if __name__ == "__main__":
    main()
