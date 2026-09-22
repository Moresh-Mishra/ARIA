from dataclasses import dataclass, field
from typing import Any


@dataclass
class SakhaState:
    current_task: str | None = None

    context: dict[str, Any] = field(default_factory=dict)

    active_tasks: dict[str, Any] = field(default_factory=dict)

    permissions: dict[str, bool] = field(default_factory=dict)