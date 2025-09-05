from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class benefit(Base):
    __tablename__ = 'benefit'

    id = Column("pk_benefit", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    interest = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o benefit e um card.
    # Aqui está sendo definido a coluna 'card' que vai guardar
    # a referencia ao card, a chave estrangeira que relaciona
    # um produto ao comentário.
    card = Column(Integer, ForeignKey("client.pk_card"), nullable=False)

    def __init__(self, name:str, interest:str, data_insercao:Union[DateTime, None] = None):
        """
        Create a benefit

        Arguments:
            name: benefit name.
            interest: Interest that this benefit is registered.
            data_insercao: date when the benefit was added to the database.
        """
        self.name = name
        self.interest = interest

        # if date not informed the date will be the inserction date in the database
        if data_insercao:
            self.data_insercao = data_insercao


