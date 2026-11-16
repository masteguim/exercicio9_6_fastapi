from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Exercicio 9.5 - FastAPI e Docker",
    description="API RESTful de gerenciamento de itens",
    version="1.0.0"
)


class ItemEntrada(BaseModel):
    nome: str = Field(min_length=1)
    preco: float = Field(ge=0)


class Item(ItemEntrada):
    id: int


itens = [
    Item(id=1, nome="Notebook", preco=3500.0),
    Item(id=2, nome="Mouse", preco=120.0)
]


@app.get("/")
def home():
    return {
        "mensagem": "Exercicio 9.5 - FastAPI e Docker",
        "status": "online"
    }


@app.get("/items", response_model=list[Item])
def listar_itens():
    return itens


@app.get("/items/{item_id}", response_model=Item)
def buscar_item(item_id: int):
    for item in itens:
        if item.id == item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Item nao encontrado"
    )


@app.post("/items", response_model=Item, status_code=201)
def criar_item(dados: ItemEntrada):
    novo_id = max(
        (item.id for item in itens),
        default=0
    ) + 1

    novo_item = Item(
        id=novo_id,
        nome=dados.nome,
        preco=dados.preco
    )

    itens.append(novo_item)

    return novo_item


@app.put("/items/{item_id}", response_model=Item)
def atualizar_item(item_id: int, dados: ItemEntrada):
    for item in itens:
        if item.id == item_id:
            item.nome = dados.nome
            item.preco = dados.preco
            return item

    raise HTTPException(
        status_code=404,
        detail="Item nao encontrado"
    )


@app.delete("/items/{item_id}")
def excluir_item(item_id: int):
    for item in itens:
        if item.id == item_id:
            itens.remove(item)
            return {
                "mensagem": "Item excluido com sucesso"
            }

    raise HTTPException(
        status_code=404,
        detail="Item nao encontrado"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )

