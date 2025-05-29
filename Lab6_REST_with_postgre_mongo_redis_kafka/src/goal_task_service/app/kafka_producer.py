import json
import os
from confluent_kafka import Producer

# Получаем адрес Kafka из переменных окружения
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

# Конфигурация Kafka Producer
conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
}

# Создание Producer
producer = Producer(**conf)

# Определяем топики
TASK_TOPIC = 'task_events'

# Функция для обработки результатов доставки сообщения
def delivery_report(err, msg):
    if err is not None:
        print(f'Ошибка доставки сообщения: {err}')
    else:
        print(f'Сообщение доставлено в {msg.topic()} [раздел {msg.partition()}]')

def send_task_event(task_data, event_type='create'):
    """
    Отправляет событие, связанное с задачей, в Kafka
    
    Args:
        task_data: Данные задачи
        event_type: Тип события (create, update, delete)
    """
    # Добавляем тип события в данные
    message = {
        'event_type': event_type,
        'data': task_data
    }
    
    try:
        # Отправляем сообщение
        producer.produce(
            topic=TASK_TOPIC,
            key=str(task_data.get('id', 0)),
            value=json.dumps(message),
            callback=delivery_report
        )
        # Запускаем доставку сообщений (неблокирующий вызов)
        producer.poll(0)
        
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")