"""
역할: availability_365 중심의 핵심 EDA 요약을 dict로 생성.
- price 컬럼을 가정하지 않음
- README/리포트에 바로 넣을 수 있는 요약 통계를 생성
"""

import pandas as pd


def quick_eda(df: pd.DataFrame) -> dict:
    out: dict = {}

    out["n_rows"] = int(len(df))
    out["n_cols"] = int(df.shape[1])
    out["columns"] = list(df.columns)

    # Target summary (availability_365)
    if "availability_365" in df.columns:
        out["availability_desc"] = df["availability_365"].describe().to_dict()
        out["availability_zero_ratio"] = float((df["availability_365"] == 0).mean())
        out["availability_full_ratio"] = float((df["availability_365"] == 365).mean())
    else:
        out["availability_desc"] = {}
        out["availability_zero_ratio"] = None
        out["availability_full_ratio"] = None

    # Categorical summaries
    if "neighbourhood_group_cleansed" in df.columns:
        out["top_neighbourhood_groups"] = (
            df["neighbourhood_group_cleansed"].value_counts().head(10).to_dict()
        )
    else:
        out["top_neighbourhood_groups"] = {}

    if "room_type" in df.columns:
        out["room_type_counts"] = df["room_type"].value_counts().to_dict()
    else:
        out["room_type_counts"] = {}

    # Numeric quick stats (optional)
    numeric_cols = [
        c for c in [
            "accommodates",
            "bedrooms",
            "beds",
            "minimum_nights",
            "number_of_reviews",
            "reviews_per_month",
        ]
        if c in df.columns
    ]
    out["numeric_desc"] = {c: df[c].describe().to_dict() for c in numeric_cols}

    return out