import asyncio
from collections import defaultdict
from typing import Callable, Awaitable, Any


class EventBus:
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[dict], Awaitable[Any]]
    ):
        self.listeners[event_type].append(handler)

    async def publish(self, event_type: str, data: dict):
        handlers = self.listeners.get(event_type, [])

        await asyncio.gather(
            *(handler(data) for handler in handlers)
        )