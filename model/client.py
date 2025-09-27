from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base
from model.card import Card

class Client(Base):
    __tablename__ = 'client'

    id = Column("pk_client", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    income = Column(Float)
    benefitClient = Column(String(140))
    inserction_date = Column(DateTime, default=datetime.now())

    # Implicit relationship between cliente and card, SQLAlchemy
    # have the responsability of rebuilding this relationship
    cards = relationship("Card")

    def __init__(self, name:str, income:float, benefitClient:str,
                 inserction_date:Union[DateTime, None] = None):
        """
        Create a client

        Arguments:
            name: client name.
            income: clients monthly income.
            benefitClient: benefit desired when choosing a credit card.
            inserction_date: date when the client was added to the database.
        """
        self.name = name
        self.income = income
        self.benefitClient = benefitClient

        # if date not informed the date will be the inserction date in the database
        if inserction_date:
            self.inserction_date = inserction_date


    def add_card(self, card:Card):
        """ Adiciona um novo cartão ao cliente
        """
        self.cards.append(card)