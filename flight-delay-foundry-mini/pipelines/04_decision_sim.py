import pandas as pd
from pathlib import Path

INP1 = Path("data/L1_clean")
OUT = Path("data/L4_decision")
OUT.mkdir(parents=True, exist_ok=True)

flights = pd.read_parquet(INP1 / "flights_clean.parquet")

def simulate_shock(dep_airport: str, delay_multiplier: float = 1.5):
    sim = flights.copy()
    shocked = sim["dep_airport"].eq(dep_airport)
    sim.loc[shocked, "delay_min"] = sim.loc[shocked, "delay_min"] * delay_multiplier

    # 결과 KPI: 전체 평균 지연, 상위 10% 지연 비율
    avg_delay = sim["delay_min"].mean()
    p90 = sim["delay_min"].quantile(0.9)
    high_ratio = (sim["delay_min"] >= p90).mean()

    return {
        "shock_airport": dep_airport,
        "multiplier": delay_multiplier,
        "avg_delay": round(float(avg_delay), 2),
        "p90_delay": round(float(p90), 2),
        "high_delay_ratio": round(float(high_ratio), 4),
    }

airports = sorted(flights["dep_airport"].unique())
rows = [simulate_shock(a, 1.7) for a in airports]
pd.DataFrame(rows).to_parquet(OUT / "shock_results.parquet", index=False)

print("✅ L4_decision saved:", OUT)
