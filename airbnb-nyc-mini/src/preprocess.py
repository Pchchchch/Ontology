import pandas as pd

KEEP_COLS = [
    "id",
    "latitude",
    "longitude",
    "room_type",
    "property_type",
    "accommodates",
    "bedrooms",
    "beds",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "availability_365",
    "neighbourhood_group_cleansed",
    "neighbourhood_cleansed",  # ✅ choropleth 매칭용 (중요)
]


def load_raw_listings(path: str) -> pd.DataFrame:
    return pd.read_csv(path, compression="gzip", low_memory=False)


def basic_clean_listings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    cols = [c for c in KEEP_COLS if c in df.columns]
    df = df[cols]

    df = df.dropna(subset=["latitude", "longitude"])

    if "reviews_per_month" in df.columns:
        df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

    for c in ["bedrooms", "beds"]:
        if c in df.columns:
            df[c] = df[c].fillna(0)

    # choropleth key는 문자열 정리해두는 게 안전
    if "neighbourhood_cleansed" in df.columns:
        df["neighbourhood_cleansed"] = df["neighbourhood_cleansed"].astype(str).str.strip()

    return df


def save_parquet(df: pd.DataFrame, path: str) -> None:
    df.to_parquet(path, index=False)