from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Card(Base):
    __tablename__ = 'card'

    id = Column("pk_card", Integer, primary_key=True)
    name = Column(String(140))
    limit = Column(Float)
    benefitCard = Column(String(140))
    inserction_date = Column(DateTime, default=datetime.now())

    # Definition of the relationship between the card and a client.
    # This defines the 'client' column, which will store
    # the reference to the client, the foreign key that links
    # a product to the comment.
    client = Column(Integer, ForeignKey("client.pk_client"), nullable=False)

    def __init__(self, name:str, limit:float, benefitCard:str,
                 inserction_date:Union[DateTime, None] = None):
        """
        Create a card

        Arguments:
            name: card name.
            limit: card limit.
            benefitCard: card benefit.
            inserction_date: date when the card was added to the database.
        """
        self.name = name
        self.limit = limit
        self.benefitCard = benefitCard

        # if date not informed the date will be the inserction date in the database
        if inserction_date:
            self.inserction_date = inserction_date


