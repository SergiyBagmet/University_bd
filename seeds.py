from datetime import datetime
from random import randint

from faker import Faker


from src.models import Teacher, Subject, Group, Student, Grade
from src.crud import CRUDManager
from src.config import url
from src.db import DBManager

NUMBER_TEACHERS = 6
NUMBER_STUDENTS = 50

SUBJECTS = [
    "Математика",
    "Теоретична інформатика",
    "Архітектура комп'ютерів",
    "Алгоритми та структури даних",
    "Мови програмування",
    "Бази даних",
    "Інформаційні мережі",
    "Криптографія та інформаційна безпека"
]

GROUPS = ["мт-11-3", "мм-13-1", "кн-12-2"]


class UniverSeeder:
    def __init__(self, crud_m: CRUDManager):
        self.crud_m = crud_m
        self.fake = Faker()

    def seed_teachers(self, number_teachers):
        teachers = [
            Teacher(
                first_name=self.fake.first_name(), 
                last_name=self.fake.last_name()
                ) 
            for _ in range(number_teachers)
            ]
        self.crud_m.create_many(teachers)
        
    def seed_subjects(self, subjects, number_teachers):
        subjects = [
            Subject(
                name=sub, 
                teacher_id=randint(1, number_teachers)
                ) 
            for sub in subjects
            ]
        self.crud_m.create_many(subjects)
        
    def seed_groups(self, groups):
        groups = [Group(name=gr)for gr in groups]
        self.crud_m.create_many(groups)
    
    def seed_students(self, groups, number_students):
        students = [
            Student(
                first_name=self.fake.first_name(), 
                last_name=self.fake.last_name(),
                group_id=randint(1, len(groups)) 
                ) 
            for _ in range(number_students)
            ]
        self.crud_m.create_many(students)
        
    
    def _random_date(self) -> str:
        start_date = datetime(2023, 9, 1)  # Начало учебного года
        end_date = datetime(2024, 6, 30)  # Конец учебного года
        while True:
            fake_date : datetime = self.fake.date_between_dates(start_date, end_date)
            if fake_date.isoweekday() < 6:
                return fake_date.strftime("%Y-%m-%d")
    
    def seed_grades(self, subjects , number_students):
        grades = []
        grade_counters = {student_id: 0 for student_id in range(1, number_students + 1)}
        
        while any(count < 20 for count in grade_counters.values()):
            subject_id = randint(1, len(subjects))
            student_id = randint(1, number_students)
            grade = randint(1, 100)
            date = self._random_date()
            
            if grade_counters[student_id] < 20:
                grades.append(
                    Grade(
                        score=grade,
                        date_of=date,
                        student_id=student_id,
                        subject_id=subject_id
                        )
                    )
                grade_counters[student_id] += 1
                   
        self.crud_m.create_many(grades)



if __name__ == "__main__":
    
    dbm = DBManager(url)
    crud_m = CRUDManager(dbm)
    seeder = UniverSeeder(crud_m)
    
    seeder.seed_teachers(NUMBER_TEACHERS)
    seeder.seed_subjects(SUBJECTS, NUMBER_TEACHERS)
    seeder.seed_groups(GROUPS)
    seeder.seed_students(GROUPS, NUMBER_STUDENTS)
    seeder.seed_grades(SUBJECTS, NUMBER_STUDENTS)

