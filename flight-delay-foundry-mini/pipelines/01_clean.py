import pandas as pd
from pathlib import Path

INP = Path("data/L0_raw")
OUT = Path("data/L1_clean")
OUT.mkdir(parents=True, exist_ok=True)

flights = pd.read_parquet(INP / "flights.parquet")
airports = pd.read_parquet(INP / "airports.parquet")
airlines = pd.read_parquet(INP / "airlines.parquet")

# 기본 정제
flights["date"] = pd.to_datetime(flights["date"])
flights = flights[(flights["delay_min"] >= 0) & (flights["delay_min"] <= 600)]
flights = flights.dropna()

# 참조 무결성
valid_airports = set(airports["airport_code"])
flights = flights[flights["dep_airport"].isin(valid_airports) & flights["arr_airport"].isin(valid_airports)]

valid_airlines = set(airlines["airline_code"])
flights = flights[flights["airline_code"].isin(valid_airlines)]

flights.to_parquet(OUT / "flights_clean.parquet", index=False)
airports.to_parquet(OUT / "airports.parquet", index=False)
airlines.to_parquet(OUT / "airlines.parquet", index=False)

print("✅ L1_clean saved:", OUT)
