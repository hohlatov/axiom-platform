from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    grade = Column(String(50)) # "5 класс", "6 класс" и т.д.
    subject = Column(String(100)) # "Математика", "Физика"
    
    # Связь: материал принадлежит учителю
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="materials")
    
    