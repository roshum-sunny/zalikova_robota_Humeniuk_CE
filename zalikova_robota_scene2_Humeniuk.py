import csv
from abc import ABC, abstractmethod
from typing import List

# Створюємо батьківський клас, від якого інші класи будуть наслідувати
class SchoolEmployee:
    def __init__(self, last_name: str, first_name: str, middle_name: str, base_salary:float) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.base_salary = base_salary

# Використовуємо абстрактний клас щоб розрахувати зарплату
    @abstractmethod
    def calculate_employee_salary(self) -> float:
        pass

# Cтворюємо метод, який нам буде повертати інформацію про працівників школи.
    def get_info(self) -> dict:
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "base_salary": self.base_salary,
            "bonus_salary": self.calculate_employee_salary()
        }

# Клас для Директора школи
class Headmaster(SchoolEmployee):
    def __init__(self, last_name: str, first_name: str, middle_name: str, base_salary:float, teaching_experience: int, leadership_experience: int ) -> None:
        super().__init__(last_name, first_name, middle_name, base_salary)
        self.teaching_experience = teaching_experience
        self.leadership_experience = leadership_experience

# Реалізуємо метод зарплати для директора
    def calculate_employee_salary(self) -> float:
        return ((self.base_salary * self.teaching_experience) / 50) + (self.leadership_experience * 500)

# Використовуємо метод super() щоб дочірній клас міг звернутися до оригінального методу.
    def get_info(self) -> dict:
        info = super().get_info()
        info["teaching_experience"] = self.teaching_experience
        info["leadership_experience"] = self.leadership_experience
        info["position"] = "Директор"
        return info

class Teacher(SchoolEmployee):
    def __init__(self, last_name: str, first_name: str, middle_name: str, base_salary: float, teaching_experience: int) -> None:
        super().__init__(last_name, first_name, middle_name, base_salary)
        self.teaching_experience = teaching_experience

    def calculate_employee_salary(self) -> float:
        return (self.base_salary * self.teaching_experience) / 30

    def get_info(self) -> dict:
        info = super().get_info()
        info["teaching_experience"] = self.teaching_experience
        info["position"] = "Вчитель школи"
        return info

class SecurityGuard(SchoolEmployee):
    def __init__(self, last_name: str, first_name: str, middle_name: str, base_salary: float, job_experience: float) -> None:
        super().__init__(last_name, first_name, middle_name, base_salary)
        self.job_experience = job_experience

    def calculate_employee_salary(self) -> float:
        return self.base_salary + self.job_experience * 250

    def get_info(self) -> dict:
        info = super().get_info()
        info['job_experience'] = self.job_experience
        info['position'] = "Охоронець"
        return info

class SalaryManager:
    def __init__(self) -> None:
        self.school_employees: List[SchoolEmployee] = []

    def new_employee(self, school_employee: SchoolEmployee) -> None:
        self.school_employees.append(school_employee)

# Метод який розраховує зарплати для всіх працівників.
    def calculate_all_salaries(self) -> List[dict]:
        return [school_employee.get_info() for school_employee in self.school_employees]

    def save_to_csv(self) -> None:
        salaries_data = self.calculate_all_salaries()
        all_fields = set()
        for record in salaries_data:
            all_fields.update(record.keys())

        fieldnames = ["last_name", "first_name", "middle_name", "position", "base_salary", "bonus_salary"]
        unique_fields = ["teaching_experience", "leadership_experience", "job_experience"]
        for field in unique_fields:
            if field in all_fields:
                fieldnames.append(field)


        with open("salaries.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames= fieldnames)
            writer.writeheader()
            writer.writerows(salaries_data)
        print("Дані збережені!")


    def display_salaries(self) -> None:
        salaries_data = self.calculate_all_salaries()
        print(f"{"Прізвище":<15} {"Ім'я":<15} {"По-Батькові":<15} {"Посада":<15} {"Базова зарплата":<15} {"Бонусні Зарплати":<15}")
        for record in salaries_data:
            last_name = record["last_name"]
            first_name = record["first_name"]
            middle_name = record["middle_name"]
            position = record["position"]
            base_salary = record["base_salary"]
            bonus_salary = record["bonus_salary"]
            print(f"{last_name:<15} {first_name:<15} {middle_name:<15} {position:<15} {base_salary:<15} {bonus_salary:<10.2f}")
        print(f"Всього працівників: {len(salaries_data)}")

# Приклад роботи системи

salary_man = SalaryManager()

headmaster = Headmaster(
            last_name= "Новоселецький",
            first_name= "Геннадій",
            middle_name= "Юрійовч",
            base_salary= 15000,
            teaching_experience= 30,
            leadership_experience= 15
        )
teacher1 = Teacher(
last_name="Галабурда",
first_name="Дмитро",
middle_name="Юрійович",
base_salary=12000,
teaching_experience=10,
    )
teacher2 = Teacher(
last_name="Опанасівна",
first_name="Ніна",
middle_name="Володимирівна",
base_salary=12000,
teaching_experience=45,
    )
teacher3 = Teacher(
last_name="Козловський",
first_name="Ігор",
middle_name="Олексійович",
base_salary=12000,
teaching_experience=14,
    )
security_guard = SecurityGuard(
last_name="Теремкова",
first_name="Світлана",
middle_name="Василівна",
base_salary=11000,
job_experience=7
    )
salary_man.new_employee(headmaster)
salary_man.new_employee(teacher1)
salary_man.new_employee(teacher2)
salary_man.new_employee(teacher3)
salary_man.new_employee(security_guard)
salary_man.display_salaries()
salary_man.save_to_csv()






