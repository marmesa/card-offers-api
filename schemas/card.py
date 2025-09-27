from pydantic import BaseModel
from typing import Optional, List

from model.card import Card

class CardSchema(BaseModel):
    """ Define como um novo cartão a ser inserido deve ser representado
    """
    client_id: int = 1
    name: str = "Cartao Preto"
    limit: float = 1000
    benefitCard: str = "Anuidade Zero"

class ListCardsSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    cards:List[CardSchema]

def show_cards(cards: List[Card]):
    """ Retorna uma representação de cartões seguindo o schema definido em
        CardViewSchema.
    """
    result = []
    for card in cards:
        result.append({
            "name": card.name,
            "limit": card.limit,
            "benefitCard": card.benefitCard,
            "client_id": card.client
        })

    return {"cards": result}