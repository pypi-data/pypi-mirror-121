import json
from typing import Any

from car_finder.utils.log_utils import get_logger
from pika import BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosed
from pika.exchange_type import ExchangeType

logger = get_logger(__name__)


class PikaUtilsError(BaseException):
    "Utils Exception"


def validate_queue(connection: BlockingConnection, queue) -> bool:
    ch = open_channel_from_connection(connection)
    try:

        ch.queue_declare(queue=queue, passive=True)
        close_channel(ch)
        return True
    except ChannelClosed:
        close_channel(ch)

        return False


def create_queue(connection: BlockingConnection, queue) -> bool:
    ch = open_channel_from_connection(connection)
    logger.info(f"Creating Queue: '{queue}'")
    if ch.queue_declare(queue=queue):
        close_channel(ch)
        return True
    else:
        return False


def delete_queue(connection: BlockingConnection, queue, if_empty=False, if_unused=False) -> bool:
    ch = open_channel_from_connection(connection)
    results = ch.queue_delete(queue=queue, if_empty=if_empty, if_unused=if_unused)
    close_channel(ch)
    if results:
        logger.info(f"Removing Queue: {queue}")
        return True
    else:
        return False


def purge_queue(connection: BlockingConnection, queue):
    ch = open_channel_from_connection(connection)
    if ch.is_open:
        logger.info(f"Purging Queue: {queue}")
        ch.queue_purge(queue=queue)
        return True

    else:
        raise PikaUtilsError(f"{ch.channel_number} is Closed")


def create_exchange(connection: BlockingConnection, exchange: str, exchange_type='direct') -> bool:
    ch = open_channel_from_connection(connection)
    if ExchangeType(exchange_type):
        try:
            ch.exchange_declare(exchange=exchange, exchange_type=ExchangeType(exchange_type).value, durable=True)
        except Exception:
            raise

        close_channel(ch)
        return True
    else:
        return False


def delete_exchange(connection: BlockingConnection, exchange, if_unused=False) -> bool:
    ch = open_channel_from_connection(connection)
    try:
        ch.exchange_delete(exchange=exchange, if_unused=if_unused)
    except Exception:
        raise

    close_channel(ch)
    return True


def bind_queue(connection: BlockingConnection, queue, exchange, routing_key) -> bool:
    ch = open_channel_from_connection(connection)
    try:
        ch.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
        logger.info(f"Binding ({exchange}, {queue}, {routing_key})")
    except Exception:
        raise

    close_channel(ch)
    return True


def unbind_queue(connection: BlockingConnection, queue, exchange, routing_key) -> bool:
    ch = open_channel_from_connection(connection)
    try:
        ch.queue_unbind(queue=queue, exchange=exchange, routing_key=routing_key)
    except Exception:
        raise

    close_channel(ch)
    return True


def open_channel_from_connection(connection: BlockingConnection) -> BlockingChannel:
    if connection.is_open:
        channel = connection.channel()
        logger.info(f"Opened Channel: {channel.channel_number}")
        return channel
    else:
        raise PikaUtilsError(f"{connection} is Closed")


def close_channel(channel: BlockingChannel):
    if channel.is_open:
        logger.info(f"Closing Channel: {channel.channel_number}")
        channel.close()
        return True
    else:
        return False


def close_connection(connection: BlockingConnection):
    if connection.is_open:
        logger.info(f"Closing Connection: {str(connection)}")
        connection.close()
        return True
    else:
        return False


def set_channel_qos(channel: BlockingChannel, prefetch_count):
    if channel.is_open:
        channel.basic_qos(prefetch_count=prefetch_count)
        return True
    else:
        raise PikaUtilsError(f"{channel.channel_number} is Closed")


def get_blocking_connection(url) -> BlockingConnection:
    logger.info(f"Connecting to URL: '{url}'")
    return BlockingConnection(
        parameters=URLParameters(url=url)
    )


def publish_message(connection: BlockingConnection, exchange: str, routing_key: str, data: Any) -> bool:
    ch = open_channel_from_connection(connection)
    if ch.is_open:
        try:
            logger.info(f"Publishing Message: {data}")
            if isinstance(data, bytes):
                ch.basic_publish(exchange=exchange, routing_key=routing_key, body=data)

            if isinstance(data, dict):
                ch.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(data).encode())

            close_channel(ch)
            return True
        except Exception:
            raise
    else:

        raise PikaUtilsError(f"{ch.channel_number} is Closed")


def acknowledge_message(channel: BlockingChannel, delivery_tag):
    channel.basic_ack(delivery_tag=delivery_tag)


def nacknowledge_message(channel: BlockingChannel, delivery_tag):
    channel.basic_nack(delivery_tag=delivery_tag)
