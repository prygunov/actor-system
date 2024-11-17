from enum import Enum
from dataclasses import dataclass
from typing import Any

class MessageType(Enum):
    INITIALIZATION = 'Инициализация'
    OPERATION = 'Операция'

class OperationType(Enum):
    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'
    POWER = 'power'
    MODULUS = 'modulus'
    MAX = 'max'
    MIN = 'min'

@dataclass
class Message:
    msg_type: MessageType
    msg_body: Any

@dataclass
class OperationMessageBody:
    operation: OperationType
    operand1: float
    operand2: float
