# Supply Chain & Inventory Optimization Analytics

## Overview
A beginner-friendly analytics project exploring product demand, stock levels, supplier lead times, and simplified reorder-point estimates using Python, Pandas, SQLite SQL, and Matplotlib.

## Dataset
`inventory_demand.csv` contains synthetic illustrative data generated for this project. It is not real company data.

Columns:
- `date`: observation date
- `product_id`: synthetic product identifier
- `demand_units`: demand recorded in the observation period
- `inventory_on_hand`: inventory on hand at the observation
- `supplier_lead_time_days`: supplier lead time in days
- `unit_cost`: illustrative unit cost
- `supplier`: synthetic supplier label

## Tools
Python, Pandas, SQLite SQL, Matplotlib.

## How to run
Install Python 3.10 or newer, then run from this folder:

```bash
pip install -r requirements.txt
python supply_chain_analysis.py
```

## Outputs
The script creates an `outputs/` folder with:
- `product_inventory_summary.csv`
- `supplier_summary.csv`
- `sql_supplier_summary.csv`
- `inventory_analytics.db`
- `demand_by_product.png`
- `lead_time_vs_reorder_point.png`

## Methods
- Clean and validate fields, remove duplicate records, and aggregate demand by product.
- Summarize supplier lead times, average stock, and unit costs.
- Estimate reorder points using average daily demand multiplied by average lead time.
- Query supplier-level metrics with SQLite and generate charts.

## Limitations
The dataset is synthetic and the reorder-point formula is a simplified planning estimate. The observation frequency and assumptions must be validated before applying this method to a real business. Do not claim the results are from a real company.

## Suggested extensions
- Add safety stock using demand variability and lead-time variability.
- Build an Excel or Power BI dashboard.
- Compare forecast methods and evaluate errors on a real, documented dataset.
