from thespian.actors import *
from reference_book import ReferenceBook
from lab6.base_entity import BaseEntity
from message import MessageType, Message
from lab6.agent_base import AgentBase

from lab6.courier_agent import CourierAgent
from lab6.order_agent import OrderAgent

TYPES_AGENTS = {
    'COURIER': CourierAgent,
    'ORDER': OrderAgent,
}

class AgentsDispatcher:
    """
    Класс диспетчера агентов
    """
    def __init__(self, scene):
        self.actor_system = ActorSystem()
        self.reference_book = ReferenceBook()
        self.scene = scene

    def add_entity(self, entity: BaseEntity):
        """
        Добавляет сущность в сцену, создает агента и отправляет ему сообщение об инициализации
        :param entity:
        :return:
        """
        entity_type = entity.get_type()
        agent_type = TYPES_AGENTS.get(entity_type)
        if not agent_type:
            logging.warning(f'Для сущности типа {entity_type} не указан агент')
            return False
        self.scene.entities[entity_type].append(entity)
        self.create_agent(agent_type, entity)
        return True

    def create_agent(self, agent_class, entity):
        """
        Создает агента заданного класса с привязкой к сущности
        :param agent_class:
        :param entity:
        :return:
        """
        agent = self.actor_system.createActor(agent_class)
        self.reference_book.add_agent(entity=entity, agent_address=agent)
        init_data = {
            'dispatcher': self,
            'scene': self.scene,
            'entity': entity,
            'actor_system': self.actor_system,
            'reference_book': self.reference_book,
        }
        init_message = Message(MessageType.INIT_MESSAGE, init_data)
        self.actor_system.tell(agent, init_message)

    def remove_agent(self, entity: BaseEntity):
        """
        Удаляет сущность из сцены и из адресной книги
        :param entity:
        :return:
        """
        destroy_message = Message(MessageType.DESTROY_MESSAGE, {"entity": entity})
        entity_type = entity.get_type()
        self.scene.entities[entity_type].remove(entity)
        self.actor_system.tell(self.reference_book.agents_entities[entity], destroy_message)
        self.reference_book.remove_agent(entity)


    def get_entities(self, entity_type) -> list[AgentBase]:
        return self.scene.entities[entity_type]

    def count_entities(self, entity_type) -> int:
        return len(self.get_entities(entity_type))