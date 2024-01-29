from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase


class Good(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Goods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    cost_of_good = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<Goods> {self.id}, ' \
               f'name: {self.name}, ' \
               f'description: {self.description}, ' \
               f'cost_of_good: {self.cost_of_good}'

