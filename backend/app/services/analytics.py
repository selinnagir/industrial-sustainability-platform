import pandas as pd

def apply_filters(df: pd.DataFrame, facility: str | None = None, sector: str | None = None) -> pd.DataFrame:
    filtered = df.copy()

    if facility and facility != "All":
        filtered = filtered[filtered["facility_name"] == facility]

    if sector and sector != "All":
        filtered = filtered[filtered["sector"] == sector]

    return filtered

def build_summary(df: pd.DataFrame) -> dict:
    total_consumption = float(df["energy_kwh"].sum()) if not df.empty else 0.0
    total_facilities = int(df["facility_name"].nunique()) if not df.empty else 0

    if not df.empty:
        monthly = (
            df.groupby("year_month", as_index=False)["energy_kwh"]
            .sum()
            .sort_values("year_month")
        )

        latest_value = monthly["energy_kwh"].iloc[-1]
        previous_value = monthly["energy_kwh"].iloc[-2] if len(monthly) > 1 else latest_value

        change_pct = 0.0 if previous_value == 0 else float(((latest_value - previous_value) / previous_value) * 100)
    else:
        change_pct = 0.0

    return {
        "total_consumption_kwh": round(total_consumption, 2),
        "total_facilities": total_facilities,
        "monthly_change_pct": round(change_pct, 2),
    }

def build_trend(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []

    trend = (
        df.groupby("year_month", as_index=False)["energy_kwh"]
        .sum()
        .sort_values("year_month")
    )

    return [
        {
            "period": row["year_month"],
            "energy_kwh": round(float(row["energy_kwh"]), 2),
        }
        for _, row in trend.iterrows()
    ]

def build_filter_options(df: pd.DataFrame) -> dict:
    return {
        "facilities": sorted(df["facility_name"].dropna().unique().tolist()),
        "sectors": sorted(df["sector"].dropna().unique().tolist()),
    }
