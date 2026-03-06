from pathlib import Path
import json

from src.config import (
    DATA_RAW,
    DATA_PROCESSED,
    FIGURES,
    MAPS,
    LISTINGS_URL,
    RAW_LISTINGS_GZ,
    RAW_NEIGH_GEOJSON,
    NEIGH_GEOJSON_URL,
    PROCESSED_PARQUET,
    MODEL_PATH,
)

from src.download import download_file
from src.preprocess import load_raw_listings, basic_clean_listings, save_parquet
from src.eda import quick_eda
from src.model import train_eval_save
from src.map_viz import (
    make_heatmap,
    make_marker_map,
    make_neighbourhood_choropleth_styled,
    make_neighbourhood_choropleth_png,
)


def save_json(d, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    for p in [DATA_RAW, DATA_PROCESSED, FIGURES, MAPS]:
        p.mkdir(parents=True, exist_ok=True)

    print("[1] download")
    download_file(LISTINGS_URL, RAW_LISTINGS_GZ, overwrite=False)
    download_file(NEIGH_GEOJSON_URL, RAW_NEIGH_GEOJSON, overwrite=False)

    print("[2] preprocess")
    raw = load_raw_listings(str(RAW_LISTINGS_GZ))
    df = basic_clean_listings(raw)
    save_parquet(df, str(PROCESSED_PARQUET))

    print("[3] eda")
    info = quick_eda(df)
    save_json(info, Path("reports/eda_summary.json"))

    print("[4] model")
    metrics = train_eval_save(df, str(MODEL_PATH))
    save_json(metrics, Path("reports/model_metrics.json"))

    print("[5] maps")
    make_heatmap(df, str(MAPS / "availability_heatmap.html"))
    make_marker_map(df, str(MAPS / "availability_markers.html"))

    ok_html = make_neighbourhood_choropleth_styled(
        df,
        str(RAW_NEIGH_GEOJSON),
        str(MAPS / "availability_choropleth_styled.html"),
        agg="median",
    )
    print(f"[info] choropleth styled html: {ok_html}")

    # 정적 PNG (Austin 예시 형태에 가장 근접)
    ok_png = make_neighbourhood_choropleth_png(
        df,
        str(RAW_NEIGH_GEOJSON),
        str(FIGURES / "availability_choropleth.png"),
        agg="median",
        label=True,
    )
    print(f"[info] choropleth png: {ok_png} (needs geopandas)")

    print("done")


if __name__ == "__main__":
    main()