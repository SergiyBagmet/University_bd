from datetime import datetime
from random import randint

from faker import Faker


from src.models import Teacher, Subject, Group, Student, Grade
from src.crud import CRUDManager
from src.config import url
from src.db import DBManager

NUMBER_TEACHERS = 6
NUMBER_STUDENTS = 50

subjects = [
    "Математика",
    "Теоретична інформатика",
    "Архітектура комп'ютерів",
    "Алгоритми та структури даних",
    "Мови програмування",
    "Бази даних",
    "Інформаційні мережі",
    "Криптографія та інформаційна безпека"
]

groups = ["мт-11-3", "мм-13-1", "кн-12-2"]


class UniverSeeder:
    def __init__(self, crud_m: CRUDManager):
        self.crud_m = crud_m
        self.fake = Faker()

    def seed_teachers(self, number_teachers):
        teachers = [Teacher(first_name=self.fake.first_name(), last_name=self.fake.last_name()) for _ in range(number_teachers)]
        self.crud_m.create_many(teachers)
        
    # def seed_subjects(self, subjects, number_teachers):
    #     data_subjects = zip(subjects, iter(randint(1, number_teachers) for _ in range(len(subjects))))
        
    # def seed_groups(self, groups):
    #     sql = "INSERT INTO groups (name) VALUES (?)"
    #     data_groups = zip(groups, )
    #     self.crud.execute_many_sql(sql, data_groups)
    
    # def seed_students(self, groups, number_students):
    #     sql = "INSERT INTO students (fullname, group_id) VALUES (?, ?)"
    #     students = [self.fake.name() for _ in range(number_students)]
    #     data_students = zip(students, iter(randint(1, len(groups))for _ in range(number_students)))
    #     self.crud.execute_many_sql(sql, data_students)
    
    # def _random_date(self) -> str:
    #     start_date = datetime(2023, 9, 1)  # Начало учебного года
    #     end_date = datetime(2024, 6, 30)  # Конец учебного года
    #     while True:
    #         fake_date : datetime = self.fake.date_between_dates(start_date, end_date)
    #         if fake_date.isoweekday() < 6:
    #             return fake_date.strftime("%Y-%m-%d")
    
    # def seed_grades(self, subjects , number_students):
    #     sql = "INSERT INTO grades (subject_id, student_id, grade, date_of ) VALUES (?, ?, ?, ?)"
        
    #     grades = []
    #     grade_counters = {student_id: 0 for student_id in range(1, number_students + 1)}
        
    #     while any(count < 20 for count in grade_counters.values()):
    #         subject_id = randint(1, len(subjects))
    #         student_id = randint(1, number_students)
    #         grade = randint(1, 12)
    #         date = self._random_date()
            
    #         if grade_counters[student_id] < 20:
    #             grades.append((subject_id, student_id, grade, date))
    #             grade_counters[student_id] += 1
                   
    #     self.crud.execute_many_sql(sql, grades)

if __name__ == "__main__":
    
    dbm = DBManager(url)
    crud_m = CRUDManager(dbm)
    seeder = UniverSeeder(crud_m)
    
    # seeder.seed_teachers(NUMBER_TEACHERS)


