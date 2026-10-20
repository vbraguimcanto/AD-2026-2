from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Produto

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Produtos")


class ProdutoCreate(BaseModel):
    nome: str
    preco: float


@app.get("/")
def home():
    return {"mensagem": "API funcionando"}


@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


@app.post("/produtos")
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(
        nome=produto.nome,
        preco=produto.preco
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@app.put("/produtos/{produto_id}")
def atualizar_produto(
    produto_id: int,
    produto: ProdutoCreate,
    db: Session = Depends(get_db)
):
    produto_db = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_db.nome = produto.nome
    produto_db.preco = produto.preco

    db.commit()
    db.refresh(produto_db)

    return produto_db


@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()

    return {"mensagem": "Produto excluído"}
