from thespian.actors import ActorAddress
from agent_base import AgentBase
from message import Message, MessageType, OperationMessageBody, OperationType


class NumberAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.subscribe(MessageType.INITIALIZATION, self.handle_initialization)

    def handle_initialization(self, message: Message, sender: ActorAddress):
        calculator_address = message.msg_body.get('calculator_address')
        operation_str = message.msg_body.get('operation')
        operand1 = message.msg_body.get('operand1')
        operand2 = message.msg_body.get('operand2')

        try:
            operation = OperationType(operation_str)
        except ValueError:
            operation = None

        if calculator_address and operation in OperationType:
            calc_msg = OperationMessageBody(
                operation=operation,
                operand1=operand1,
                operand2=operand2
            )
            self.send(calculator_address, Message(MessageType.OPERATION, calc_msg))
        else:
            print(f'Invalid operation or calculator address in message: {message}')
