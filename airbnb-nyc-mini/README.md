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
3. reports/maps/availability_choropleth.html
4. reports/maps/availability_choropleth_styled.html


1. heatmap
<img width="637" height="674" alt="image" src="https://github.com/user-attachments/assets/15be88fd-7632-4203-b275-a323ccd2e521" />

2. markers
<img width="638" height="673" alt="image" src="https://github.com/user-attachments/assets/9244b9fa-e439-4b3d-9d04-e1f2068345d9" />

3. choropleth
<img width="639" height="672" alt="image" src="https://github.com/user-attachments/assets/f1650ebd-5adf-443f-bb7f-c637ca902a69" />

4. choropleth_styled 
<img width="639" height="673" alt="image" src="https://github.com/user-attachments/assets/ba69bcb9-05c3-471d-8cbd-add308ee0a4a" />

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

