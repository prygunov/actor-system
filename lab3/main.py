import typing
import pandas as pd

from thespian.actors import *
from lab3.courier_entity import CourierEntity
from lab3.order_entity import OrderEntity
from agents_dispatcher import AgentsDispatcher
from scene import Scene


def get_excel_data(filename, sheet_name) -> typing.List:
     df = pd.read_excel(filename, sheet_name=sheet_name)
     df_index = df.to_dict('index')
     resulted_list = list(df_index.values())
     return resulted_list

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s%(levelname)s %(message)s")
    logging.info("Добро пожаловать в систему доставки")
    scene = Scene()
    dispatcher = AgentsDispatcher(scene)
    couriers = get_excel_data('source.xlsx', 'Курьеры')
    logging.info(f'Прочитаны курьеры: {couriers}')

    orders = get_excel_data('source.xlsx', 'Заказы')
    logging.info(f'Прочитаны заказы: {orders}')

    for courier in couriers[:1]:
        onto_description = {}
        entity = CourierEntity(onto_description, courier, scene)
        dispatcher.add_entity(entity)

    for order in orders[:1]:
        onto_description = {}
        entity = OrderEntity(onto_description, order, scene)
        dispatcher.add_entity(entity)
