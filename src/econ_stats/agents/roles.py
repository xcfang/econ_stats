"""Concrete agents (stubs). Replace bodies with LLM + data tools."""

from __future__ import annotations

from typing import Any

from econ_stats.agents.base import AgentMessage, BaseAgent


class DataAgent(BaseAgent):
    name = "quant_data"

    def run(self, task: str, context: dict[str, Any]) -> AgentMessage:
        # TODO: FRED / Wind / 本地 parquet 等
        return AgentMessage(
            role=self.name,
            content=f"[stub] Would load & clean series for: {task!r}",
            meta={"symbols": context.get("symbols", [])},
        )


class MacroAnalystAgent(BaseAgent):
    name = "macro_analyst"

    def run(self, task: str, context: dict[str, Any]) -> AgentMessage:
        return AgentMessage(
            role=self.name,
            content=f"[stub] Would analyze panel / factors for: {task!r}",
            meta={},
        )


class SynthesisAgent(BaseAgent):
    name = "synthesis"

    def run(self, task: str, context: dict[str, Any]) -> AgentMessage:
        prior = context.get("prior_messages", [])
        lines = [f"- {m.role}: {m.content[:200]}..." for m in prior[-3:]]
        body = "\n".join(lines) if lines else "(no prior)"
        return AgentMessage(
            role=self.name,
            content=f"[stub] Summary for {task!r}\n{body}",
            meta={},
        )
