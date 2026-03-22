def build_sustainability_score(company_payload: dict) -> dict:
    summary = company_payload.get("summary", {})
    sustainability = company_payload.get("sustainability_metrics", {})
    historical = company_payload.get("historical_analysis", {})
    anomaly = company_payload.get("anomaly_analysis", {})
    forecast = company_payload.get("forecast_analysis", {})

    score = 100.0
    strengths = []
    weaknesses = []
    drivers = []

    total_energy = float(summary.get("total_energy_mwh", 0) or 0)
    total_emissions = float(summary.get("total_direct_emissions_tons", 0) or 0)

    carbon_intensity = sustainability.get("carbon_intensity_ton_per_mwh")
    water_intensity = sustainability.get("water_intensity_per_mwh")
    waste_intensity = sustainability.get("waste_intensity_per_mwh")

    emissions_change = historical.get("emissions_change_percent")
    anomaly_count = int(anomaly.get("total_anomalies", 0) or 0)

    forecast_emissions = forecast.get("forecast_direct_emissions_tons")
    period_count = int(historical.get("period_count", 0) or 0)

    if carbon_intensity is None:
        score -= 8
        weaknesses.append("Karbon yoğunluğu hesaplanamadı.")
        drivers.append("Karbon yoğunluğu verisi eksik.")
    elif carbon_intensity > 0.6:
        score -= 22
        weaknesses.append("Karbon yoğunluğu yüksek.")
        drivers.append("Yüksek karbon yoğunluğu skoru düşürdü.")
    elif carbon_intensity > 0.35:
        score -= 14
        weaknesses.append("Karbon yoğunluğu orta-yüksek seviyede.")
        drivers.append("Karbon yoğunluğu iyileştirme gerektiriyor.")
    elif carbon_intensity > 0.2:
        score -= 6
        strengths.append("Karbon yoğunluğu kabul edilebilir seviyede.")
    else:
        strengths.append("Karbon yoğunluğu güçlü seviyede.")

    if water_intensity is not None:
        if water_intensity > 20:
            score -= 10
            weaknesses.append("Su yoğunluğu yüksek.")
            drivers.append("Su yoğunluğu skoru düşürdü.")
        elif water_intensity > 10:
            score -= 5
            weaknesses.append("Su yoğunluğu orta seviyede.")
        else:
            strengths.append("Su yoğunluğu kontrollü.")

    if waste_intensity is not None:
        if waste_intensity > 0.05:
            score -= 10
            weaknesses.append("Atık yoğunluğu yüksek.")
            drivers.append("Atık yoğunluğu skoru düşürdü.")
        elif waste_intensity > 0.02:
            score -= 5
            weaknesses.append("Atık yoğunluğu orta seviyede.")
        else:
            strengths.append("Atık yoğunluğu kontrollü.")

    if emissions_change is not None:
        if emissions_change > 20:
            score -= 18
            weaknesses.append("Emisyon trendi güçlü artış gösteriyor.")
            drivers.append("Emisyon artışı skoru düşürdü.")
        elif emissions_change > 10:
            score -= 12
            weaknesses.append("Emisyon trendi artıyor.")
            drivers.append("Yukarı yönlü emisyon trendi mevcut.")
        elif emissions_change > 3:
            score -= 6
            weaknesses.append("Emisyon trendi hafif yukarı yönlü.")
        elif emissions_change < -3:
            score += 3
            strengths.append("Emisyon trendi düşüş gösteriyor.")

    if anomaly_count >= 3:
        score -= 18
        weaknesses.append("Birden fazla anomali kaydı var.")
        drivers.append("Anomali sayısı yüksek.")
    elif anomaly_count >= 1:
        score -= 10
        weaknesses.append("Anomali tespiti mevcut.")
        drivers.append("Anomali varlığı skoru düşürdü.")
    else:
        strengths.append("Belirgin anomali tespit edilmedi.")

    if forecast_emissions is not None and period_count > 0:
        avg_emissions_per_period = total_emissions / period_count if period_count > 0 else None
        if avg_emissions_per_period:
            if float(forecast_emissions) > avg_emissions_per_period * 1.10:
                score -= 8
                weaknesses.append("Gelecek dönem emisyon tahmini olumsuz.")
                drivers.append("Tahmin edilen emisyon artışı skoru düşürdü.")
            elif float(forecast_emissions) < avg_emissions_per_period * 0.95:
                score += 2
                strengths.append("Gelecek dönem emisyon tahmini olumlu.")

    if total_energy == 0 and total_emissions == 0:
        score = 0
        weaknesses.append("Skor üretmek için yeterli operasyonel veri yok.")
        drivers.append("Enerji ve emisyon verisi bulunamadı.")

    score = max(0, min(round(score, 1), 100))

    if score >= 85:
        grade = "A"
        label = "Güçlü"
    elif score >= 70:
        grade = "B"
        label = "İyi"
    elif score >= 55:
        grade = "C"
        label = "Geliştirilmeli"
    else:
        grade = "D"
        label = "Kritik"

    if not strengths:
        strengths.append("Temel veri akışı mevcut.")
    if not weaknesses:
        weaknesses.append("Belirgin zayıf nokta görünmüyor.")
    if not drivers:
        drivers.append("Skor büyük ölçüde dengeli performanstan oluştu.")

    return {
        "score": score,
        "grade": grade,
        "label": label,
        "strengths": strengths[:5],
        "weaknesses": weaknesses[:5],
        "drivers": drivers[:5],
    }
