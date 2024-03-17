import json
from typing import Any
from config import Settings
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

settings = Settings()


def key_serializer(key: Any):
    return json.dumps(key).encode(encoding="utf-8")


def value_serializer(value: Any):
    return json.dumps(value).encode(encoding="utf-8")


def key_deserializer(key: str | bytes | bytearray):
    return json.loads(key).decode(encoding="utf-8")


def value_deserializer(value: str | bytes | bytearray):
    return json.loads(value)


async def aio_kafka_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
        value_serializer=value_serializer,
    )


async def aio_kafka_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        bootstrap_servers=settings.testgate_kafka_bootstrap_servers,
        value_deserializer=value_deserializer,
    )
