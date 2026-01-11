from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import declarative_base
import enum
from sqlalchemy import Enum as SAEnum

Base = declarative_base()

class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.student, nullable=False)