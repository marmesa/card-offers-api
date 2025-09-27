from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class card(Base):
    __tablename__ = 'card'

    id = Column("pk_card", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    firstBenefit = Column(String(140))
    secondBenefit = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definition of the relationship between the card and a client.
    # This defines the 'client' column, which will store
    # the reference to the client, the foreign key that links
    # a product to the comment.
    client = Column(Integer, ForeignKey("client.pk_client"), nullable=False)

    def __init__(self, name:str, firstBenefit:str, secondBenefit:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Create a card

        Arguments:
            name: card name.
            firstbenefit: card first benefit if chosen.
            secondbenefit: card second benefit if chosen.
            data_insercao: date when the card was added to the database.
        """
        self.name = name
        self.firstBenefit = firstBenefit
        self.secondBenefit = secondBenefit

        # if date not informed the date will be the inserction date in the database
        if data_insercao:
            self.data_insercao = data_insercao


