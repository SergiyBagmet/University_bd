from sqlalchemy import  Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    students = relationship("Student", back_populates="group")
    
    def __str__(self):
        return f"Group(id={self.id}, name='{self.name}')"


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete='CASCADE', onupdate='CASCADE'))
    
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")
    
    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @name.setter
    def name(self, value: str):
        parts = value.split(' ')
        if len(parts) >= 2:
            self.first_name = parts[0]
            self.last_name = ' '.join(parts[1:])
        elif len(parts) == 1:
            self.first_name = parts[0]
            self.last_name = ""
        else:
            raise ValueError("Invalid fullname format. Please provide at least a first name.")
    
    def __str__(self):
        return f"Student(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', group_id={self.group_id})"    
    
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")
    
    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @name.setter
    def name(self, value: str):
        parts = value.split(' ')
        if len(parts) >= 2:
            self.first_name = parts[0]
            self.last_name = ' '.join(parts[1:])
        elif len(parts) == 1:
            self.first_name = parts[0]
            self.last_name = ""
        else:
            raise ValueError("Invalid fullname format. Please provide at least a first name.")
    
    def __str__(self):
        return f"Teacher(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')"    
        
    
       
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete='CASCADE', onupdate='CASCADE'))
    
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")
    
    def __str__(self):
        return f"Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})"
    
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete='CASCADE', onupdate='CASCADE'))
    
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
    
    def __str__(self):
        return f"Grade(id={self.id}, score={self.score}, date_of={self.date_of}, student_id={self.student_id}, subject_id={self.subject_id})"    
        