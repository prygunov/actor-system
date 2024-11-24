import logging

class ReferenceBook:
    """Адресная книга агентов с привязкой к сущностям"""
    def __init__(self):
        self.agents_entities = {}
    
    def add_agent(self, entity, agent_address):
        """
        Сохраняет адрес агента с привязкой с сущности
        :param entity:
        :param agent_address:
        :return:
        """
        self.agents_entities[entity] = agent_address

    def get_address(self, entity):
        """
        Возвращает адрес агента указанной сущности.
        :param entity:
        :return:
        """
        if entity not in self.agents_entities:
            logging.error(f'Агент {entity} отсутствует в адресной книге')
            return None
        return self.agents_entities[entity]

    def remove_agent(self, entity):
        """
        Удаляет агента из адресной книги
        :param entity:
        :return:
        """
        if entity in self.agents_entities:
            del self.agents_entities[entity]
        else:
            logging.error(f'Агент {entity} отсутствует в адресной книге')
            