# Airbnb NYC Spatial Analysis

## Objective

Identify spatial patterns in Airbnb listings and generate map-based outputs for location comparison.

---
## Outputs

    - Heatmap (listing density by availability)
    - Marker Map (listing-level visualzation)
    - Choropleth Map (neighbourhood availability distribution)

---
## Output files

reports/maps/availability_heatmap.html
reports/maps/availability_markers.html
reports/maps/availability_choropleth_styled.html

---
## Timeline

2026.03.06 __ Phase 1
Initial analysis using InsideAirbnb NYC dataset.

2026.03.06 __ Phase 2
Price data unavailable -> pivot to availability_365 based analysis -> heatmap, marker map, choropleth generated.

2026.03.06 __ Phase 3
Decision made to transition to Kaggle Airbnb NYC 2019 dataset to enable multi-variable decision anaysis.

---
## Structure

data/
reports/
src/

Run

python -m src.main

