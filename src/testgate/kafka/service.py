import asyncio
import json
from typing import Any
from config import Settings
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

settings = Settings()


def key_serializer(key: Any):
    return json.dumps(key).encode(encoding='utf-8')


def value_serializer(value: Any):
    return json.dumps(value).encode(encoding='utf-8')


def key_deserializer(key: str | bytes | bytearray):
    return json.loads(key).decode(encoding='utf-8')


def value_deserializer(value: str | bytes | bytearray):
    return json.loads(value)


# aio_kafka_producer = AIOKafkaProducer(bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
#                                       key_serializer=key_serializer,
#                                       value_serializer=value_serializer)
#
#
# aio_kafka_consumer = AIOKafkaConsumer(bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
#                                       key_deserializer=key_deserializer,
#                                       value_deserializer=value_deserializer)

async def aio_kafka_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
                            value_serializer=value_serializer)


async def aio_kafka_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
                            value_deserializer=value_deserializer)


# async def aio_kafka_producer(topic: Any, value: Any = None, key: Any = None):
#     producer = AIOKafkaProducer(bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
#                                 key_serializer=key_serializer,
#                                 value_serializer=value_serializer)
#     await producer.start()
#     try:
#         response = await producer.send_and_wait(topic=topic, value=value, key=key)
#     finally:
#         await producer.stop()
#     return response


# async def aio_kafka_consumer(*topics: Any, group_id: str | None, session: Session, ):
#     consumer = AIOKafkaConsumer(topics,
#                                 bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
#                                 group_id=group_id,
#                                 key_deserializer=key_deserializer,
#                                 value_deserializer=value_deserializer)
    # await consumer.start()
    # try:
    #     async for msg in consumer:
    #         print("consumed: ", msg.topic, msg.partition, msg.offset,
    #               msg.key, msg.value, msg.timestamp)
    # finally:
    #     await consumer.stop()


async def email_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9094')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("email", b"Super message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def email_consumer():
    consumer = AIOKafkaConsumer(
        'email',
        bootstrap_servers='localhost:9094',
        group_id="email")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()