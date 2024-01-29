from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from datetime import datetime
from sqlalchemy.orm import relationship


class Order(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("Users.id"))
    id_good = Column(Integer, ForeignKey("Goods.id"))
    order_date = Column(String, nullable=True, default=datetime.now())
    status = Column(Boolean, nullable=True, default=False)

    def __repr__(self):
        return f'<Orders> {self.id}, ' \
               f'id_user: {self.id_user}, ' \
               f'id_good: {self.id_good}, ' \
               f'order_date: {self.order_date}, ' \
               f'status: {self.status}'


