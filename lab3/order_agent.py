import logging

from sqlalchemy.event import dispatcher

from agent_base import AgentBase
from order_entity import OrderEntity
from message import MessageType, Message

class OrderAgent(AgentBase):
    """
    Класс агента заказа
    """
    def __init__(self):
        super().__init__()
        self.entity: OrderEntity
        self.name = 'Агент заказа'
        self.type = 'ORDER'
        self.courier_infos = []
        self.unavailabe_couriers = []
        self.subscribe(MessageType.INIT_MESSAGE, self.handle_init_message)
        self.subscribe(MessageType.COURIER_INFO, self.listen_couriers)
        self.subscribe(MessageType.ORDER_ASSIGN_RESPONSE, self.handle_order_assignment_response)

    def handle_init_message(self, message, sender,):
        self.dispatcher = message.msg_body.get('dispatcher')
        self.actor_system = message.msg_body['actor_system']
        self.scene = message.msg_body['scene']
        self.entity = message.msg_body['entity']
        self.reference_book = message.msg_body['reference_book']
        courier_entities = self.scene.entities['COURIER']
        courier_addresses = list(map(lambda courier: self.reference_book.agents_entities[courier], courier_entities))

        for courier in courier_addresses:
            self.actor_system.tell(courier, Message(MessageType.REQUEST_COURIER_INFO, self.entity))

    def select_best_courier(self):
        best_courier = None
        min_cost = float('inf')

        for info in self.courier_infos:
            courier = info['entity']
            if courier in self.unavailabe_couriers:
                continue
            courier_location = info['point']
            cost = info['cost']
            order_location = self.entity.point_from

            distance = self.calculate_distance(courier_location, order_location)

            if distance * cost < min_cost:
                min_cost = distance * cost
                best_courier = courier

        if best_courier:
            self.request_order_assignment(best_courier)


    def listen_couriers(self, message, sender):
        self.courier_infos.append(message.msg_body)

        courier_count = self.dispatcher.count_entities('COURIER')
        if len(self.courier_infos) == courier_count:
            self.select_best_courier()
        elif len(self.courier_infos) > courier_count:
            self.courier_infos = []
        else:
            pass

    def request_order_assignment(self, courier):
        message = Message(MessageType.REQUEST_ORDER_ASSIGN, {'entity': self.entity})
        self.send(self.reference_book.agents_entities[courier], message)

    def handle_order_assignment_response(self, message, sender):
        if message.msg_body:
            self.unavailabe_couriers = [] # order was taken
            logging.log(logging.INFO, f"Order {self.entity.name} assigned to courier")
        else:
            self.unavailabe_couriers.append(sender) # order could not be taken
            self.select_best_courier()

    def schedule_delivery(self, courier, interval):
        schedule_message = Message(MessageType.SCHEDULE_DELIVERY, {'interval': interval, 'order': self})
        self.dispatcher.actor_system.tell(courier, schedule_message)

    def calculate_distance(self, point1, point2):
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)
