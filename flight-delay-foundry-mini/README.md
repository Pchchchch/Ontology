This is a simplefied version to briefly demonstrate the ontology process.

# Flight Delay Foundry Mini

A Palantir-style operational analytics demo project.

## Concept

This project demonstrates a Foundry-like data architecture:

L0_raw → L1_clean → L2_modeled → L3_metrics → L4_decision

Instead of simple analytics, it focuses on:
- Ontology-based modeling
- Network metrics
- Decision simulation

## How to Run

```bash
pip install -r requirements.txt
python pipelines/00_generate_sample_data.py
python pipelines/01_clean.py
python pipelines/02_model_network.py
python pipelines/03_metrics.py
python pipelines/04_decision_sim.py
streamlit run app/dashboard.py


