import logging

from agent_base import AgentBase
from courier_entity import CourierEntity
from message import MessageType, Message

from lab6.order_entity import OrderEntity


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
        self.subscribe(MessageType.ORDER_DECLINING, self.remove_order)
        self.subscribe(MessageType.DESTROY_MESSAGE, self.decline_orders)

    def handle_init_message(self, message, sender):
        self.dispatcher = message.msg_body['dispatcher']
        self.actor_system = message.msg_body['actor_system']
        self.scene = message.msg_body['scene']
        self.reference_book = message.msg_body['reference_book']
        self.entity = message.msg_body['entity']

    def get_info(self, message, sender):
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
                can_take = False
                break

        current_volume = 0
        for order in self.orders:
            current_volume += order.volume

        if can_take:
            can_take = (self.entity.max_volume - current_volume) >= requested_entity.volume

        message = Message(MessageType.ORDER_ASSIGN_RESPONSE, can_take)
        self.actor_system.tell(self.reference_book.agents_entities[requested_entity], message)

    def decline_orders(self, message, sender):
        for order in self.orders:
            self.actor_system.tell(self.reference_book.agents_entities[order], Message(MessageType.ORDER_ASSIGN_RESPONSE, False))

    def remove_order(self, message, sender):
        order = message.msg_body['entity']
        self.orders.remove(order)
        logging.log(logging.INFO, f"Courier {self.entity.name} declined order {order.name}")


