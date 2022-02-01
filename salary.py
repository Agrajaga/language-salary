import os
from functools import partial
from typing import Callable

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_vacancies_hh(language: str, api_url: str) -> tuple[int, list]:
    vacancies = []
    page = 0
    while True:
        params = {
            "text": f"программист {language}",
            "area": 1,
            # "only_with_salary" : True,
            "per_page": 100,
            "page": page,
        }
        response = requests.get(f"{api_url}vacancies", params=params)
        response.raise_for_status()
        json_response = response.json()
        vacancies.extend(json_response["items"])
        page += 1
        if page == json_response["pages"]:
            break

    return (json_response["found"], vacancies)


def get_vacancies_sj(language: str, api_token: str, api_url: str) -> tuple[int, list]:
    headers = {
        "X-Api-App-Id": api_token,
    }
    vacancies = []
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
        json_response = response.json()
        vacancies.extend(json_response["objects"])
        if json_response["more"]:
            page += 1
        else:
            break

    return (json_response["total"], vacancies)


def get_currency_rates(url: str) -> dict:
    currencies = {}
    response = requests.get(f"{url}dictionaries")
    response.raise_for_status()

    for currency in response.json()["currency"]:
        currencies[currency["code"]] = currency["rate"]
    return currencies


def predict_salary(
    salary_from: float | None,
    salary_to: float | None
) -> float | None:
    if salary_from and salary_to:
        raw_salary = (salary_from + salary_to) / 2
    elif salary_from:
        raw_salary = salary_from * 1.2
    elif salary_to:
        raw_salary = salary_to * 0.8
    else:
        return None
    return raw_salary


def predict_rub_salary_hh(vacancy: dict, currency_rates: dict) -> float | None:
    salary_description = vacancy["salary"]
    if not salary_description:
        return
    raw_salary = predict_salary(
        salary_description["from"], salary_description["to"])
    if raw_salary:
        return raw_salary / currency_rates[salary_description["currency"]]


def predict_rub_salary_sj(vacancy: dict) -> float | None:
    if vacancy["currency"] != "rub":
        return None

    return predict_salary(vacancy["payment_from"], vacancy["payment_to"])


def calc_statistics(
    languages: tuple,
    func_get_vacancies: Callable[[str], tuple[int, list]],
    func_predict_salary: Callable[[dict], float | None]
) -> dict:
    vacancy_statistics = {}
    for language in languages:
        vacancies_found, vacancies = func_get_vacancies(language)
        language_stat = {}
        language_stat["vacancies_found"] = vacancies_found
        count = 0
        salary_sum = 0
        for vacancy in vacancies:
            salary = func_predict_salary(vacancy)
            if salary:
                salary_sum += salary
                count += 1
        language_stat["vacancies_processed"] = count
        language_stat["average_salary"] = int(salary_sum / count)
        vacancy_statistics[language] = language_stat
    return vacancy_statistics


def calc_hh_statistics(languages: tuple) -> dict:
    hh_api_url = "https://api.hh.ru/"

    currency_rates = get_currency_rates(url=hh_api_url)
    predict_salary = partial(predict_rub_salary_hh,
                             currency_rates=currency_rates)
    get_vacancies = partial(get_vacancies_hh,
                            api_url=hh_api_url)
    return calc_statistics(languages, get_vacancies, predict_salary)


def calc_sj_statistics(languages: tuple, api_token: str) -> dict:
    sj_api_url = "https://api.superjob.ru/2.0/"

    get_vacancies = partial(get_vacancies_sj,
                            api_token=api_token,
                            api_url=sj_api_url)
    return calc_statistics(languages, get_vacancies, predict_rub_salary_sj)


def tabled_statistics(statistics: dict, title: str) -> str:
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
        hh_statistics = calc_hh_statistics(languages)
        print(tabled_statistics(hh_statistics, "HeadHunter Moscow"))
    except requests.exceptions.HTTPError as error:
        error_text = f"{error.response.status_code} {error.response.reason}"
        print(f"Get vacancies from hh.ru\n \
                Something went wrong: {error_text}")
    except requests.exceptions.Timeout:
        print(f"Get vacancies from hh.ru\nError: Timeout expired")

    try:
        sj_statistics = calc_sj_statistics(languages, sj_api_token)
        print(tabled_statistics(sj_statistics, "SuperJob Moscow"))
    except requests.exceptions.HTTPError as error:
        error_text = f"{error.response.status_code} {error.response.reason}"
        print(f"Get vacancies from SuperJob.ru\n \
                Something went wrong: {error_text}")
    except requests.exceptions.Timeout:
        print(f"Get vacancies from SuperJob.ru\nError: Timeout expired")
