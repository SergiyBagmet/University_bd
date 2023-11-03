from sqlalchemy import func, and_, or_, between, desc
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import select
from tabulate import tabulate


from src.models import Teacher, Subject, Group, Student, Grade
from src.crud import CRUDManager
from src.config import url
from src.db import DBManager

session = DBManager(url).session


class Selecter:
    titel = None
  
    def select_1(self, limit=5) -> Query:
        self.titel = "1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів."
        query = (
            select(
                func.concat(Student.first_name, ' ', Student.last_name).label('students'),
                func.round(func.avg(Grade.score), 2).label('average_grade'),
            )
            .select_from(Student)
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id)
            .order_by(desc('average_grade'))
            .limit(limit)
        )
        return query
    
    #Знайти студента із найвищим середнім балом з певного предмета.
    def select_2(self, sub_id=1) -> Query :
        self.titel = "2. Знайти студента із найвищим середнім балом з певного предмета."
        query = (
            select(
                func.concat(Student.first_name, ' ', Student.last_name).label('student'),
                func.round(func.avg(Grade.score), 2).label('average_grade'),
                func.max(Subject.name).label('subject')
            )
            .select_from(Student)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Grade.subject_id == Subject.id)
            .where(Subject.id == sub_id)
            .group_by('student')
            .order_by(desc('average_grade'))
            .limit(1)
        )
        return query
    
    def select_3(self, sub_id=1) -> Query :
        self.titel = "3. Знайти середній бал у групах з певного предмета."
        query = (
            select(
                Group.name.label('groups'),
                func.round(func.avg(Grade.score), 2).label('average_grade'),
                func.max(Subject.name).label('subject')
            )
            .select_from(Grade)
            .join(Student, Grade.student_id == Student.id)
            .join(Subject, Grade.subject_id == Subject.id)
            .join(Group, Student.group_id==Group.id)
            .where(Subject.id == sub_id)
            .group_by('groups')
            .order_by(desc('average_grade'))
        )
        return query
    
    def select_4(self, sub_id=1) -> Query :
        self.titel = "4. Знайти середній бал на потоці (по всій таблиці оцінок)"
        query = (
            select(
                func.round(func.avg(Grade.score), 2).label('average_grade'),
            )
            .select_from(Grade)
        )
        return query
    
    def select_5(self, t_id=4) -> Query :
        self.titel = "5. Знайти які курси читає певний викладач."
        query = (
            select(
                Subject.name.label('subjects'),
                func.concat(Teacher.first_name, ' ', Teacher.last_name).label('teacher')   
            )
            .select_from(Subject)
            .join(Teacher, Teacher.id == Subject.teacher_id)
            .where(Teacher.id == t_id)
        )
        return query

if __name__ == "__main__":
    dbm = DBManager(url)
    crud_m = CRUDManager(dbm)
    sel = Selecter()

    for i in range(5, 6):
        query : Query = getattr(sel, f'select_{i}')()
        titel = sel.titel
        print(query.column_descriptions)
        descr_name = [data['name'] for data in query.column_descriptions]
        result = crud_m.custom_query(query)  
        tabl = tabulate(tabular_data=result, headers=descr_name, tablefmt="heavy_outline")
        print(f"{titel}\n{tabl}\n")
       