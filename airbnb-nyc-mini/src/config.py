from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

REPORTS = PROJECT_ROOT / "reports"
FIGURES = REPORTS / "figures"
MAPS = REPORTS / "maps"

LISTINGS_URL = "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-12-04/data/listings.csv.gz"

RAW_LISTINGS_GZ = DATA_RAW / "listings.csv.gz"

PROCESSED_PARQUET = DATA_PROCESSED / "listings_clean.parquet"

MODEL_PATH = REPORTS / "availability_model.joblib"

# For geojson
NEIGH_GEOJSON_URL = "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-12-04/visualisations/neighbourhoods.geojson"
RAW_NEIGH_GEOJSON = DATA_RAW / "neighbourhoods.geojson"