# nicemvvm

A lightweight, modern Model-View-ViewModel (MVVM) framework designed for [NiceGUI](https://nicegui.io).

`nicemvvm` simplifies state management, UI data-binding, decoupled component communication, and background task execution in NiceGUI applications.

---

## Features

- **MVVM Architecture**: Cleanly decouple presentation markup (`View`) from business logic and state (`ViewModel`).
- **Command & Message Dispatching**: Unified command handling with `ViewModel.call()` and `_on_call()` for asynchronous and synchronous workflows.
- **Event Bus & Messaging**: Publish-subscribe messaging system (`Messenger` / `MessengerHub`) for decoupled inter-component communication across channels.
- **Observable Collections & UI Grids**: Reactive collections like `GridList` (built on NiceGUI's `ObservableList`) optimized for AgGrid data binding with built-in `replace()` and `delete()` operations.
- **Managed Background Tasks**: Global tracking and lifecycle management (`ManagedTasks`) for `asyncio` tasks with safe cancellation on shutdown.
- **Property Binding**: `Bindable` property descriptor for reactive property change notifications.
- **Built-in Utilities**:
  - `@singleton`: Decorator for thread-safe/centralized singleton services.
  - **Excel Export**: Quick browser download of tabular data using Pandas (`export_to_excel`).
  - **Validation**: Common validators like `is_date()` and `is_email()`.
  - **User & Session Helpers**: Session helpers, role checks, and robust date/time parsing utilities (`dict_to_date`, `dict_to_datetime`, etc.).

---

## Installation

Add `nicemvvm` to your project using `uv` or `pip`:

```bash
uv add nicemvvm
```

Or with `pip`:

```bash
pip install nicemvvm
```

### Requirements
- Python `>= 3.14`
- `nicegui >= 3.16.0`
- `pandas >= 3.0.5`
- `openpyxl >= 3.1.5`

---

## Core Concepts & Architecture

### 1. ViewModel (`nicemvvm.view_models.ViewModel`)

`ViewModel` is the abstract base class that encapsulates application state, commands, and communication logic.

```python
from nicemvvm.view_models.view_model import ViewModel
from nicegui import binding

@binding.bindable_dataclass
class CounterViewModel(ViewModel):
    count: int = 0

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "increment":
                self.count += 1
                await self.broadcast("counter", "updated", count=self.count)
            case "reset":
                self.count = 0
                await self.broadcast("counter", "updated", count=self.count)
```

#### Key ViewModel Methods:
- **`call(msg, **kwargs)`**: Invokes the `_on_call` handler (handling async coroutines automatically) and returns the result.
- **`_on_call(msg, **kwargs)`**: Abstract method to implement command routing (e.g. using `match ... case`).
- **`get(name, default=None)` / `set(name, value)`**: Safe dynamic property getter and setter.
- **`broadcast(channel, message, **kwargs)`**: Dispatches an event on the specified messaging channel.
- **`subscribe(channel, *, message=None, messages=None, handler=...)`**: Subscribes a callback to one or more channel messages.

---

### 2. View (`nicemvvm.views.View`)

`View` is the base class for UI components. It holds a reference to a `ViewModel` (`self.vm`) and provides convenience methods for event broadcasting and subscription.

```python
from nicegui import ui
from nicemvvm.views.view import View

class CounterView(View):
    def __init__(self, vm: CounterViewModel):
        super().__init__(vm)
        self.build_ui()

    def build_ui(self):
        with ui.column().classes("items-center p-4"):
            ui.label().bind_text_from(self.vm, "count", backward=lambda c: f"Current Count: {c}")
            with ui.row():
                ui.button("Increment", on_click=lambda: self.vm.call("increment"))
                ui.button("Reset", on_click=lambda: self.vm.call("reset")).props("color=red")
```

---

### 3. Decoupled Event Messaging (`Messenger` & `MessengerHub`)

`nicemvvm` includes a lightweight pub/sub event bus to let disparate views or viewmodels coordinate without direct dependencies.

```python
from nicemvvm.tools.messenger import get_messenger, send_message

# Subscribe to a channel event
messenger = get_messenger("study")
messenger.subscribe("saved", lambda study_id: print(f"Study {study_id} was saved!"))

# Send message on a channel (executed in background via ManagedTasks)
await send_message("study", "saved", study_id=42)
```

`ViewModel` and `View` also expose static helper methods `broadcast` and `subscribe` directly:

```python
# In a ViewModel or View
self.subscribe(channel="patient", messages=["saved", "deleted"], handler=self._refresh_data)
await self.broadcast(channel="patient", message="saved", patient_id=10)
```

---

### 4. Reactive Grid & Observables (`GridList`, `Observable`)

- **`GridList`**: A specialized `ObservableList` subclass designed for table and AgGrid integration. It provides batch manipulation methods:
  - `replace(new_items)`: Clears and replaces all items in one operation.
  - `delete(key, value)`: Filters out items matching the specified key/value.

```python
from nicemvvm.tools.observability import GridList

studies = GridList()
studies.replace([{"id": 1, "name": "Trial A"}, {"id": 2, "name": "Trial B"}])
studies.delete("id", 1)  # Removes Trial A
```

- **`Observable`**: A base class implementing the Observer pattern with async/sync notification support:
  - `register(handler)` / `unregister(handler)`
  - `notify(action, **kwargs)`

---

## Built-in Tools & Utilities

| Tool | Module | Description |
| :--- | :--- | :--- |
| **`ManagedTasks`** | `nicemvvm.tools.tasks` | Singleton task tracker to create and cancel `asyncio` background tasks cleanly. |
| **`Bindable`** | `nicemvvm.tools.bindable` | Wrapper over NiceGUI `BindableProperty` with hook for `change_handler`. |
| **`@singleton`** | `nicemvvm.tools.singleton` | Class decorator to enforce singleton instance pattern. |
| **`export_to_excel`** | `nicemvvm.tools.excel` | Converts list of dictionaries to Excel (`.xlsx`) and triggers a browser download. |
| **`is_date`, `is_email`** | `nicemvvm.tools.validation` | String validation helper functions. |
| **Session & Date Helpers** | `nicemvvm.tools.user` | `logout()`, `record_user_activity()`, `get_user_name()`, `is_user_readonly()`, `dict_to_date()`, `dict_to_datetime()`. |

---

## Example: Master-Detail List with MVVM

```python
from nicegui import ui
from nicemvvm.view_models.view_model import ViewModel
from nicemvvm.views.view import View
from nicemvvm.tools.observability import GridList

# 1. List ViewModel
class ItemListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.items = GridList()
        self.selected_id: int = 0
        self.subscribe(channel="item", messages=["saved", "deleted"], handler=self._reload)

    async def _reload(self, **kwargs):
        # Reload items from database or service
        pass

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self._reload()
            case "select":
                self.selected_id = kwargs.get("item_id", 0)
                await self.broadcast("item", "selected", item_id=self.selected_id)

# 2. View Component
class ItemListView(View):
    def __init__(self, vm: ItemListViewModel):
        super().__init__(vm)
        self.build_ui()

    def build_ui(self):
        ui.label("Items Overview").classes("text-lg font-bold")
        # Bind AgGrid or NiceGUI table to self.vm.items
        ui.table(
            columns=[{"name": "name", "label": "Name", "field": "name"}],
            rows=self.vm.get("items"),
        )
```

---

## Module Structure

```text
nicemvvm/
├── views/
│   └── view.py              # Base View class
├── view_models/
│   └── view_model.py        # Base ViewModel class
└── tools/
    ├── bindable.py          # Bindable property wrapper
    ├── excel.py             # Excel export utility
    ├── messenger.py         # Pub/Sub messenger system
    ├── observability.py     # Observable base and GridList
    ├── singleton.py         # Singleton decorator
    ├── tasks.py             # ManagedTasks background task runner
    ├── user.py              # User session & date conversion helpers
    └── validation.py        # Validation helpers (date, email)
```

---

## License

This project is licensed under the MIT License.
