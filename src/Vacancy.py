class Vacancy:
    """класс вакансии"""

    __slots__ = ["__name", "__salary", "__url", "__id", "__employer_name", "__employer_link"]

    def __init__(self,
                 name: str,
                 salary: float,
                 url: str,
                 id_: str,
                 employer_name: str,
                 employer_link: str) -> None:

        self.__name = name
        self.__salary = self.__salary_not_none(salary)
        self.__url = url
        self.__id = id_
        self.__employer_name = self.__employer_not_none(employer_name)
        self.__employer_link = self.__employer_not_none(employer_link)

    @staticmethod
    def __salary_not_none(salary: float | None) -> float:
        """валидатор зарплаты"""
        if salary is None:
            return 0.0
        return salary

    @staticmethod
    def __employer_not_none(employer: str | None) -> str:
        """валидатор зарплаты"""
        if employer is None:
            return "не указан"
        return employer

    def __lt__(self, other: "Vacancy") -> bool:
        return self.salary < other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        return self.salary > other.salary

    @classmethod
    def build_vacancies(cls, data: dict) -> "Vacancy":
        """преврощает словарь в вакансию"""
        salary = data.get("salary")
        employer = data.get("employer")
        employer_link = None
        if employer is None:
            employer = None
        else:
            employer, employer_link = employer.get("name"), employer.get("alternate_url")
        if salary is not None:
            if salary.get("to") is None:
                salary = salary.get("from")
            else:
                salary = salary.get("to")

        return cls(
            data.get("name", "notFound"),
            salary,
            data.get("alternate_url", "notFound"),
            data.get("id", "notFound"),
            employer,
            employer_link
        )

    @property
    def name(self) -> str:
        return self.__name

    @property
    def salary(self) -> float:
        return self.__salary

    @property
    def url(self) -> str:
        return self.__url

    @property
    def id(self) -> str:
        return self.__id

    @property
    def employer_name(self) -> str:
        return self.__employer_name

    @property
    def employer_link(self) -> str:
        return self.__employer_link