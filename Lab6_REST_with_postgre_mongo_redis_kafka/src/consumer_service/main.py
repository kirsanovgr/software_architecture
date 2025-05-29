from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaError
import json
import os
import threading
import time


KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'task_consumer_group')
TASK_TOPIC = 'task_events'

MSGS = []

def process_task_event(event_data):
    """
    Обрабатывает событие задачи из Kafka и сохраняет в базу данных
    """
    try:
        event = json.loads(event_data)
        event_type = event.get('event_type')
        data = event.get('data', {})
        
        info = f"Обработка события {event_type} для задачи: {data.get('title')}"
        print(info)
        MSGS.append(info)
        if event_type == 'create':
            print('Была отправлена команда на создание задачи')
            
            
    except Exception as e:
        print(f"Ошибка при обработке события: {e}")

def start_consumer():
    """
    Запускает потребителя Kafka для обработки сообщений
    """
    print(f"Запуск потребителя Kafka: {KAFKA_BOOTSTRAP_SERVERS}, группа: {KAFKA_GROUP_ID}")
    
    # Конфигурация Kafka Consumer
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'  # Начинать с самого раннего сообщения
    }
    
    # Создание Consumer
    consumer = Consumer(conf)
    
    # Подписка на топик
    consumer.subscribe([TASK_TOPIC])
    
    print(f"Потребитель запущен, ожидание сообщений из топика {TASK_TOPIC}...")
    
    # Цикл для получения сообщений
    try:
        while True:
            msg = consumer.poll(1.0)  # Ожидание сообщения в течение 1 секунды
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            
            # Обработка полученного сообщения
            process_task_event(msg.value().decode('utf-8'))
            
    except KeyboardInterrupt:
        pass
    finally:
        # Закрытие Consumer
        consumer.close()
        
# Запуск потребителя Kafka в отдельном потоке
def run_kafka_consumer():
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.daemon = True  # Поток будет завершен при завершении основного потока
    consumer_thread.start()
    return consumer_thread

app = FastAPI(title='ConsumerService')

@app.get('/')
def get_root():
    return { "massage": f"hello from {app.title}" }

@app.get('/kafka/test')
def get_kafka_test():
    if not MSGS:  # Проверка на пустой список
        return { "massage": "kafka test", "data": "Нет сообщений" }
    return { "massage": "kafka test", "data": MSGS[-1] }

# Запуск потребителя Kafka при старте приложения
@app.on_event("startup")
async def startup_event():
    run_kafka_consumer()

if __name__ == '__main__':
    import uvicorn
    # Запускаем потребителя Kafka в отдельном потоке
    run_kafka_consumer()
    # Запускаем FastAPI приложение
    uvicorn.run(app="main:app", host="0.0.0.0", port=8002)