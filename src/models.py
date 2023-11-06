from sqlalchemy import  Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

model_registry = {}

def register_model(cls):
    """
    Декоратор для регистрации классов моделей в реестре.
    """
    model_registry[cls.__name__] = cls
    return cls


class BaseModel(Base):
    __abstract__ = True  # Делает класс абстрактным для SQLAlchemy
    
    id = Column(Integer, primary_key=True)  # Общий первичный ключ для всех моделей
    
    args_spase = None 
    
    @classmethod
    def get_column_names(cls):
        # Возвращает список имен столбцов для класса
        c_names = [column.name for column in cls.__table__.columns]
        cls.args_spase = c_names[-1:] + c_names[:-1]
        
        if all(hasattr(cls, attr) for attr in ['first_name', 'last_name']): # КОСТЫЛЬ
            c_names.append('name')
        return c_names
        
    def __str__(self):
        self.get_column_names()
        columns_attr = [f"{c_name}={getattr(self, c_name)}" for c_name in self.args_spase]
        return  f'<{self.__class__.__name__} ({", ".join(map(str, columns_attr))})>'

@register_model
class Group(BaseModel):
    __tablename__ = 'groups'
    
    name = Column(String(50), unique=True, nullable=False)
    students = relationship("Student", back_populates="group")
    
@register_model 
class Student(BaseModel):
    __tablename__ = 'students'
    
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
    
@register_model
class Teacher(BaseModel):
    __tablename__ = 'teachers'
 
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
    
@register_model       
class Subject(BaseModel):
    __tablename__ = 'subjects'

    name = Column(String(50), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete='CASCADE', onupdate='CASCADE'))
    
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

@register_model
class Grade(BaseModel):
    __tablename__ = 'grades'
   
    score = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete='CASCADE', onupdate='CASCADE'))
    
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
    

      