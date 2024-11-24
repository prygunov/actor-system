import logging

from agent_base import AgentBase
from courier_entity import CourierEntity
from message import MessageType, Message

from lab3.order_entity import OrderEntity


class CourierAgent(AgentBase):
    """
    Класс агента курьера
    """
    def __init__(self):
        super().__init__()
        self.entity: CourierEntity
        self.name = 'Агент курьера'
        self.type = 'COURIER'
        self.orders :list(OrderEntity) = []
        self.subscribe(MessageType.REQUEST_COURIER_INFO, self.get_info)
        self.subscribe(MessageType.REQUEST_ORDER_ASSIGN, self.request_order_assign)
        self.subscribe(MessageType.INIT_MESSAGE, self.handle_init_message)

    def handle_init_message(self, message, sender):
        self.dispatcher = message.msg_body['dispatcher']
        self.actor_system = message.msg_body['actor_system']
        self.scene = message.msg_body['scene']
        self.reference_book = message.msg_body['reference_book']
        self.entity = message.msg_body['entity']

    def get_info(self, message, sender):
        # TODO посчитать в какой интервал времени мы можем взять заказ
        response_message = Message(MessageType.COURIER_INFO, {
            'entity': self.entity,
            'cost': self.entity.cost,
            'point': self.entity.init_point,
        })
        self.actor_system.tell( self.reference_book.agents_entities[message.msg_body], response_message)

    def request_order_assign(self, message, sender):
        requested_entity: OrderEntity = message.msg_body['entity']
        logging.log(logging.INFO, f"Courier {self.entity.name} was requested for order assignment")

        can_take = True
        for order in self.orders:
            if (order.time_from < requested_entity.time_to and order.time_to > requested_entity.time_from):
                can_take = False  # Указываем, что заказ нельзя взять из-за пересечения
                break  # Выходим из цикла, так как уже нашли пересечение

        message = Message(MessageType.ORDER_ASSIGN_RESPONSE, can_take)

        # курьер добавил к себе заказ к выполнению
        self.actor_system.tell(self.reference_book.agents_entities[requested_entity], message)

        # TODO если курьер не может взять заказ или уходит с работы - сообщает об этом агентам своих заказов


    def provide_delivery_intervals(self, message, sender):
        intervals = self.calculate_delivery_intervals()
        response_message = Message(MessageType.DELIVERY_INTERVALS, {'intervals': intervals, 'courier': self})
        self.dispatcher.actor_system.tell(sender, response_message)

    def calculate_delivery_intervals(self):
        # Placeholder for the actual logic
        return ["09:00-11:00", "13:00-15:00", "17:00-19:00"]

