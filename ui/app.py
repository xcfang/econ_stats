import json
from pathlib import Path
import time
import threading

import streamlit as st
import yfinance as yf
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

CONFIG_FILE = Path("agent_configs.json")
AUTOSAVE_INTERVAL = 1  # 自动保存周期，单位秒



def load_agent_configs():
    if not CONFIG_FILE.exists():
        return None
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_agent_configs(configs):
    try:
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(configs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存 Agent 配置失败: {e}")


def maybe_save_agent_configs():
    cur = st.session_state.get("agent_configs", [])
    last = st.session_state.get("agent_configs_last_saved")
    last_save_time = st.session_state.get("agent_configs_last_save_time", 0)
    current_time = time.time()
    
    # 检测是否有改动且距离上次保存超过间隔时间
    if cur != last and (current_time - last_save_time) >= AUTOSAVE_INTERVAL:
        st.session_state["is_saving"] = True
        save_agent_configs(cur)
        st.session_state["agent_configs_last_saved"] = [dict(x) for x in cur]
        st.session_state["agent_configs_last_save_time"] = current_time
        st.session_state["is_saving"] = False
        return True
    return False


# --- 1. 状态定义 ---
class AgentState(TypedDict):
    target: str
    indicators: List[str]
    data_results: dict
    current_step: str  # 用于 UI 显示当前状态

# --- 2. Agent 逻辑（带 UI 反馈） ---
def researcher_node(state: AgentState):
    # 更新 UI 状态
    st.session_state.current_agent = "理论研究员"
    st.session_state.logs.append("🔍 理论研究员正在查阅《预测》周期理论...")
    
    # 模拟 Prompt 处理（实际可从 UI 获取）
    target = state['target']
    # 这里为了演示直接给出逻辑，实际可接入 LLM
    indicators = ["Forward_PE", "Dividend_Yield"] 
    return {"indicators": indicators, "current_step": "Data Collection"}

def collector_node(state: AgentState):
    st.session_state.current_agent = "数据获取 Agent"
    st.session_state.logs.append(f"📡 正在通过 yfinance 获取 {state['indicators']}...")
    
    ticker = yf.Ticker(state['target'])
    results = {ind: ticker.info.get(ind, "N/A") for ind in state['indicators']}
    
    return {"data_results": results, "current_step": "Finished"}

# --- 3. Streamlit UI 布局 ---
st.set_page_config(page_title="金融 AI Agent 控制台", layout="wide")

st.title("🤖 金融多 Agent 协作系统")

# Agent 配置初始化（放在底部）
if "agent_configs" not in st.session_state:
    saved = load_agent_configs()
    if saved is not None and isinstance(saved, list):
        st.session_state.agent_configs = saved
    else:
        st.session_state.agent_configs = [
            {
                "角色": "理论研究员",
                "prompt": "基于周期理论，列出标的的关键量化指标...",
            },
            {
                "角色": "数据 Agent",
                "prompt": "使用 yfinance API 抓取指定指标...",
            },
        ]
        save_agent_configs(st.session_state.agent_configs)

    # 建立 last_saved 缓存以避免重复写入
    st.session_state["agent_configs_last_saved"] = [dict(x) for x in st.session_state.agent_configs]
    st.session_state["agent_configs_last_save_time"] = time.time()


# 主界面分栏
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 当前运行状态")
    target_input = st.text_input("输入投资标的 (如: NVDA, AAPL)", "NVDA")
    
    if st.button("开始分析"):
        st.session_state.logs = []
        # 构建并运行 Graph (简化版演示)
        workflow = StateGraph(AgentState)
        workflow.add_node("researcher", researcher_node)
        workflow.add_node("collector", collector_node)
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "collector")
        workflow.add_edge("collector", END)
        app = workflow.compile()
        
        with st.spinner('Agent 团队协作中...'):
            result = app.invoke({"target": target_input, "logs": []})
            st.session_state.final_result = result

    # 显示实时日志
    if 'logs' in st.session_state:
        for log in st.session_state.logs:
            st.caption(log)

with col2:
    st.subheader("📦 任务产出")
    if 'final_result' in st.session_state:
        res = st.session_state.final_result
        st.write(f"**分析对象:** {res['target']}")
        
        st.info(f"**理论员建议关注:** {', '.join(res['indicators'])}")
        
        st.write("**实时数据结果:**")
        st.table(res['data_results'])
        
        st.success("✅ 流程执行完毕，等待整合 Agent 进一步分析。")

# 底部展示与增删改查Agent配置
# 每秒强制刷新实现定时保存检测
if hasattr(st, "autorefresh"):
    st.autorefresh(interval=int(AUTOSAVE_INTERVAL * 1000), key="agent_config_autorefresh")

with st.expander("📊 Agent 配置与管理", expanded=True):
    st.markdown("使用文本输入直接编辑 Agent 名称和 Prompt，失焦或回车自动保存。")

    if "agent_configs" not in st.session_state:
        st.session_state.agent_configs = []

    # 增删逻辑
    if st.button("➕ 新增 Agent"):
        st.session_state.agent_configs.append({"角色": "新 Agent", "prompt": "请输入 Prompt..."})
        maybe_save_agent_configs()

    # Per-row editing controls
    for i, agent in enumerate(st.session_state.agent_configs.copy()):
        st.markdown(f"---\n**Agent #{i + 1}**")
        role_key = f"agent_role_{i}"
        prompt_key = f"agent_prompt_{i}"

        if role_key not in st.session_state:
            st.session_state[role_key] = agent.get("角色", "")
        if prompt_key not in st.session_state:
            st.session_state[prompt_key] = agent.get("prompt", "")

        role_val = st.text_input("Agent 名称", value=st.session_state[role_key], key=role_key)
        prompt_val = st.text_area("Prompt", value=st.session_state[prompt_key], key=prompt_key)

        if role_val != agent.get("角色") or prompt_val != agent.get("prompt"):
            st.session_state.agent_configs[i] = {"角色": role_val, "prompt": prompt_val}
        
        # 每次输入后立即检测保存
        maybe_save_agent_configs()

        delete_col, _ = st.columns([1, 5])
        with delete_col:
            if st.button("🗑️ 删除", key=f"delete_agent_{i}"):
                st.session_state.agent_configs.pop(i)
                # 清理对应临时输入状态
                st.session_state.pop(role_key, None)
                st.session_state.pop(prompt_key, None)
                maybe_save_agent_configs()

    maybe_save_agent_configs()

    # 统一显示保存状态
    if st.session_state.get("is_saving", False):
        st.info("💾 正在保存...")
    elif st.session_state.get("agent_configs_last_saved") is not None:
        st.success("✅ 已保存")

    st.markdown("### 当前配置摘要")
    st.table(st.session_state.agent_configs)

