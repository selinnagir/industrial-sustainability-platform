def build_scenario_simulation(company_payload: dict, energy_reduction_pct: float = 0.0, emissions_reduction_pct: float = 0.0) -> dict:
    summary = company_payload.get("summary", {})
    sustainability = company_payload.get("sustainability_metrics", {})
    forecast = company_payload.get("forecast_analysis", {})

    baseline_energy = float(summary.get("total_energy_mwh", 0) or 0)
    baseline_emissions = float(summary.get("total_direct_emissions_tons", 0) or 0)
    baseline_carbon_intensity = sustainability.get("carbon_intensity_ton_per_mwh")

    energy_factor = max(0.0, 1 - (float(energy_reduction_pct) / 100.0))
    emissions_factor = max(0.0, 1 - (float(emissions_reduction_pct) / 100.0))

    simulated_energy = round(baseline_energy * energy_factor, 3)
    simulated_emissions = round(baseline_emissions * emissions_factor, 3)

    simulated_carbon_intensity = None
    if simulated_energy > 0:
        simulated_carbon_intensity = round(simulated_emissions / simulated_energy, 6)

    energy_saved = round(baseline_energy - simulated_energy, 3)
    emissions_saved = round(baseline_emissions - simulated_emissions, 3)

    next_period = forecast.get("next_period")
    forecast_energy = forecast.get("forecast_energy_mwh")
    forecast_emissions = forecast.get("forecast_direct_emissions_tons")

    simulated_forecast_energy = None
    simulated_forecast_emissions = None
    if forecast_energy is not None:
        simulated_forecast_energy = round(float(forecast_energy) * energy_factor, 3)
    if forecast_emissions is not None:
        simulated_forecast_emissions = round(float(forecast_emissions) * emissions_factor, 3)

    commentary = []
    if energy_saved > 0:
        commentary.append(f"Enerji senaryosu uygulanırsa toplam tüketimde {energy_saved} MWh düşüş beklenir.")
    if emissions_saved > 0:
        commentary.append(f"Emisyon senaryosu uygulanırsa toplam direct emissions {emissions_saved} ton azalabilir.")

    if simulated_carbon_intensity is not None and baseline_carbon_intensity is not None:
        if simulated_carbon_intensity < baseline_carbon_intensity:
            commentary.append("Karbon yoğunluğu senaryo sonrası iyileşiyor.")
        elif simulated_carbon_intensity > baseline_carbon_intensity:
            commentary.append("Karbon yoğunluğu beklenenden kötüleşiyor; enerji ve emisyon azaltımı dengeli seçilmeli.")
        else:
            commentary.append("Karbon yoğunluğu değişmiyor.")

    recommendations = []
    if energy_reduction_pct >= 10:
        recommendations.append("Enerji azaltımı için proses optimizasyonu ve ekipman verimliliği aksiyonları önceliklendirilmeli.")
    if emissions_reduction_pct >= 10:
        recommendations.append("Emisyon azaltımı için yakıt karışımı, elektrikleşme ve operasyon iyileştirmeleri değerlendirilmeli.")
    if energy_reduction_pct >= 20 or emissions_reduction_pct >= 20:
        recommendations.append("Bu senaryo agresif olabilir; operasyonel uygulanabilirlik ve yatırım etkisi ayrıca doğrulanmalı.")
    if not recommendations:
        recommendations.append("Daha anlamlı çıktı için enerji veya emisyon azaltım yüzdesini artırarak senaryoyu tekrar dene.")

    return {
        "inputs": {
            "energy_reduction_pct": round(float(energy_reduction_pct), 3),
            "emissions_reduction_pct": round(float(emissions_reduction_pct), 3),
        },
        "baseline": {
            "total_energy_mwh": round(baseline_energy, 3),
            "total_direct_emissions_tons": round(baseline_emissions, 3),
            "carbon_intensity_ton_per_mwh": baseline_carbon_intensity,
        },
        "simulation": {
            "total_energy_mwh": simulated_energy,
            "total_direct_emissions_tons": simulated_emissions,
            "carbon_intensity_ton_per_mwh": simulated_carbon_intensity,
            "energy_saved_mwh": energy_saved,
            "emissions_saved_tons": emissions_saved,
        },
        "forecast_effect": {
            "next_period": next_period,
            "baseline_forecast_energy_mwh": forecast_energy,
            "baseline_forecast_direct_emissions_tons": forecast_emissions,
            "simulated_forecast_energy_mwh": simulated_forecast_energy,
            "simulated_forecast_direct_emissions_tons": simulated_forecast_emissions,
        },
        "commentary": commentary,
        "recommendations": recommendations,
    }
