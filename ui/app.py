"""
Web UI for econ_stats (Streamlit).

把你的「生成 UI」逻辑接进来：
- 在下方 `render_custom_panel()` 里粘贴/调用你的组件；
- 或新建模块并在 `import` 后替换 `render_custom_panel` 的实现。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 允许在未 pip install -e . 时从仓库根目录运行: streamlit run ui/app.py
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

import streamlit as st

from econ_stats.agents.orchestrator import MacroResearchOrchestrator


def render_custom_panel() -> None:
    """在此合并你的初始 UI 代码（图表、表单、多 tab 等）。"""
    st.caption("默认占位：把自定义组件写进 `render_custom_panel()` 或单独模块。")


def main() -> None:
    st.set_page_config(page_title="econ_stats — Macro agents", layout="wide")
    st.title("Quant macro · multi-agent")
    st.markdown(
        "数据层 → **Data** / **Analyst** / **Synthesis** 三阶段（当前为 stub，可接 LLM 与数据源）。"
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        symbols = st.text_input("关注序列（逗号分隔，占位）", "GDP,CPI,FEDFUNDS")
        task = st.text_area("研究问题 / 任务描述", "比较美国 CPI 与联邦基金利率的领先滞后关系（示例）")
        run = st.button("运行 agent 流水线", type="primary")

    with col2:
        if run and task.strip():
            orch = MacroResearchOrchestrator(
                symbols=[s.strip() for s in symbols.split(",") if s.strip()]
            )
            messages = orch.run(task.strip())
            for i, m in enumerate(messages, 1):
                with st.expander(f"Step {i} · {m.role}", expanded=(i == len(messages))):
                    st.write(m.content)
                    if m.meta:
                        st.json(m.meta)
        elif run:
            st.warning("请先填写任务描述。")

    st.divider()
    render_custom_panel()


if __name__ == "__main__":
    main()
