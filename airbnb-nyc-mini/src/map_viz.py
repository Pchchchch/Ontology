import json
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster

from branca.colormap import LinearColormap


def make_heatmap(df: pd.DataFrame, out_html: str, sample: int = 20000) -> None:
    use = df[["latitude", "longitude", "availability_365"]].dropna()
    if len(use) > sample:
        use = use.sample(sample, random_state=42)

    m = folium.Map(
        location=[float(use["latitude"].mean()), float(use["longitude"].mean())],
        zoom_start=11,
        tiles="CartoDB Positron",  # ✅ 더 깔끔한 베이스맵
    )

    heat_data = use[["latitude", "longitude", "availability_365"]].values.tolist()
    HeatMap(heat_data, radius=8, blur=12, max_zoom=13).add_to(m)
    m.save(out_html)


def make_marker_map(df: pd.DataFrame, out_html: str, top_n: int = 1500) -> None:
    use = (
        df.dropna(subset=["latitude", "longitude", "availability_365"])
        .sort_values("availability_365", ascending=False)
        .head(top_n)
    )

    m = folium.Map(
        location=[float(use["latitude"].mean()), float(use["longitude"].mean())],
        zoom_start=11,
        tiles="CartoDB Positron",
    )
    cluster = MarkerCluster().add_to(m)

    cols = [c for c in ["neighbourhood_cleansed", "room_type", "availability_365"] if c in use.columns]

    for _, r in use.iterrows():
        popup = "<br/>".join([f"<b>{c}</b>: {r.get(c, '')}" for c in cols])
        folium.CircleMarker(
            location=[float(r["latitude"]), float(r["longitude"])],
            radius=3,
            weight=0.3,
            fill=True,
            fill_opacity=0.6,
            popup=folium.Popup(popup, max_width=320),
        ).add_to(cluster)

    m.save(out_html)


def _detect_geojson_name_key(gj: dict) -> str | None:
    if "features" not in gj or not gj["features"]:
        return None
    props = gj["features"][0].get("properties", {})
    keys = list(props.keys())
    candidates = ["neighbourhood", "neighborhood", "name", "neighbourhood_group", "neighbourhood_cleansed"]
    for c in candidates:
        if c in keys:
            return c
    for k in keys:
        lk = k.lower()
        if "neigh" in lk or "name" in lk:
            return k
    return None


def make_neighbourhood_choropleth_styled(
    df: pd.DataFrame,
    neighbourhood_geojson_path: str,
    out_html: str,
    agg: str = "median",  # "median" or "mean"
) -> bool:
    """
    ✅ 디자인 튜닝 버전 (Austin 예시처럼 '진한 파랑 ↔ 노랑' 대비 + 깔끔한 타일)
    """
    if "neighbourhood_cleansed" not in df.columns:
        return False

    with open(neighbourhood_geojson_path, "r", encoding="utf-8") as f:
        gj = json.load(f)

    key = _detect_geojson_name_key(gj)
    if key is None:
        return False

    if agg == "mean":
        agg_df = (
            df.groupby("neighbourhood_cleansed")["availability_365"]
            .mean()
            .reset_index()
            .rename(columns={"neighbourhood_cleansed": "neigh", "availability_365": "value"})
        )
        title = "Mean availability_365"
    else:
        agg_df = (
            df.groupby("neighbourhood_cleansed")["availability_365"]
            .median()
            .reset_index()
            .rename(columns={"neighbourhood_cleansed": "neigh", "availability_365": "value"})
        )
        title = "Median availability_365"

    # 값 범위
    vmin = float(agg_df["value"].min())
    vmax = float(agg_df["value"].max())
    if vmin == vmax:
        vmax = vmin + 1.0

    # ✅ "진한 파랑 -> 밝은 회색 -> 노랑" 느낌 커스텀 팔레트
    # (Austin 예시와 최대한 비슷한 대비)
    colors = [
        "#08306B",  # deep blue
        "#08519C",
        "#2171B5",
        "#6BAED6",
        "#DEEBF7",  # very light blue
        "#FEE8A3",  # light yellow
        "#FDBE6F",
        "#F59E0B",  # deeper yellow/orange
    ]
    cmap = LinearColormap(colors=colors, vmin=vmin, vmax=vmax)
    cmap.caption = title

    m = folium.Map(
        location=[float(df["latitude"].mean()), float(df["longitude"].mean())],
        zoom_start=11,
        tiles="CartoDB Positron",
    )

    # join dict
    value_by_neigh = dict(zip(agg_df["neigh"], agg_df["value"]))

    def style_fn(feature):
        name = feature["properties"].get(key)
        v = value_by_neigh.get(name, None)
        if v is None:
            return {
                "fillColor": "#FFFFFF",
                "color": "#999999",
                "weight": 0.6,
                "fillOpacity": 0.05,
            }
        return {
            "fillColor": cmap(v),
            "color": "#FFFFFF",     # ✅ 경계선을 하얗게 (예시처럼)
            "weight": 1.0,
            "fillOpacity": 0.70,    # ✅ 색 강도
        }

    def highlight_fn(_):
        return {"weight": 2.5, "color": "#222222"}

    folium.GeoJson(
        gj,
        name="availability choropleth",
        style_function=style_fn,
        highlight_function=highlight_fn,
        tooltip=folium.GeoJsonTooltip(
            fields=[key],
            aliases=["Area:"],
            sticky=True,
        ),
    ).add_to(m)

    cmap.add_to(m)
    m.save(out_html)
    return True


def make_neighbourhood_choropleth_png(
    df: pd.DataFrame,
    neighbourhood_geojson_path: str,
    out_png: str,
    agg: str = "median",
    label: bool = True,
) -> bool:
    """
    ✅ '아까 첨부한 이미지' 스타일에 더 가까운 정적 PNG:
    - 면적 채색 + 경계선 + 컬러바 + (옵션) 라벨
    - geopandas가 있으면 가장 깔끔하게 출력됨.
    """
    try:
        import geopandas as gpd
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
    except Exception:
        # geopandas 설치가 안 되어 있으면 PNG 생성은 스킵
        return False

    if "neighbourhood_cleansed" not in df.columns:
        return False

    gdf = gpd.read_file(neighbourhood_geojson_path)

    # 어떤 컬럼이 이름인지 자동 탐지
    name_key = None
    for cand in ["neighbourhood", "neighborhood", "name", "neighbourhood_cleansed"]:
        if cand in gdf.columns:
            name_key = cand
            break
    if name_key is None:
        # fallback: 첫 번째 object 컬럼
        obj_cols = [c for c in gdf.columns if gdf[c].dtype == "object"]
        if obj_cols:
            name_key = obj_cols[0]
        else:
            return False

    if agg == "mean":
        agg_df = df.groupby("neighbourhood_cleansed")["availability_365"].mean().reset_index()
        title = "Average Airbnb Availability per Neighbourhood (availability_365)"
    else:
        agg_df = df.groupby("neighbourhood_cleansed")["availability_365"].median().reset_index()
        title = "Median Airbnb Availability per Neighbourhood (availability_365)"

    agg_df = agg_df.rename(columns={"neighbourhood_cleansed": name_key, "availability_365": "value"})

    # merge
    gdf = gdf.merge(agg_df, on=name_key, how="left")

    # custom colormap (blue->yellow 느낌)
    colors = ["#08306B", "#2171B5", "#6BAED6", "#DEEBF7", "#FEE8A3", "#FDBE6F", "#F59E0B"]
    cmap = LinearSegmentedColormap.from_list("blue_yellow_custom", colors)

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_axis_off()
    ax.set_title(title, fontsize=16)

    gdf.plot(
        column="value",
        cmap=cmap,
        linewidth=0.8,
        edgecolor="white",
        legend=True,
        ax=ax,
        missing_kwds={"color": "lightgrey", "edgecolor": "white", "hatch": "///"},
        legend_kwds={"shrink": 0.8},
    )

    if label:
        # 너무 촘촘하면 라벨이 지저분해질 수 있어, 기본은 on이지만 필요하면 False로
        # centroid는 geographic CRS에서 왜곡될 수 있으니 projection이 필요하지만 미니 프로젝트에서는 단순 처리
        gdf["centroid"] = gdf.geometry.centroid
        for _, r in gdf.dropna(subset=["centroid"]).iterrows():
            x, y = r["centroid"].x, r["centroid"].y
            name = str(r.get(name_key, ""))
            if name:
                ax.text(x, y, name, fontsize=6, ha="center", va="center")

    plt.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)
    return True