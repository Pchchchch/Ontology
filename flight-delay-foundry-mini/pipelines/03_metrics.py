import pandas as pd
import networkx as nx
from pathlib import Path

INP = Path("data/L2_modeled")
OUT = Path("data/L3_metrics")
OUT.mkdir(parents=True, exist_ok=True)

edges = pd.read_parquet(INP / "airport_edges.parquet")

G = nx.DiGraph()
for r in edges.itertuples(index=False):
    # 비용(가중치)은 mean_delay, 강도는 volume
    G.add_edge(r.dep_airport, r.arr_airport, mean_delay=float(r.mean_delay), volume=int(r.volume))

# 중심성: 구조적 허브(연결), 지연 가중 허브(가중치 기반은 여기선 간단 지표로 대체)
deg = dict(G.degree())
bet = nx.betweenness_centrality(G, normalized=True)
pr = nx.pagerank(G, alpha=0.85, weight="volume")

kpi = pd.DataFrame({
    "airport": list(G.nodes()),
    "degree": [deg[a] for a in G.nodes()],
    "betweenness": [bet[a] for a in G.nodes()],
    "pagerank_volume": [pr[a] for a in G.nodes()],
})

kpi = kpi.sort_values("pagerank_volume", ascending=False)
kpi.to_parquet(OUT / "airport_kpi.parquet", index=False)

print("✅ L3_metrics saved:", OUT)
