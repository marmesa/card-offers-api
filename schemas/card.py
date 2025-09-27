from pydantic import BaseModel


class CardSchema(BaseModel):
    """ Define como um novo cartão a ser inserido deve ser representado
    """
    client_id: int = 1
    name: str = "Cartao Preto"
    limit: float = 1000
    benefitCard: str = "Anuidade Zero"
