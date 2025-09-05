from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class client(Base):
    __tablename__ = 'client'

    id = Column("pk_client", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    firstInterest = Column(String(140))
    secondInterest = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    # Implicit relationship between cliente and card, SQLAlchemy
    # have the responsability of rebuilding this relationship
    card = relationship("card")

    def __init__(self, name:str, firstInterest:str, secondInterest:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Create a client

        Arguments:
            name: client name.
            firstInterest: client first interest when choosing a credit card.
            secondInterest: client second interest when choosing a credit card.
            data_insercao: date when the client was added to the database.
        """
        self.name = name
        self.firstInterest = firstInterest
        self.secondInterest = secondInterest

        # if date not informed the date will be the inserction date in the database
        if data_insercao:
            self.data_insercao = data_insercao


