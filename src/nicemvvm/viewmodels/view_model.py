import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from nicemvvm.tools.messenger import get_messenger


class ViewModel(ABC):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def broadcast(channel: str, message: str, **kwargs):
        """Broadcast a message to all registered handlers on the given channel"""
        messenger = get_messenger(channel)
        await messenger.send(message, **kwargs)

    @staticmethod
    def subscribe(
        channel: str,
        *,
        message: str | None = None,
        messages: list[str] | None = None,
        handler: Callable[..., None | Awaitable[None]],
    ) -> None:
        """Subscribe a handler to a message on the given channel"""
        messenger = get_messenger(channel)
        if message:
            messenger.subscribe(message, handler)
        elif messages:
            for msg in messages:
                messenger.subscribe(msg, handler)

    async def call(self, msg: str, **kwargs):
        """Use this method to call methods in the ViewModel. It will call the _on_call method and return the result."""
        result = self._on_call(msg, **kwargs)
        if result is not None and asyncio.iscoroutine(result):
            return await result
        return result

    @abstractmethod
    async def _on_call(self, msg: str, **kwargs) -> Any:
        """Base method for handling messages sent to the ViewModel"""
        return None

    def get(self, name: str, default: Any = None) -> Any:
        """Get the value of a property from the ViewModel"""
        if not hasattr(self, name):
            if default is not None:
                return default
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
        return getattr(self, name)

    def set(self, name: str, value: Any) -> None:
        """Set the value of a property on the ViewModel"""
        if not hasattr(self, name):
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
        setattr(self, name, value)
