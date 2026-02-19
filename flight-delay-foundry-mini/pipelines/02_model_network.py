import pandas as pd
from pathlib import Path

INP = Path("data/L1_clean")
OUT = Path("data/L2_modeled")
OUT.mkdir(parents=True, exist_ok=True)

flights = pd.read_parquet(INP / "flights_clean.parquet")

# 공항 간 연결(엣지): 출발→도착, weight=평균 지연, volume=항공편 수
edges = (flights
         .groupby(["dep_airport","arr_airport"])
         .agg(volume=("flight_id","count"),
              mean_delay=("delay_min","mean"))
         .reset_index())

edges["mean_delay"] = edges["mean_delay"].round(2)
edges.to_parquet(OUT / "airport_edges.parquet", index=False)

print("✅ L2_modeled saved:", OUT)
