from collections.abc import Callable
from typing import Any

from nicegui.binding import BindableProperty


class Bindable(BindableProperty):
    """
    A BindableProperty that can be used to create bindable properties in a class.
    It allows for automatic change tracking and notification of changes.
    """

    def __init__(self, on_change: Callable[..., Any] | None = None):
        super().__init__(on_change=on_change)

    def change_handler(self, handler: Callable[..., Any] | None = None):
        """
        Set the change handler for the bindable property.
        The handler will be called whenever the property value changes.
        """
        self._change_handler = handler
