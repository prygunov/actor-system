import typing
import pandas as pd

from thespian.actors import *
from lab6.courier_entity import CourierEntity
from lab6.order_entity import OrderEntity
from agents_dispatcher import AgentsDispatcher
from scene import Scene

def read_csv(filename) -> typing.List:
     df = pd.read_csv(filename, delimiter=';')
     df_index = df.to_dict('index')
     resulted_list = list(df_index.values())
     return resulted_list

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s%(levelname)s %(message)s")
    logging.info("Добро пожаловать в систему доставки")
    scene = Scene()
    dispatcher = AgentsDispatcher(scene)
    couriers = read_csv('../res/couriers.csv')
    logging.info(f'Прочитаны курьеры: {couriers}')

    orders = read_csv('../res/orders.csv')
    logging.info(f'Прочитаны заказы: {orders}')

    for courier in couriers[:10]:
        onto_description = {}
        entity = CourierEntity(onto_description, courier, scene)
        dispatcher.add_entity(entity)

    for order in orders[:10]:
        onto_description = {}
        entity = OrderEntity(onto_description, order, scene)
        dispatcher.add_entity(entity)

    dispatcher.remove_agent(scene.entities['COURIER'][0])