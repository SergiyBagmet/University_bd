from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    
    @hybrid_property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    group_id = Column(Integer, ForeignKey("groups.id", ondelete='CASCADE', onupdate='CASCADE'))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")
    
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    
    @hybrid_property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    subjects = relationship("Subject", back_populates="teacher")
       
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("teachers.id", ondelete='CASCADE', onupdate='CASCADE'))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")
    
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete='CASCADE', onupdate='CASCADE'))
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")    
        