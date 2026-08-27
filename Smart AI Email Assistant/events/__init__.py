"""Event-driven workflow triggers — Redis Streams + Kafka adapters."""

from Smartai.events.dispatcher import EventDispatcher, WorkflowTrigger
from Smartai.events.redis_consumer import RedisStreamsConsumer

__all__ = ["EventDispatcher", "RedisStreamsConsumer", "WorkflowTrigger"]
