from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentMessage:
    role: str
    content: str
    meta: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Single agent: receives context, returns structured text (later: tool calls)."""

    name: str = "agent"

    @abstractmethod
    def run(self, task: str, context: dict[str, Any]) -> AgentMessage:
        ...
