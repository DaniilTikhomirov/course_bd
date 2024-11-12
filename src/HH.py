from abc import ABC, abstractmethod
from decimal import Decimal
from progress.bar import IncrementalBar
from typing import Any

import requests

class Parser(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> None:
        pass



class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: Any = {"text": "", "page": 0, "per_page": 100, "search_fields": ["skills", "title"]}
        self.__vacancies: list[dict] = []
        self.__ids: list[int] = []

    def __contains(self, vacancy: list) -> None:
        """добавление в лист только тех вакансий которые не повторялись"""
        for vac2 in vacancy:
            if vac2["id"] not in self.__ids:
                self.__ids.append(vac2["id"])
                self.__vacancies.append(vac2)

    def __connect_api(self) -> None:
        """подключение к апи"""
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            vacancies = response.json()["items"]
            self.__contains(vacancies)

    def load_vacancies(self, keyword: str, n: int = 5) -> None:
        """загрузка вакансий в список"""
        self.__params["text"] = keyword
        bar = IncrementalBar("Parse", max=n)
        while self.__params.get("page") != n:
            self.__connect_api()
            self.__params["page"] += 1
            bar.next()
        bar.finish()



    @property
    def url(self) -> str:
        return self.__url

    @property
    def vacancies(self) -> list:
        return self.__vacancies

    @vacancies.setter
    def vacancies(self, data: list) -> None:
        self.__vacancies = data
