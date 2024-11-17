import numbers

from thespian.actors import *


class CalculatorActor(Actor):
    def receiveMessage(self, msg, sender):
        operation = msg.get('operation')
        operand1 = msg.get('operand1')
        operand2 = msg.get('operand2')

        if operation and operand1 is not None and operand2 is not None:
            result = None
            if operation == 'add':
                result = operand1 + operand2
            elif operation == 'subtract':
                result = operand1 - operand2
            elif operation == 'multiply':
                result = operand1 * operand2
            elif operation == 'divide':
                if operand2 != 0:
                    result = operand1 / operand2
                else:
                    result = 'Error: Division by zero'

            print(
                f'Актор-калькулятор с адресом {self.myAddress} выполнил операцию {operation} с {operand1} и {operand2}, результат: {result}')
            # Отправить результат отправителю, если необходимо
            self.send(sender, result)
        else:
            print(f'Некорректное сообщение от {sender}: {msg}')


class NumberActor(Actor):
    def receiveMessage(self, msg, sender):
        if isinstance(msg, numbers.Number):
            print(f'Ответ от {sender}: {msg}')
        else:
            calculator_address = msg.get('calculator_address')
            operation = msg.get('operation')
            operand1 = msg.get('operand1')
            operand2 = msg.get('operand2')

            if calculator_address and operation in ['add', 'subtract', 'multiply', 'divide']:
                calc_msg = {
                    'operation': operation,
                    'operand1': operand1,
                    'operand2': operand2
                }
                # Отправляем сформированное сообщение к калькулятору
                self.send(calculator_address, calc_msg)


def main():
    actorSystem = ActorSystem()
    print('________________________________')
    print('Запускаем работу системы с калькулятором')

    # Создаем актор-калькулятор и сохраняем его адрес.
    calculator_address = actorSystem.createActor(CalculatorActor)

    # Создаем актор-число
    number_agent = actorSystem.createActor(NumberActor)

    # Отправляем актору числа сообщение с операцией сложения
    add_message = {
        'operation': 'add',
        'operand1': 10,
        'operand2': 5,
        'calculator_address': calculator_address
    }
    actorSystem.tell(number_agent, add_message)

    # Отправляем актору числа сообщение с операцией вычитания
    subtract_message = {
        'operation': 'subtract',
        'operand1': 10,
        'operand2': 5,
        'calculator_address': calculator_address
    }
    actorSystem.tell(number_agent, subtract_message)

    # Отправляем актору числа сообщение с операцией умножения
    multiply_message = {
        'operation': 'multiply',
        'operand1': 10,
        'operand2': 5,
        'calculator_address': calculator_address
    }
    actorSystem.tell(number_agent, multiply_message)

    # Отправляем актору числа сообщение с операцией деления
    divide_message = {
        'operation': 'divide',
        'operand1': 10,
        'operand2': 5,
        'calculator_address': calculator_address
    }
    actorSystem.tell(number_agent, divide_message)


if __name__ == '__main__':
    main()