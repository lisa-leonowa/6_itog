# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц:
# товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
# • Таблица пользователей должна содержать следующие поля:
#           id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
# • Таблица заказов должна содержать следующие поля:
#           id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# • Таблица товаров должна содержать следующие поля:
#           id (PRIMARY KEY), название, описание и цена.
#
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой
# из трёх таблиц (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
# * Чтение всех
# * Чтение одного
# * Запись
# * Изменение
# * Удаление

from pydantic import BaseModel
from fastapi_login import LoginManager
from data import db_session
from data.Users import User
from data.Goods import Good
from data.Orders import Order
from fastapi import FastAPI
import os
from werkzeug.security import generate_password_hash


# Модель Пользователи
class Users(BaseModel):
    name: str
    last_name: str
    email: str
    password: str


# Модель Заказы
class Orders(BaseModel):
    id_user: str
    id_good: str
    order_date: str
    status: bool  # Тут статус: выполнен заказ или нет. Если выполнен - True, иначе - False


# Модель Товары
class Goods(BaseModel):
    name: str
    description: str
    cost_of_good: int


SECRET_KEY = os.urandom(24).hex()
app = FastAPI()
login_manager = LoginManager(SECRET_KEY, token_url='/')


@login_manager.user_loader()
def load_user(user_id):
    sessions = db_session.create_session()
    # return sessions.query(User).get(user_id)
    return 'Готово'


# Пример: REST API, Чтение всех Пользователей
# http://127.0.0.1:8000/users
@app.post('/users')
async def get_all_users():
    session = db_session.create_session()
    answer = [str(i) for i in session.query(User).all()]
    return answer if len(answer) != 0 else 'Таблица Пользователи пустая'


# Пример: REST API, Чтение одного Пользователя
# http://127.0.0.1:8000/users/2
@app.get('/users/{id_user}')
async def get_user(id_user: int):
    session = db_session.create_session()
    return str(session.query(User).get(id_user))


# Пример: REST API, Запись Пользователя
# http://127.0.0.1:8000/users/Sergei/Zavalishchin/Sergei.Zavalishchin@mail.ru/password45
@app.get('/users/{name}/{last_name}/{email}/{password}')
async def insert_user(name: str, last_name: str, email: str, password: str):
    session = db_session.create_session()
    user = User(name=name,
                last_name=last_name,
                email=email)
    user.set_password(password)

    answer = {'status': '',
              'name': name,
              'last_name': last_name,
              'email': email,
              'password': password}
    try:
        session.add(user)
        session.commit()
        answer['status'] = 'Пользователь был добавлен!'
    except Exception:
        answer['status'] = 'Пользователь не был добавлен!'
    return answer


# Пример: REST API, Изменение  Пользователя
# http://127.0.0.1:8000/users/1/Dasha/Zavalishchina/Daria.Zavalishchina@mail.ru/123456
@app.put('/users/{id_user}/{name}/{last_name}/{email}/{password}')
async def update_user(id_user: int, name: str, last_name: str, email: str, password: str):
    session = db_session.create_session()
    user = session.query(User).get(id_user)

    if user is not None:
        user.name = name
        user.last_name = last_name
        user.email = email
        user.password = generate_password_hash(password)
        session.commit()
    else:
        return 'Не удалось обновить информацию!'
    return 'Информация обновлена!'


# Пример: REST API, Удаление одного Пользователя
# http://127.0.0.1:8000/users/2
@app.delete('/users/{id_user}')
async def delete_user(id_user: int):
    session = db_session.create_session()
    try:
        session.delete(session.query(User).get(id_user))
        session.commit()
        return 'Пользователь удален!'
    except Exception:
        return 'Удаление не получилось выполнить!'


# Пример: REST API, Чтение всех Товаров
# http://127.0.0.1:8000/goods
@app.post('/goods')
async def get_all_goods():
    session = db_session.create_session()
    answer = [str(i) for i in session.query(Good).all()]
    return answer if len(answer) != 0 else 'Таблица Товары пустая'


# Пример: REST API, Чтение одного Товара
# http://127.0.0.1:8000/goods/1
@app.get('/goods/{id_good}')
async def get_good(id_good: int):
    session = db_session.create_session()
    return str(session.query(Good).get(id_good))


# Пример: REST API, Запись Товара
# http://127.0.0.1:8000/goods/Серьги/Замечательные/1000
@app.get('/goods/{name}/{description}/{cost_of_good}')
async def insert_good(name: str, description: str, cost_of_good: int):
    session = db_session.create_session()
    good = Good(name=name,
                description=description,
                cost_of_good=cost_of_good)

    answer = {'status': '',
              'name': name,
              'description': description,
              'cost_of_good': cost_of_good}
    try:
        session.add(good)
        session.commit()
        answer['status'] = 'Товар был добавлен!'
    except Exception:
        answer['status'] = 'Товар не был добавлен!'
    return answer


# Пример: REST API, Изменение  Товара
# http://127.0.0.1:8000/goods/1/Серьги/Прекрасные/1000
@app.put('/goods/{id_good}/{name}/{description}/{cost_of_good}')
async def update_good(id_good: int, name: str, description: str, cost_of_good: int):
    session = db_session.create_session()
    good = session.query(Good).get(id_good)

    if good is not None:
        good.name = name
        good.description = description
        good.cost_of_good = cost_of_good
        session.commit()
    else:
        return 'Не удалось обновить информацию!'
    return 'Информация обновлена!'


# Пример: REST API, Удаление одного Товара
# http://127.0.0.1:8000/goods/2
@app.delete('/goods/{id_good}')
async def delete_good(id_good: int):
    session = db_session.create_session()
    try:
        session.delete(session.query(Good).get(id_good))
        session.commit()
        return 'Товар удален!'
    except Exception:
        return 'Удаление не получилось выполнить!'


# Пример: REST API, Чтение всех Заказов
# http://127.0.0.1:8000/orders
@app.post('/orders')
async def get_all_orders():
    session = db_session.create_session()
    answer = [str(i) for i in session.query(Order).all()]
    return answer if len(answer) != 0 else 'Таблица Заказы пустая'


# Пример: REST API, Чтение одного Заказа
# http://127.0.0.1:8000/orders/1
@app.get('/orders/{id_order}')
async def get_order(id_order: int):
    session = db_session.create_session()
    return str(session.query(Order).get(id_order))


# Пример: REST API, Запись Заказа
# http://127.0.0.1:8000/orders/1/1
@app.get('/orders/{id_user}/{id_good}')
async def insert_order(id_user: int, id_good: int):
    session = db_session.create_session()
    order = Order(id_user=id_user,
                  id_good=id_good)
    try:
        session.add(order)
        session.commit()
    except Exception:
        return 'Заказ не был добавлен!'
    return 'Заказ был добавлен!'


# Пример: REST API, Изменение  Товара
# http://127.0.0.1:8000/orders/1/True
@app.put('/orders/{id_order}/{status}')
async def update_order(id_order: int, status: bool):
    session = db_session.create_session()
    order = session.query(Order).get(id_order)

    if order is not None:
        order.status = status
        session.commit()
    else:
        return 'Не удалось обновить информацию!'
    return 'Информация обновлена!'


# Пример: REST API, Удаление одного Товара
# http://127.0.0.1:8000/order/2
@app.delete('/orders/{id_order}')
async def delete_order(id_order: int):
    session = db_session.create_session()
    try:
        session.delete(session.query(Order).get(id_order))
        session.commit()
        return 'Заказ удален!'
    except Exception:
        return 'Удаление не получилось выполнить!'


db_session.global_init("db/OnlineStore.sqlite")
