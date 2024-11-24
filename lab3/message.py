from enum import Enum
from dataclasses import dataclass
from typing import Any

class MessageType(Enum):
    INIT_MESSAGE = 'Инициализация'

    REQUEST_COURIER_INFO= 'Заказ курьеров'
    COURIER_INFO = 'Информация о параметрах курьера'
    COURIER_DELIVERY_INTERVALS = 'Интервалы доставки'

    REQUEST_ORDER_ASSIGN = 'Запрос на назначение заказа'
    ORDER_ASSIGN_RESPONSE = 'Ответ на запрос на назначение заказа'

    REQUEST_DELIVERY_INTERVALS= 'Запрос временных промежутков'
    DELIVERY_INTERVALS= 'Интервал доставки'
    SCHEDULE_DELIVERY= 'Отложить доставку'
    CREATE_ACTOR = 'Создание актора'
    HELLO_WORLD = 'Приветствие'

@dataclass
class Message:
    """Класс для хранения сообщений"""
    msg_type: MessageType
    msg_body: Any