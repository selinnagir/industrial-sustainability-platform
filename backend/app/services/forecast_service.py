import pandas as pd

def _safe_forecast_next(values: list[float]) -> float | None:
    clean = [float(v) for v in values if pd.notna(v)]
    if not clean:
        return None
    if len(clean) == 1:
        return round(clean[-1], 3)

    diffs = []
    for i in range(1, len(clean)):
        diffs.append(clean[i] - clean[i - 1])

    avg_diff = sum(diffs) / len(diffs) if diffs else 0
    forecast_value = clean[-1] + avg_diff
    return round(max(forecast_value, 0), 3)

def build_forecast_analysis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "next_period": None,
            "forecast_energy_mwh": None,
            "forecast_direct_emissions_tons": None,
            "energy_forecast_comment": "Tahmin için yeterli veri yok.",
            "emissions_forecast_comment": "Tahmin için yeterli veri yok.",
            "confidence": "low",
        }

    trend_df = (
        df.assign(period=df["date"].dt.strftime("%Y-%m"))
        .groupby("period", as_index=False)[["energy_mwh", "direct_emissions_tons"]]
        .sum()
        .sort_values("period")
    )

    if trend_df.empty:
        return {
            "next_period": None,
            "forecast_energy_mwh": None,
            "forecast_direct_emissions_tons": None,
            "energy_forecast_comment": "Tahmin için yeterli veri yok.",
            "emissions_forecast_comment": "Tahmin için yeterli veri yok.",
            "confidence": "low",
        }

    last_period_str = trend_df.iloc[-1]["period"]
    last_period_dt = pd.to_datetime(last_period_str + "-01", errors="coerce")
    next_period = None
    if pd.notna(last_period_dt):
        next_period = (last_period_dt + pd.DateOffset(months=1)).strftime("%Y-%m")

    energy_values = trend_df["energy_mwh"].fillna(0).tolist()
    emissions_values = trend_df["direct_emissions_tons"].fillna(0).tolist()

    forecast_energy = _safe_forecast_next(energy_values)
    forecast_emissions = _safe_forecast_next(emissions_values)

    confidence = "low"
    if len(trend_df) >= 4:
        confidence = "medium"
    if len(trend_df) >= 8:
        confidence = "high"

    last_energy = float(energy_values[-1]) if energy_values else 0
    last_emissions = float(emissions_values[-1]) if emissions_values else 0

    if forecast_energy is None:
        energy_comment = "Enerji tahmini üretilemedi."
    elif forecast_energy > last_energy:
        energy_comment = "Enerji tüketiminde gelecek dönemde artış beklentisi var."
    elif forecast_energy < last_energy:
        energy_comment = "Enerji tüketiminde gelecek dönemde düşüş beklentisi var."
    else:
        energy_comment = "Enerji tüketimi gelecek dönemde benzer seviyede kalabilir."

    if forecast_emissions is None:
        emissions_comment = "Emisyon tahmini üretilemedi."
    elif forecast_emissions > last_emissions:
        emissions_comment = "Direct emissions tarafında gelecek dönemde artış riski var."
    elif forecast_emissions < last_emissions:
        emissions_comment = "Direct emissions tarafında gelecek dönemde düşüş beklentisi var."
    else:
        emissions_comment = "Direct emissions gelecek dönemde benzer seviyede kalabilir."

    return {
        "next_period": next_period,
        "forecast_energy_mwh": forecast_energy,
        "forecast_direct_emissions_tons": forecast_emissions,
        "energy_forecast_comment": energy_comment,
        "emissions_forecast_comment": emissions_comment,
        "confidence": confidence,
    }
