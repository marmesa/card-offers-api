from pydantic import BaseModel
from typing import Optional, List
from model.client import Client

from schemas import CardSchema


class ClientSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    name: str = "Maria"
    income: float = 1000
    benefitClient: str = "Anuidade Zero"


class ClientSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no name do cliente.
    """
    name: str = "Maria"


class ListClientsSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clients:List[ClientSchema]


def show_clients(clients: List[Client]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        clientViewSchema.
    """
    result = []
    for client in clients:
        result.append({
            "name": client.name,
            "income": client.income,
            "benefitClient": client.benefitClient,
        })

    return {"clients": result}


class ClientViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente + comentários.
    """
    id: int = 1
    name: str = "Maria"
    income: float = 1000
    benefitClient: str = "Anuidade Zero"
    total_cards: int = 1
    cards:List[CardSchema]


class ClientDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str

def show_client(client: Client):
    """ Retorna uma representação do cliente seguindo o schema definido em
        clientViewSchema.
    """
    return {
        "id": client.id,
        "name": client.name,
        "income": client.income,
        "benefitClient": client.benefitClient,
        "total_cards": len(client.cards),
        "cards": [{ "name": c.name,
                    "limit": c.limit,
                    "benefitCard": c.benefitCard
                  } for c in client.cards]
    }
