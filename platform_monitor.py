import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime

# Page Configuration for Enterprise Dashboard Layout
st.set_page_config(page_title="MLOps Infraguard Engine", page_icon="⚙️", layout="wide")

st.title("⚙️ MLOps Docker Orchestrator & Cluster Control Plane")
st.caption("Staff-Architect Platform View | Idempotent Node Infrastructure & Distributed Pipeline Telemetry")

# --- INITIALIZE DISTRIBUTED SYSTEM STATE ---
if "pipeline_stage" not in st.session_state:
    st.session_state.pipeline_stage = "Idle"
if "node_cluster" not in st.session_state:
    st.session_state.node_cluster = {
        "ingress-worker-01": {"status": "HEALTHY", "cpu": 12.4, "memory": 42.1, "uptime": "14d 06h"},
        "training-blade-02": {"status": "HEALTHY", "cpu": 8.1, "memory": 14.8, "uptime": "43d 11h"},
        "inference-node-alpha": {"status": "HEALTHY", "cpu": 18.9, "memory": 55.3, "uptime": "08d 22h"}
    }
if "orchestration_logs" not in st.session_state:
    st.session_state.orchestration_logs = []

def log_event(level, service, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    st.session_state.orchestration_logs.insert(0, f"[{timestamp}] [{level}] [{service}] {message}")

# --- SIDEBAR: CHAOS ENGINEERING RUNTIME CONTROLLER ---
st.sidebar.header("💥 Chaos Engineering Engine")
st.sidebar.markdown("Inject deterministic failure modes into running container daemons to evaluate platform auto-recovery.")

target_node = st.sidebar.selectbox("Select Target Cluster Node", list(st.session_state.node_cluster.keys()))

if st.sidebar.button("💀 Kill Active Container Thread"):
    st.session_state.node_cluster[target_node]["status"] = "CRASH_LOOP_BACKOFF"
    st.session_state.node_cluster[target_node]["cpu"] = 0.0
    st.session_state.node_cluster[target_node]["memory"] = 0.0
    log_event("CRITICAL", target_node, "SIGKILL signal propagated. Container runtime terminated abruptly.")
    st.toast(f"Injected container failure into {target_node}!", icon="🔥")

if st.sidebar.button("♻️ Trigger Idempotent Cluster Re-Provision (Ansible/IaC)"):
    with st.spinner("Executing infrastructure-as-code state synchronization..."):
        time.sleep(1.0)
        for node in st.session_state.node_cluster:
            if st.session_state.node_cluster[node]["status"] != "HEALTHY":
                st.session_state.node_cluster[node]["status"] = "HEALTHY"
                st.session_state.node_cluster[node]["uptime"] = "0h 01m"
                log_event("INFO", node, "Container re-provisioned via configuration state convergence.")
    st.success("Desired cluster state restored successfully.")

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Manual Pipeline Traversal")
if st.sidebar.button("▶️ Execute Full MLOps Pipeline Job"):
    st.session_state.pipeline_stage = "Data Ingestion"

# --- TOP LEVEL ARCHITECTURAL METRICS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    healthy_nodes = sum(1 for n in st.session_state.node_cluster.values() if n["status"] == "HEALTHY")
    st.metric("Cluster Convergence State", f"{healthy_nodes} / {len(st.session_state.node_cluster)} Nodes", 
              delta="Nominal" if healthy_nodes == len(st.session_state.node_cluster) else "-1 Node Degraded", 
              delta_color="normal" if healthy_nodes == len(st.session_state.node_cluster) else "inverse")
with col_m2:
    st.metric("Orchestrator Scheduler Latency", f"{random.uniform(0.85, 1.42):.2f} ms", delta="SLA Target < 5ms")
with col_m3:
    st.metric("Telemetry Pipeline Throughput", "84.2k events/sec", delta="Prometheus Scrape Active")
with col_m4:
    st.metric("Global Active Replica Count", "12 Containers", delta="Auto-Scale Standard")

st.markdown("---")

# --- PIPELINE DIRECTED ACYCLIC GRAPH (DAG) VISUALIZER ---
st.subheader("📊 MLOps Pipeline Orchestration Graph (DAG State Machine)")

# Logic to smoothly transition steps sequentially if triggered
stages = ["Idle", "Data Ingestion", "Feature Validation", "Model Training", "Image Compilation", "Registry Promotion"]
if st.session_state.pipeline_stage != "Idle":
    current_idx = stages.index(st.session_state.pipeline_stage)
    if current_idx < len(stages) - 1:
        time.sleep(0.6)  # Simulate running state execution boundaries
        st.session_state.pipeline_stage = stages[current_idx + 1]
        log_event("INFO", "SCHEDULER", f"Transitioned task node state to: {st.session_state.pipeline_stage}")
    else:
        st.session_state.pipeline_stage = "Idle"
        log_event("SUCCESS", "SCHEDULER", "Pipeline execution cycle completed. State machine reclaimed resources.")

# Render horizontal visual pipeline blocks
cols = st.columns(len(stages) - 1)
for i, stage in enumerate(stages[1:]):
    with cols[i]:
        if st.session_state.pipeline_stage == stage:
            st.markdown(f"<div style='background-color:#1E3A8A; border:2px solid #3B82F6; padding:15px; border-radius:8px; text-align:center; color:white; font-weight:bold;'>🔄 {stage}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#1E293B; border:1px solid #475569; padding:15px; border-radius:8px; text-align:center; color:#94A3B8;'>⏳ {stage}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- WORKER NODE CLUSTER MATRIX ---
st.subheader("🖥️ Distributed Container Runtime Matrix")
node_data = []
for name, metrics in st.session_state.node_cluster.items():
    # Jitter live hardware readings for simulation authenticity
    if metrics["status"] == "HEALTHY":
        metrics["cpu"] = max(2.0, min(98.0, metrics["cpu"] + random.uniform(-1.5, 1.5)))
        metrics["memory"] = max(5.0, min(95.0, metrics["memory"] + random.uniform(-0.5, 0.5)))
        
    node_data.append({
        "Container Worker Identity": name,
        "Orchestration Status": metrics["status"],
        "CPU Load (%)": round(metrics["cpu"], 1),
        "Memory Consumption (%)": round(metrics["memory"], 1),
        "Cluster Node Uptime": metrics["uptime"]
    })

df_nodes = pd.DataFrame(node_data)

def style_cluster_nodes(val):
    if val == "HEALTHY": return "background-color: rgba(16, 185, 129, 0.2); color: #10b981; font-weight: bold;"
    if val == "CRASH_LOOP_BACKOFF": return "background-color: rgba(239, 68, 68, 0.2); color: #ef4444; font-weight: bold;"
    return ""

st.dataframe(
    df_nodes.style.map(style_cluster_nodes, subset=["Orchestration Status"])
                  .background_gradient(cmap="Blues", subset=["CPU Load (%)", "Memory Consumption (%)"]),
    use_container_width=True,
    hide_index=True
)

# --- OBSERVABILITY LOG STREAM ---
st.markdown("---")
st.subheader("📜 Live Orchestrator System Trace Events JSON/Standard Stream")

if st.session_state.orchestration_logs:
    log_text = "\n".join(st.session_state.orchestration_logs[:20])
    st.code(log_text, language="text")
else:
    st.info("System logging daemon silent. Telemetry loops reporting clear buffer matrices.")

# Automatically trigger page reruns for continuous performance monitoring update loops
time.sleep(1.0)
st.rerun()
