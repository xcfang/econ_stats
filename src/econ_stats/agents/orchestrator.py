"""Orchestrates multiple agents for one macro research question."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from econ_stats.agents.base import AgentMessage
from econ_stats.agents.roles import DataAgent, MacroAnalystAgent, SynthesisAgent


@dataclass
class MacroResearchOrchestrator:
    """
    Pipeline: data -> analyst -> synthesis.
    Swap agents or add parallel branches without changing UI.
    """

    symbols: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._data = DataAgent()
        self._analyst = MacroAnalystAgent()
        self._synth = SynthesisAgent()

    def run(self, task: str) -> list[AgentMessage]:
        ctx: dict[str, Any] = {"symbols": self.symbols}
        m1 = self._data.run(task, ctx)
        ctx["prior_messages"] = [m1]
        m2 = self._analyst.run(task, ctx)
        ctx["prior_messages"] = [m1, m2]
        m3 = self._synth.run(task, ctx)
        return [m1, m2, m3]
