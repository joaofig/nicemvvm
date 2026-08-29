# Utilities & Tools

This folder contains utility objects, helper functions, and architectural tools used throughout the application to support UI binding, background tasks, data validation, and session management.

## Available Tools

### UI & Binding Helpers
- **Bindable** (`bindable.py`): A wrapper around NiceGUI's `BindableProperty` that allows class properties to participate in the framework's change tracking and notification system.
- **Observability** (`observability.py`):
    - `Observable`: A base class providing a standard implementation of the Observer pattern, allowing objects to register handlers and notify them of state changes.
    - `GridList`: A specialized version of NiceGUI's `ObservableList` optimized for AgGrid, adding helper methods like `replace()` and `delete()` for easier data manipulation.

### Communication & Tasks
- **Messenger** (`messenger.py`): A lightweight, named message dispatch system that allows decoupled components to communicate via `subscribe()` and `broadcast()`. It uses `ManagedTasks` to handle handlers asynchronously.
- **ManagedTasks** (`tasks.py`): A singleton service for tracking and managing `asyncio` tasks globally. It ensures that background tasks are properly recorded and provides a mechanism to cancel all pending tasks during application shutdown.

### Data & Validation
- **Excel Export** (`excel.py`): Provides the `export_to_excel` utility, which converts a list of dictionaries into an `.xlsx` file using Pandas and triggers a browser download via NiceGUI.
- **Validation** (`validation.py`): Contains helper functions for common validation needs, such as `is_date()` and `is_email()`.

### Session & Utilities
- **User & Session Helpers** (`user.py`): Utilities for managing NiceGUI user sessions (e.g., `logout`, `get_user_name`) and robust date/time conversion functions (`str_to_date`, `dict_to_datetime`) that handle parsing and default values.
- **Singleton** (`singleton.py`): A class decorator that implements the Singleton pattern, ensuring a class has only one instance across the application.

### Architectural Patterns
- The tools in this directory promote a decoupled architecture, using **Singletons** for global services, the **Observer** pattern for state updates, and **Managed Tasks** for safe asynchronous execution.
