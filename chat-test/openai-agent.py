from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError
import requests

# Настройки для Zookeeper
ZOOKEEPER_HOSTS = '127.0.0.1:2181'

# Настройки OpenAI
API_URL = 'https://api.openai.com/v1/example'
API_KEY = 'your_openai_api_key'

# Создаем клиента Zookeeper
zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
zk.start()

# Регистрация агента в Zookeeper
AGENT_NODE_PATH = "/agents/agent1"

try:
    zk.create(AGENT_NODE_PATH, ephemeral=True, makepath=True)
    print("Узел создан.")
except NodeExistsError:
    print("Узел уже существует. Прерывание.")
    zk.stop()
    exit()


def handle_request(request_data):
    # Пример обработки запроса и обращения к API OpenAI
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.post(API_URL, headers=headers, json=request_data)
    return response.json()


def forward_request_to_other_agent():
    # Здесь должна быть логика для обращения к другому агенту
    # Например, выберите случайного доступного агента и отправьте ему запрос
    children = zk.get_children("/agents")
    if children:
        for child in children:
            print(f"Доступен агент: {child}")


# Основная логика работы агента
try:
    while True:
        # Пример простой работы агента: получение API данных и печать результата
        # На самом деле здесь можно организовать ваш агент по-другому
        request_data = {
            'input': 'Hello, world!'
        }

        response_data = handle_request(request_data)
        print(f"Response from OpenAI: {response_data}")

        forward_request_to_other_agent()
finally:
    # Очистка при завершении работы
    zk.stop()
    zk.close()