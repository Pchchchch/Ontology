import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path("data/L0_raw")
OUT.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

airports = pd.DataFrame({
    "airport_code": ["ICN","GMP","NRT","HND","PVG","HKG","SIN","LAX","SFO","JFK"],
    "name": ["Incheon","Gimpo","Narita","Haneda","Pudong","Hong Kong","Changi","Los Angeles","San Francisco","JFK"],
    "country": ["KR","KR","JP","JP","CN","HK","SG","US","US","US"],
})

airlines = pd.DataFrame({
    "airline_code": ["KE","OZ","JL","NH","UA","AA","DL","SQ"],
    "name": ["Korean Air","Asiana","JAL","ANA","United","American","Delta","Singapore Airlines"],
})

n = 5000
dates = pd.date_range("2025-01-01", "2025-03-31", freq="D")
dep = np.random.choice(airports["airport_code"], size=n)
arr = np.random.choice(airports["airport_code"], size=n)
arr = np.where(arr == dep, np.random.choice(airports["airport_code"], size=n), arr)

base_delay = np.random.gamma(shape=2.0, scale=7.0, size=n)  # 평균 약 14분
hub_boost = np.isin(dep, ["ICN","HND","LAX","JFK"]).astype(int) * np.random.uniform(3, 10, size=n)
weather_spike = (np.random.rand(n) < 0.03).astype(int) * np.random.uniform(30, 120, size=n)

flights = pd.DataFrame({
    "flight_id": [f"F{i:06d}" for i in range(n)],
    "date": np.random.choice(dates, size=n),
    "airline_code": np.random.choice(airlines["airline_code"], size=n),
    "dep_airport": dep,
    "arr_airport": arr,
    "delay_min": np.round(base_delay + hub_boost + weather_spike, 1),
})

airports.to_parquet(OUT / "airports.parquet", index=False)
airlines.to_parquet(OUT / "airlines.parquet", index=False)
flights.to_parquet(OUT / "flights.parquet", index=False)

print("L0_raw generated:", OUT)
