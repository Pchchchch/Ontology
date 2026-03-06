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

1. reports/maps/availability_heatmap.html
2. reports/maps/availability_markers.html
3. reports/maps/availability_choropleth_styled.html

1.
<img width="637" height="674" alt="image" src="https://github.com/user-attachments/assets/15be88fd-7632-4203-b275-a323ccd2e521" />

2.

3.

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

