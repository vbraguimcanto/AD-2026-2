from sqlalchemy import Column, Integer, String

from database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    curso = Column(String)