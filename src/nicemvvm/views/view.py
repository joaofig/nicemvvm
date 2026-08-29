from collections.abc import Awaitable, Callable

from nicemvvm.tools.messenger import get_messenger
from nicemvvm.viewmodels.view_model import ViewModel


class View:
    def __init__(self, vm: ViewModel):
        self.vm = vm

    @staticmethod
    async def broadcast(channel: str, message: str, **kwargs):
        """Broadcast a message to all registered handlers on the given channel"""
        messenger = get_messenger(channel)
        await messenger.send(message, **kwargs)

    @staticmethod
    def subscribe(
        channel: str, message: str, handler: Callable[..., None | Awaitable[None]]
    ):
        """Subscribe a handler to a message on the given channel"""
        messenger = get_messenger(channel)
        messenger.subscribe(message, handler)
