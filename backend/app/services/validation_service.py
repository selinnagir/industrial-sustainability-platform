import pandas as pd

COLUMN_PATTERNS = {
    "company_name": ["company", "organization", "firm"],
    "facility_name": ["facility", "plant", "site", "facility_name", "plant_name"],
    "state_or_region": ["state", "region", "province", "country_code"],
    "date": ["date", "month", "year", "timestamp", "period"],
    "energy_mwh": ["energy", "mwh", "gwh", "kwh", "consumption"],
    "electricity_mwh": ["electricity", "power", "grid"],
    "fuel_type": ["fuel", "fuel_type", "fueltype"],
    "direct_emissions_tons": ["emission", "co2", "co2e", "ghg", "carbon"],
    "water_use": ["water"],
    "waste_tons": ["waste"],
    "production_amount": ["production", "output", "throughput"],
}

def suggest_column_mapping(columns: list[str]) -> dict:
    suggested = {}
    lowered = {col: str(col).strip().lower() for col in columns}

    for target, patterns in COLUMN_PATTERNS.items():
        best_match = None
        for original, low in lowered.items():
            if any(pattern in low for pattern in patterns):
                best_match = original
                break
        suggested[target] = best_match

    return suggested

def validate_dataset(df: pd.DataFrame, mapping: dict) -> dict:
    issues = []
    warnings = []

    required_identity = ["facility_name", "date"]
    for field in required_identity:
        if not mapping.get(field):
            issues.append(f"Zorunlu alan için eşleşme bulunamadı: {field}")

    metric_candidates = ["energy_mwh", "electricity_mwh", "direct_emissions_tons"]
    detected_metrics = [field for field in metric_candidates if mapping.get(field)]

    if not detected_metrics:
        issues.append("En az bir metrik alanı gerekli: energy_mwh / electricity_mwh / direct_emissions_tons")

    if df.empty:
        issues.append("Dosya boş görünüyor.")

    if len(df.columns) < 2:
        issues.append("Kolon sayısı çok az. Dosya tablo formatında olmayabilir.")

    if df.duplicated().sum() > 0:
        warnings.append(f"Tekrarlı satır tespit edildi: {int(df.duplicated().sum())}")

    null_ratio = float(df.isna().mean().mean()) if not df.empty else 0.0
    if null_ratio > 0.3:
        warnings.append(f"Veride yüksek boşluk oranı var: %{round(null_ratio * 100, 1)}")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "detected_metrics": detected_metrics,
    }
