import os
from functools import partial
from typing import Callable

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hh_vacancy_salaries(language: str) -> tuple[int, list]:
    api_url = "https://api.hh.ru/"
    salaries = []
    page = 0
    while True:
        params = {
            "text": f"программист {language}",
            "area": 1,
            "per_page": 100,
            "page": page,
        }
        response = requests.get(f"{api_url}vacancies", params=params)
        response.raise_for_status()
        response_content = response.json()
        for vacancy in response_content["items"]:
            salary_description = vacancy["salary"]
            if salary_description and salary_description["currency"] == "RUR":
                salary = (salary_description["from"], salary_description["to"])
                salaries.append(salary)
        page += 1
        if page == response_content["pages"]:
            break

    return (response_content["found"], salaries)


def get_sj_vacancy_salaries(language: str, api_token: str) -> tuple[int, list]:
    api_url = "https://api.superjob.ru/2.0/"
    headers = {
        "X-Api-App-Id": api_token,
    }
    salaries = []
    page = 0
    while True:
        params = {
            "town": "Москва",
            "keyword": f"программист {language}",
            "count": 100,
            "page": page,
        }
        response = requests.get(
            f"{api_url}vacancies/", headers=headers, params=params)
        response.raise_for_status()
        response_content = response.json()
        for vacancy in response_content["objects"]:
            if vacancy["currency"] == "rub":
                salary = (vacancy["payment_from"], vacancy["payment_to"])
                salaries.append(salary)
        page += 1
        if not response_content["more"]:
            break

    return (response_content["total"], salaries)


def predict_salary(
    salary_from: float | None,
    salary_to: float | None
) -> float | None:
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def calc_statistics(
    languages: tuple,
    func_get_salaries: Callable[[str], tuple[int, list]]
) -> dict:
    vacancy_statistics = {}
    for language in languages:
        vacancies_found, salaries = func_get_salaries(language)
        language_stat = {}
        language_stat["vacancies_found"] = vacancies_found
        count = 0
        salary_sum = 0
        for salary_from, salary_to in salaries:
            salary = predict_salary(salary_from, salary_to)
            if salary:
                salary_sum += salary
                count += 1
        language_stat["vacancies_processed"] = count
        language_stat["average_salary"] = int(
            salary_sum / count) if count else 0
        vacancy_statistics[language] = language_stat
    return vacancy_statistics


def get_statistics_table(statistics: dict, title: str) -> str:
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ],
    ]
    for language in statistics:
        table_data.append([
            language,
            statistics[language]["vacancies_found"],
            statistics[language]["vacancies_processed"],
            statistics[language]["average_salary"],
        ])
    table = AsciiTable(table_data)
    table.title = title

    return table.table


if __name__ == "__main__":
    load_dotenv()
    sj_api_token = os.getenv("SJ_API_TOKEN")

    languages = (
        "Python",
        "JavaScript",
        "Java",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "Go",
        "Scala",
        "Swift",
        "1С",
    )

    try:
        hh_statistics = calc_statistics(languages, get_hh_vacancy_salaries)
        print(get_statistics_table(hh_statistics, "HeadHunter Moscow"))
    except requests.exceptions.HTTPError as error:
        error_text = f"{error.response.status_code} {error.response.reason}"
        print(f"Get vacancies from hh.ru\n \
                Something went wrong: {error_text}")
    except requests.exceptions.Timeout:
        print(f"Get vacancies from hh.ru\nError: Timeout expired")

    try:
        get_salaries = partial(get_sj_vacancy_salaries, api_token=sj_api_token)
        sj_statistics = calc_statistics(languages, get_salaries)
        print(get_statistics_table(sj_statistics, "SuperJob Moscow"))
    except requests.exceptions.HTTPError as error:
        error_text = f"{error.response.status_code} {error.response.reason}"
        print(f"Get vacancies from SuperJob.ru\n \
                Something went wrong: {error_text}")
    except requests.exceptions.Timeout:
        print(f"Get vacancies from SuperJob.ru\nError: Timeout expired")
