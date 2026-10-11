"""
Supply Chain & Inventory Analytics
Uses synthetic illustrative data, not real company records.

Run:
    pip install -r requirements.txt
    python supply_chain_analysis.py
"""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "inventory_demand.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(DATA, parse_dates=["date"])
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates()
    for col in ["demand_units", "inventory_on_hand", "supplier_lead_time_days", "unit_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "product_id", "demand_units", "inventory_on_hand",
                           "supplier_lead_time_days", "unit_cost"])

    # Aggregate product-level demand and inventory indicators
    product_summary = df.groupby("product_id").agg(
        total_demand_units=("demand_units", "sum"),
        avg_demand_per_period=("demand_units", "mean"),
        avg_inventory_on_hand=("inventory_on_hand", "mean"),
        avg_lead_time_days=("supplier_lead_time_days", "mean"),
        avg_unit_cost=("unit_cost", "mean"),
        observations=("date", "count")
    ).reset_index()

    # Illustrative reorder point = average demand per period * average lead time in days / 3
    # Dataset observations are spaced roughly 3 days apart; this is a simplified planning estimate.
    product_summary["estimated_daily_demand"] = product_summary["avg_demand_per_period"] / 3
    product_summary["estimated_reorder_point_units"] = (
        product_summary["estimated_daily_demand"] * product_summary["avg_lead_time_days"]
    ).round(0).astype(int)
    product_summary["inventory_status"] = product_summary.apply(
        lambda r: "Review stock" if r["avg_inventory_on_hand"] < r["estimated_reorder_point_units"]
        else "Stock above estimated reorder point", axis=1
    )
    product_summary.to_csv(OUT / "product_inventory_summary.csv", index=False)

    supplier_summary = df.groupby("supplier").agg(
        total_demand_units=("demand_units", "sum"),
        avg_lead_time_days=("supplier_lead_time_days", "mean"),
        avg_inventory_on_hand=("inventory_on_hand", "mean"),
        average_unit_cost=("unit_cost", "mean")
    ).reset_index()
    supplier_summary.to_csv(OUT / "supplier_summary.csv", index=False)

    # SQL analysis using SQLite
    with sqlite3.connect(OUT / "inventory_analytics.db") as conn:
        df.to_sql("inventory_records", conn, if_exists="replace", index=False)
        sql_summary = pd.read_sql_query("""
            SELECT supplier,
                   COUNT(*) AS records,
                   SUM(demand_units) AS total_demand_units,
                   ROUND(AVG(supplier_lead_time_days), 2) AS avg_lead_time_days,
                   ROUND(AVG(inventory_on_hand), 2) AS avg_inventory_on_hand
            FROM inventory_records
            GROUP BY supplier
            ORDER BY total_demand_units DESC;
        """, conn)
    sql_summary.to_csv(OUT / "sql_supplier_summary.csv", index=False)

    # Charts
    plt.figure(figsize=(9, 5))
    ordered = product_summary.sort_values("total_demand_units", ascending=False)
    plt.bar(ordered["product_id"], ordered["total_demand_units"])
    plt.title("Total Demand by Product")
    plt.xlabel("Product ID")
    plt.ylabel("Demand units")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUT / "demand_by_product.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(product_summary["avg_lead_time_days"],
                product_summary["estimated_reorder_point_units"])
    plt.title("Supplier Lead Time vs Estimated Reorder Point")
    plt.xlabel("Average lead time (days)")
    plt.ylabel("Estimated reorder point (units)")
    plt.tight_layout()
    plt.savefig(OUT / "lead_time_vs_reorder_point.png", dpi=160)
    plt.close()

    print("\\nSUPPLY CHAIN & INVENTORY ANALYTICS")
    print("=" * 42)
    print(f"Records analyzed: {len(df)}")
    print(f"Products analyzed: {df['product_id'].nunique()}")
    print(f"Suppliers analyzed: {df['supplier'].nunique()}")
    print("\\nTop products by total demand:")
    print(ordered[["product_id", "total_demand_units"]].head(5).to_string(index=False))
    print(f"\\nSummary tables and charts saved to: {OUT}")
    print("Reorder points are simplified estimates; validate assumptions before real operational use.")

if __name__ == "__main__":
    main()
