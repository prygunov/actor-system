from base_entity import BaseEntity
from point import Point
from datetime import datetime

class OrderEntity(BaseEntity):
    """
    Класс заказа
    """
    def __init__(self, onto_desc: dict, init_dict_data, scene=None):
        super().__init__(onto_desc, scene)
        self.type = 'ORDER'
        self.number = init_dict_data.get('Номер')
        self.name = init_dict_data.get('Наименование')
        self.weight = init_dict_data.get('Масса')
        self.volume = init_dict_data.get('Объем')
        self.price = init_dict_data.get('Стоимость')
        x1 = init_dict_data.get('Координата получения x')
        y1 = init_dict_data.get('Координата получения y')
        self.point_from = Point(x1, y1)
        x2 = init_dict_data.get('Координата доставки x')
        y2 = init_dict_data.get('Координата доставки y')
        self.point_to = Point(x2, y2)
        self.time_from = init_dict_data.get('Время получения заказа')
        self.time_to = init_dict_data.get('Время доставки заказа')
        self.order_type = init_dict_data.get('Тип заказа')
        self.uri = 'Order' + str(self.number)