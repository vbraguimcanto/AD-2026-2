from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from database import Base, Session, engine
from models import Aluno


app = FastAPI()

Base.metadata.create_all(engine)


class AlunoPayload(BaseModel):
    nome: str
    curso: str


@app.get("/alunos", status_code=status.HTTP_200_OK)
def listar_alunos():
    db = Session()
    alunos = db.query(Aluno).all()
    db.close()

    return alunos


@app.get("/alunos/{aluno_id}", status_code=status.HTTP_200_OK)
def buscar_aluno(aluno_id: int):
    db = Session()
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    db.close()

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return aluno


@app.post("/alunos", status_code=status.HTTP_201_CREATED)
def cadastrar_aluno(dados: AlunoPayload):
    db = Session()

    aluno = Aluno(
        nome=dados.nome,
        curso=dados.curso
    )

    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    db.close()

    return aluno


@app.delete("/alunos/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_aluno(aluno_id: int):
    db = Session()
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if aluno is None:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    db.delete(aluno)
    db.commit()
    db.close()