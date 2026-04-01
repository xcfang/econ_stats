# econ_stats

多 agent 协作、基于量化数据做宏观经济研究的实验项目。目标仓库：[github.com/xcfang/econ_stats](https://github.com/xcfang/econ_stats)。

## 结构

- `src/econ_stats/agents/` — `BaseAgent`、具体角色（数据 / 宏观分析 / 综合）、`MacroResearchOrchestrator` 编排
- `src/econ_stats/data/` — 时间序列清洗与对齐（占位）
- `ui/app.py` — Streamlit 界面；把你的「生成 UI」代码接在 `render_custom_panel()` 或拆成独立模块再 import

