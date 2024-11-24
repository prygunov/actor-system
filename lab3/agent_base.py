from abc import ABC
from typing import Dict, Callable, Any, List
import logging
import traceback
from thespian.actors import Actor, ActorAddress
from message import MessageType, Message

MBV = ABC

class AgentBase(MBV, Actor):
    def __init__(self):
        self.name = 'Базовый агент'
        self.handlers: Dict[MessageType, Callable[[Any, ActorAddress], None]] = {}
        self.subscribe(MessageType.INIT_MESSAGE, self.handle_init_message)
    
    def subscribe(self, msg_type: MessageType, handler: Callable[[Any, ActorAddress], None]):
        """
        Подписка на события определенного типа
        :param msg_type: Тип события
        :param handler: Обработчик сообщения заданного типа
        :return:
        """
        if msg_type in self.handlers:
            logging.warning('Повторная подписка на сообщение: %s', msg_type)
        self.handlers[msg_type] = handler

    def receiveMessage(self, msg, sender):
        """Обрабатывает сообщения - запускает их обработку в зависимости от типа.
        :param msg:
        :param sender:
        :return:
        """
        logging.debug('%s получил сообщение: %s', self.name, msg)
        if isinstance(msg, Message):
            message_type = msg.msg_type
            if message_type in self.handlers:
                try:
                    self.handlers[message_type](msg, sender)
                except Exception as ex:
                    traceback.print_exc()
                    logging.error(ex)
            else:
                logging.warning('%s Отсутствует подписка на сообщение: %s', self.name, message_type)
        
    def handle_init_message(self, message, sender):
        """
        Обработка сообщения с инициализацией - сохранение присланных данных в агенте.
        :param message:
        :param sender:
        :return:
        """
        message_data = message.msg_body
        self.scene = message_data.get('scene')
        self.dispatcher = message_data.get('dispatcher')
        self.entity = message_data.get('entity')
        self.name = self.name + ' ' + self.entity.name
        logging.info(f'{self} - проинициализирован')

