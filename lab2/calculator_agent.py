from thespian.actors import ActorAddress
from agent_base import AgentBase
from message import *


class CalculatorAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.subscribe(MessageType.OPERATION, self.handle_init)

    def handle_init(self, message: Message, sender: ActorAddress):
        if message.msg_type == MessageType.OPERATION:
            body: Optional[OperationMessageBody] = message.msg_body
            if body:
                operation = body.operation
                operand1 = body.operand1
                operand2 = body.operand2

                try:
                    result = self._perform_operation(operation, operand1, operand2)
                except Exception as e:
                    result = f'Error: {str(e)}'

                print(
                    f'CalculatorAgent with address {self.myAddress} performed operation {operation} on {operand1} and {operand2}, result: {result}')
            else:
                print(f'Invalid message body from {sender}: {message}')
        else:
            print(f'Unsupported message type from {sender}: {message}')

    def _perform_operation(self, operation: OperationType, operand1: float, operand2: float) -> Any:
        match operation:
            case OperationType.ADD:
                return operand1 + operand2
            case OperationType.SUBTRACT:
                return operand1 - operand2
            case OperationType.MULTIPLY:
                return operand1 * operand2
            case OperationType.DIVIDE:
                return operand1 / operand2 if operand2 != 0 else 'Error: Division by zero'
            case OperationType.POWER:
                return operand1 ** operand2
            case OperationType.MODULUS:
                return operand1 % operand2
            case OperationType.MAX:
                return max(operand1, operand2)
            case OperationType.MIN:
                return min(operand1, operand2)
            case _:
                return f'Error: Unsupported operation {operation}'