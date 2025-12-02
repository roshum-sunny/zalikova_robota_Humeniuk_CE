# Крок 1: Завантаження інформації про класи та учнів з файлів CSV.
import csv
import streamlit as st
import matplotlib.pyplot as plt

st.title("Ліцей №172 «Нивки»")
st.header("Керування шкільними процесами")


#Створюємо клас для студентів
class Students:
    def __init__(self, last_name: str, first_name: str, middle_name: str, birth_year: int, gender: str, average_grade: float) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.gender = gender
        self.average_grade = average_grade


# Створюємо клас
class SchoolClass:
    def __init__(self, parallel: int, vertical: str) -> None:
        self.parallel = parallel
        self.vertical = vertical
        self.students = []

# Одразу створюємо метод переведення учнів на рік перед
    def move_year(self) -> None:
         self.parallel = int(self.parallel) + 1


    def student_count(self) -> int:
        return len(self.students)

    def add_student(self, student) -> None:
        self.students.append(student)

    def get_class_name(self) -> str:
        return f"{self.parallel}{self.vertical}"


    classes_data = [
        ['parallel', 'vertical'],
        [1, 'А'],
        [1, 'Б'],
        [1, 'В'],
        [2, 'А'],
        [2, 'Б'],
        [2, 'В'],
        [3, 'А'],
        [3, 'Б'],
        [3, 'В'],
        [4, 'А'],
        [4, 'Б'],
        [3, 'В'],
        [5, 'А'],
        [5, 'Б'],
        [5, 'В'],
        [6, 'А'],
        [6, 'Б'],
        [7, 'А'],
        [7, 'Б'],
        [8, 'А'],
        [8, 'Б'],
        [9, 'А'],
        [9, 'Б'],
        [10, 'А'],
        [10, 'Б'],
        [11, 'А'],
        [11, 'Б'],
    ]
    with open("classes.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(classes_data)



# Крок 2: Виносимо інформацію
class School:
    def __init__(self):
        self.classes = []

    def get_total_students(self) -> int:
        total = 0
        for class_obj in self.classes:
            total += class_obj.student_count()
        return total

    def add_class(self, school_class) -> None:
        self.classes.append(school_class)

# Рахуємо кількість дівчат та хлопців
    def get_gender_distribution(self) -> tuple[float, float]:
        girls = 0
        boys = 0
        total_students = self.get_total_students()

        for class_obj in self.classes:
            for student in class_obj.students:
                if student.gender.lower() == 'ч':
                    boys += 1
                else:
                    girls += 1

        if total_students == 0:
            return 0, 0

# Знаходимо відсоток хлопців і дівчат.

        percentage_of_girls = (girls / total_students) * 100
        percentage_of_boys = (boys / total_students) * 100
        return percentage_of_girls, percentage_of_boys

# Cередня кількість учнів у класі.

    def average_amount_of_students(self) -> float:
        if not self.classes:
            return 0
        return self.get_total_students() / len(self.classes)

# Мінімальну та максимальну кількість учнів

    def max_amount_of_students(self):
        max_amount = max(self.classes, key=lambda x: x.student_count())
        return {"class": max_amount.get_class_name(), "count": max_amount.student_count()}

    def min_amount_of_students(self):
        min_amount = min(self.classes, key=lambda x: x.student_count())
        return {"class": min_amount.get_class_name(), "count": min_amount.student_count()}

    def move_all_classes(self) -> None:
        self.classes = [cls for cls in self.classes if cls.parallel != 11]
        for class_obj in self.classes:
            class_obj.move_year()
        twelfth_classes = [cls for cls in self.classes if cls.parallel > 11]
        if twelfth_classes:
            for cls in twelfth_classes:
                self.classes.remove(cls)


# Крок 3: Будуємо умови для створення графіків

    def get_parallel_distribution(self):
        parallel_counts = {}
        for class_obj in self.classes:
            parallel = class_obj.parallel
            if parallel not in parallel_counts:
                parallel_counts[parallel] = 0
            parallel_counts[parallel] += class_obj.student_count()
        return parallel_counts

    # Отримати розподіл учнів по вертикалях
    def get_vertical_distribution(self):
        vertical_counts = {}
        for class_obj in self.classes:
            vertical = class_obj.vertical
            if vertical not in vertical_counts:
                vertical_counts[vertical] = []
            vertical_counts[vertical].append(class_obj.student_count())

        # Обчислюємо середнє для кожної вертикалі
        vertical_avg = {}
        for vertical, counts in vertical_counts.items():
            vertical_avg[vertical] = sum(counts) / len(counts)
        return vertical_avg

    # Отримати розподіл учнів за роком народження
    def get_birth_year_distribution(self):
        birth_years = {}
        for class_obj in self.classes:
            for student in class_obj.students:
                year = student.birth_year
                if year not in birth_years:
                    birth_years[year] = 0
                birth_years[year] += 1
        return birth_years

    # Отримати середні оцінки по класах
    def get_grades_by_class(self):
        class_grades = {}
        for class_obj in self.classes:
            parallel = class_obj.parallel
            if parallel not in class_grades:
                class_grades[parallel] = []
            for student in class_obj.students:
                class_grades[parallel].append(student.average_grade)

        # Обчислюємо середнє для кожного класу
        avg_grades = {}
        for parallel, grades in class_grades.items():
            avg_grades[parallel] = sum(grades) / len(grades)
        return avg_grades

# Завантаження даних із csv-файлів
def data_from_csv() -> School:
    school = School()
    classes_dict = {}
    with open("classes.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parallel = row['parallel']
            vertical = row['vertical']
            class_name = f"{parallel}{vertical}"
            classes_dict[class_name] = SchoolClass(parallel, vertical)

# Завантаження даних про студентів
    with open("students.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            class_name = f"{row['class_parallel']}{row['class_vertical']}"
            if class_name in classes_dict:
                student = Students(
                    row['last_name'],
                    row['first_name'],
                    row['middle_name'],
                    int(row['birth_year']),
                    row['gender'],
                    float(row['average_grade'])
                )
                classes_dict[class_name].add_student(student)

    for class_obj in classes_dict.values():
        school.add_class(class_obj)
    return school

data_from_csv()
st.header("Інформація про школу")
school = data_from_csv()

if school.classes:
    total_students = school.get_total_students()
    average_size = school.average_amount_of_students()
    girls_percent, boys_percent = school.get_gender_distribution()
    max_class = school.max_amount_of_students()
    min_class = school.min_amount_of_students()

    # Використаємо колонки для порівняння інформації
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Загальна кількість учнів", total_students)
        st.write("Середня кількість учнів в одному класі", f"{average_size:.1f}")

    with col2:
        st.write("Середня кількість дівчат", f"{girls_percent:.1f}%")
        st.write("Середня кількість хлопців", f"{boys_percent:.1f}%")

    with col3:
        st.write("Найбільший клас", f"{max_class['class']} який має ({max_class['count']} учнів)")
        st.write("Наймненший клас", f"{min_class['class']} який має ({min_class['count']} учнів)")

    # Будуємо графіки
    st.header("Графіки")
    # Графік 1: Розподіл учнів по паралелях
    st.subheader("1. Розподіл кількості учнів по паралелях")
    parallel_graph = school.get_parallel_distribution()
    if parallel_graph:
        fig1, axis1 = plt.subplots()
        axis1.bar(parallel_graph.keys(), parallel_graph.values())
        axis1.set_xlabel('Паралель')
        axis1.set_ylabel('Кількість учнів')
        axis1.set_title('Розподіл учнів по паралелях')
        st.pyplot(fig1)

    st.subheader("2. Розподіл середньої кількості учнів по вертикалях")
    vertical_graph = school.get_vertical_distribution()
    if vertical_graph:
        fig2, axis2 = plt.subplots()
        axis2.bar(vertical_graph.keys(), vertical_graph.values(), color='red')
        axis2.set_xlabel('Вертикаль')
        axis2.set_ylabel('Середня кількість учнів')
        axis2.set_title('Середня кількість учнів по вертикалях')
        st.pyplot(fig2)


    st.subheader("3. Лінійний графік кількості учнів від року народження")
    birth_graph = school.get_birth_year_distribution()
    if birth_graph:
        fig3, axis3 = plt.subplots()
        years = sorted(birth_graph.keys())
        counts = [birth_graph[year] for year in years]
        axis3.plot(years, counts, marker='o')
        axis3.set_xlabel('Рік народження')
        axis3.set_ylabel('Кількість учнів')
        axis3.set_title('Кількість учнів за роком народження')
        st.pyplot(fig3)

    st.subheader("4.Графік залежності середньої оцінки учнів від класу")
    grades_graph = school.get_grades_by_class()
    if grades_graph:
        fig4, axis4 = plt.subplots()
        parallels = (grades_graph.keys())
        avg_grades = [grades_graph[parallel] for parallel in parallels]
        axis4.scatter(parallels, avg_grades, color='green')
        axis4.set_xlabel('Клас')
        axis4.set_ylabel('Середня оцінка')
        axis4.set_title('Середня оцінка по класах')
        st.pyplot(fig4)

# Крок 4: Переведення всіх класів на рік вперед

    if st.button("Перевести всі класи на рік вперед"):
        school.move_all_classes()
        st.success("Класи перевили")

        st.subheader("Новий навчальний рік!")
        new_total_students = school.get_total_students()
        new_average_size = school.average_amount_of_students()
        new_girls_percent, new_boys_percent = school.get_gender_distribution()
        new_max_class = school.max_amount_of_students()
        new_min_class = school.min_amount_of_students()

        # Використаємо колонки для порівняння інформації
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(" Нова Загальна кількість учнів", new_total_students)
            st.write(" Нова Середня кількість учнів в одному класі", f"{new_average_size:.1f}")

        with col2:
            st.write("Нова Середня кількість дівчат", f"{new_girls_percent:.1f}%")
            st.write("Нова Середня кількість хлопців", f"{new_boys_percent:.1f}%")

        with col3:
            st.write("Найбільший клас", f"{new_max_class['class']} який має ({new_max_class['count']} учнів)")
            st.write("Наймненший клас", f"{new_min_class['class']} який має ({new_min_class['count']} учнів)")





