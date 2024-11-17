from thespian.actors import *
from calculator_agent import CalculatorAgent
from number_agent import NumberAgent
from message import Message, MessageType

if __name__ == '__main__':
    actorSystem = ActorSystem()
    calculator_address = actorSystem.createActor(CalculatorAgent)
    number_agent = actorSystem.createActor(NumberAgent)

    messages = [
        {'operation': 'add', 'operand1': 22, 'operand2': 1, 'calculator_address': calculator_address},
        {'operation': 'subtract', 'operand1': 33, 'operand2': 2, 'calculator_address': calculator_address},
        {'operation': 'multiply', 'operand1': 55, 'operand2': 3, 'calculator_address': calculator_address},
        {'operation': 'divide', 'operand1': 41, 'operand2':5 , 'calculator_address': calculator_address},
        {'operation': 'max', 'operand1': -41, 'operand2':5 , 'calculator_address': calculator_address},
        {'operation': 'min', 'operand1': -41, 'operand2':5 , 'calculator_address': calculator_address},
        {'operation': 'modulus', 'operand1': 21, 'operand2':5 , 'calculator_address': calculator_address},
        {'operation': 'divide', 'operand1': 11, 'operand2': 0, 'calculator_address': calculator_address},
    ]

    for msg in messages:
        actorSystem.tell(number_agent, Message(MessageType.INITIALIZATION, msg))