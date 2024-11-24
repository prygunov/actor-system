from base_entity import BaseEntity
from point import Point

class CourierEntity(BaseEntity):
    """
    Класс курьера
    """
    def __init__(self, onto_desc: dict, init_dict_data, scene=None):
        super().__init__(onto_desc, scene)
        self.type = 'COURIER'
        self.number = init_dict_data.get('Табельный номер')
        self.name = init_dict_data.get('ФИО')
        x1 = init_dict_data.get('Координата начального положения x')
        y1 = init_dict_data.get('Координата начального положения y')
        self.init_point = Point(x1, y1)
        self.types = [_type.lstrip() for _type in init_dict_data.get('Типы доставляемых заказов', '').split(';')]
        self.cost = init_dict_data.get('Стоимость выхода на работу')
        self.rate = init_dict_data.get('Цена работы за единицу времени')
        self.velocity = init_dict_data.get('Скорость')
        self.max_volume = init_dict_data.get('Объем ранца')
        self.max_mass = init_dict_data.get('Грузоподъемность')
        self.uri = 'Courier' + str(self.number)