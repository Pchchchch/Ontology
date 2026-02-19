import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Flight Delay Foundry Mini", layout="wide")

st.title("✈️ Flight Delay Foundry Mini (Palantir-style demo)")
st.caption("Layers: L0→L4 | Ontology-backed modeling | Metrics + Decision simulation")

kpi_path = Path("data/L3_metrics/airport_kpi.parquet")
shock_path = Path("data/L4_decision/shock_results.parquet")

col1, col2 = st.columns(2)

with col1:
    st.subheader("L3 Metrics: Airport KPI")
    if kpi_path.exists():
        kpi = pd.read_parquet(kpi_path)
        st.dataframe(kpi, use_container_width=True)
    else:
        st.warning("Run pipelines up to 03_metrics.py first.")

with col2:
    st.subheader("L4 Decision: Shock Simulation")
    if shock_path.exists():
        shock = pd.read_parquet(shock_path)
        st.dataframe(shock.sort_values("avg_delay", ascending=False), use_container_width=True)
    else:
        st.warning("Run pipelines up to 04_decision_sim.py first.")
