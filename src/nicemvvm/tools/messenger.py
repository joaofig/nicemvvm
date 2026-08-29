from collections.abc import Awaitable, Callable

from nicemvvm.tools.singleton import singleton
from nicemvvm.tools.tasks import ManagedTasks


class Messenger:
    def __init__(self):
        self.handlers = {}

    async def broadcast(self, message: str, **kwargs):
        mt = ManagedTasks()
        if message in self.handlers:
            for handler in self.handlers[message]:
                if handler is not None and isinstance(handler, Callable):
                    mt.create(handler(**kwargs))

    async def send(self, message: str, **kwargs):
        await self.broadcast(message, **kwargs)

    def subscribe(
        self, message: str, handler: Callable[..., None | Awaitable[None]]
    ) -> None:
        if message not in self.handlers:
            self.handlers[message] = [handler]
        else:
            self.handlers[message].append(handler)


@singleton
class MessengerHub:
    def __init__(self):
        self.hub = {}

    def __getitem__(self, message) -> Messenger:
        if message not in self.hub:
            self.hub[message] = Messenger()
        return self.hub[message]


def get_messenger(name: str) -> Messenger:
    return MessengerHub()[name]


async def send_message(messenger: str, message: str, **kwargs):
    msg = get_messenger(messenger)
    if msg:
        await msg.send(message, **kwargs)
