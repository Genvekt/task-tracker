import asyncio
import logging
from logging import Logger
from typing import Callable, Dict

import aio_pika
from aio_pika.connection import AbstractConnection
from aio_pika.exchange import ExchangeType
from aio_pika.message import AbstractIncomingMessage
from library.rmq_broker.events import Event
from marshmallow import Schema

Handler = Callable[[Event, Logger], None]


class MessageProcessError(Exception):
    """Exception for message processing errors."""


class Consumer:
    """
    RMQ consumer that handles incoming messages.

    It binds durable queue to specific exchange and
    processes incoming messages with provided handlers.
    On processing error messages are re-queued.
    Messages without matching handlers are skipped.
    Message type identified by header 'MessageType'
    """

    def __init__(
        self,
        exchange_name: str,
        exchange_type: ExchangeType,
        queue_name: str,
        routing_key: str,
        handlers: Dict[str, Handler],
        schemas: Dict[str, Schema],
        logger: Logger
    ):
        """
        Consumer initialisation.
        Args:
            exchange_name: Name of source exchange
            exchange_type: Type of source exchange
            queue_name: Name of the reading queue
            routing_key: Rule of the messages filtering in queue
            handlers: Mapping from message type to processing function
            schemas: Mapping from string type to the Event schema
            logger: For logging
        """
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue_name = queue_name
        self._routing_key = routing_key
        self._handlers = handlers
        self._schemas = schemas
        self._logger = logger

    async def start(self, connection: AbstractConnection) -> asyncio.Task:
        """
        Trigger consumer start.
        Args:
            connection: Connection to RMQ
        Returns:
            asyncio task of consumer process
        """
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        exchange = await channel.declare_exchange(
            name=self._exchange_name,
            type=self._exchange_type
        )
        queue = await channel.declare_queue(self._queue_name, auto_delete=False)
        await queue.bind(exchange, routing_key=self._routing_key)
        task = asyncio.create_task(queue.consume(self.process_message))
        self._logger.info(
            f"Start consuming from queue '{self._exchange_name}'"
        )
        return task

    async def process_message(self, message: AbstractIncomingMessage) -> None:
        """
        Route message to handler and requeue on error
        Args:
            message: Message from RMQ queue
        """
        self._logger.info(f"Received message from '{self._exchange_name}' queue.")
        async with message.process(requeue=True, ignore_processed=True):
            message_type = message.headers.get("MessageType")
            if message_type in self._handlers and message_type in self._schemas:
                try:
                    event_data = message.body.decode("utf8")
                    event_schema = self._schemas[message_type]
                    event = event_schema.loads(event_data)
                    self._handlers[message_type](event, self._logger)
                except MessageProcessError:
                    await message.reject()
            else:
                self._logger.info("Message skipped as its type is not supported.")


class Publisher:
    """RMQ publisher that publishes events form internal queue."""
    def __init__(
        self,
        exchange_name: str,
        event_queue: asyncio.Queue[Event],
        logger: Logger,
        schemas: Dict[str, Schema],
        queue_names: list[str] = None,
        routing_key: str | None = None
    ):
        """
        Publisher initialisation.
        Args:
            exchange_name: Name of exchange for publishing
            event_queue: Internal queue with events to publish
            schemas: Mapping from string type to the Event schema
        """
        self._exchange_name = exchange_name
        self._queue = event_queue
        self._schemas = schemas
        self._logger = logger
        self._queue_names = queue_names if queue_names is not None else []
        self._routing_key = routing_key

    async def start(self, is_stopped: asyncio.Future, connection: AbstractConnection) -> None:
        """
        Trigger publisher start.
        Args:
            is_stopped: Future to indicate publish end.
            connection: Connection to RMQ
        """
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name=self._exchange_name,
            type=ExchangeType.FANOUT
        )
        if self._queue is not None:
            for queue_name in self._queue_names:
                queue = await channel.declare_queue(queue_name, auto_delete=False)
                await queue.bind(exchange, routing_key=self._routing_key)

        self._logger.info(f"Start publishing to '{self._exchange_name}' exchange.")
        while not is_stopped.done():
            finished, unfinished = await asyncio.wait([
                is_stopped,
                asyncio.create_task(self._queue.get())
            ], return_when=asyncio.FIRST_COMPLETED)
            for task in finished:
                event: bool | Event = task.result()
                if isinstance(event, bool):
                    continue
                event_type = event.__class__.__name__
                if event_type not in self._schemas:
                    logging.warning(f"Skipping event ast its type is not supported: {event.__dict__}")
                schema = self._schemas[event_type]
                await exchange.publish(
                    aio_pika.Message(
                        body=schema.dumps(event).encode("utf8"),
                        headers={"MessageType": event_type}
                    ),
                    routing_key=event_type,
                )
                self._logger.info(f"Message was published {event}")


class RMQBroker:
    def __init__(
        self,
        rmq_url: str,
        logger: Logger
    ):
        """
        Broker initialisation.
        Args:
            rmq_url: URL to the RMQ service
            logger: Logger for printing.
        """
        self._rmq_url: str = rmq_url
        self.consumers: list[Consumer] = []
        self.publisher: Publisher | None = None
        self._is_stopped: asyncio.Future = asyncio.Future()
        self._is_stopped.set_result(True)
        self._connection: AbstractConnection | None = None
        self._logger: Logger = logger
        self._running_consumers: list[asyncio.Task] = []

    def add_consumer(
        self,
        exchange_name: str,
        exchange_type: ExchangeType,
        queue_name: str,
        routing_key: str,
        handlers: Dict[str, Handler],
        schemas: Dict[str, Schema],
    ) -> None:
        """
        Adds consumer to broker.
        Args:
            exchange_name: Name of source exchange
            exchange_type: Type of source exchange
            queue_name: Name of the reading queue
            routing_key: Rule of the messages filtering in queue
            handlers: Mapping from message type to processing function
            schemas: Mapping from string type to the Event schema
        """
        self.consumers.append(Consumer(
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            queue_name=queue_name,
            routing_key=routing_key,
            handlers=handlers,
            schemas=schemas,
            logger=self._logger
        ))

    def set_publisher(
        self,
        exchange_name: str,
        event_queue: asyncio.Queue,
        schemas: Dict[str, Schema],
        queue_names: list[str] = None,
        routing_key: str | None = None
    ) -> None:
        """
        Sets publisher to broker.
        Args:
            exchange_name: Name of exchange for publishing
            event_queue: Internal queue with events to publish
            schemas: Mapping from string type to the Event schema
            queue_names (optional): Optional list of queues to bind with auto_delete=False
            routing_key (optional): Routing key for optional queues
        """
        self.publisher = Publisher(
            exchange_name=exchange_name,
            event_queue=event_queue,
            schemas=schemas,
            logger=self._logger,
            queue_names=queue_names,
            routing_key=routing_key
        )

    async def start(self) -> None:
        """Starts all consumers and publisher."""
        if not self._is_stopped.done():
            self._logger.error("Stop RMQ broker before starting it.")
            return

        self._connection = await aio_pika.connect(
            self._rmq_url
        )
        for consumer in self.consumers:
            consumer_task = await consumer.start(connection=self._connection)
            self._running_consumers.append(consumer_task)

        if self.publisher:
            self._is_stopped = asyncio.Future()
            await self.publisher.start(
                is_stopped=self._is_stopped,
                connection=self._connection
            )

    def stop(self) -> None:
        """Stops all running consumers and publisher."""
        self._is_stopped.set_result(True)
        for consumer_task in self._running_consumers:
            consumer_task.cancel()
        self._running_consumers = []
        self._logger.info("RMQ broker stopped.")
