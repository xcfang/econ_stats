# econ_stats

多 agent 协作、基于量化数据做宏观经济研究的实验项目。目标仓库：[github.com/xcfang/econ_stats](https://github.com/xcfang/econ_stats)。

## 结构

- `src/econ_stats/agents/` — `BaseAgent`、具体角色（数据 / 宏观分析 / 综合）、`MacroResearchOrchestrator` 编排
- `src/econ_stats/data/` — 时间序列清洗与对齐（占位）
- `ui/app.py` — Streamlit 界面；把你的「生成 UI」代码接在 `render_custom_panel()` 或拆成独立模块再 import

## 本地 setup

```bash
cd econ_stats
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## 运行 UI

```bash
streamlit run ui/app.py
```

不执行 `pip install -e .` 时，可在仓库根目录：

```bash
PYTHONPATH=src streamlit run ui/app.py
```

## 推到 GitHub

若本地尚未关联远程：

```bash
cd econ_stats
git init
git remote add origin https://github.com/xcfang/econ_stats.git
git add .
git commit -m "Scaffold multi-agent macro research and Streamlit UI"
git branch -M main
git push -u origin main
```

若远程已有 README-only 历史，可能需要 `git pull --rebase origin main` 后再 push。

## 下一步

- 在 `roles.py` 中把 stub 换成真实 LLM 调用或规则引擎
- 在 `data/` 接入 FRED、Wind、本地 parquet 等
- 在 `ui/app.py` 的 `render_custom_panel()` 合并你的可视化与交互逻辑
