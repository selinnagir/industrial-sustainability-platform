def build_risk_assessment(company_payload: dict) -> dict:
    sustainability = company_payload.get("sustainability_metrics", {})
    historical = company_payload.get("historical_analysis", {})
    anomaly = company_payload.get("anomaly_analysis", {})

    energy_change = historical.get("energy_change_percent")
    emissions_change = historical.get("emissions_change_percent")
    anomaly_count = anomaly.get("total_anomalies", 0)
    carbon_intensity = sustainability.get("carbon_intensity_ton_per_mwh")

    score = 0.0
    drivers = []

    if emissions_change is not None:
        if emissions_change > 20:
            score += 30
            drivers.append("Direct emissions güçlü artış eğiliminde.")
        elif emissions_change > 10:
            score += 20
            drivers.append("Direct emissions artış gösteriyor.")
        elif emissions_change > 3:
            score += 10
            drivers.append("Direct emissions hafif yukarı yönlü.")

    if energy_change is not None:
        if energy_change > 20:
            score += 25
            drivers.append("Enerji tüketimi güçlü artış eğiliminde.")
        elif energy_change > 10:
            score += 18
            drivers.append("Enerji tüketimi artış gösteriyor.")
        elif energy_change > 3:
            score += 10
            drivers.append("Enerji tüketimi hafif yukarı yönlü.")

    if anomaly_count >= 3:
        score += 25
        drivers.append("Birden fazla anomali kaydı tespit edildi.")
    elif anomaly_count >= 1:
        score += 15
        drivers.append("Anomali tespiti mevcut.")

    if carbon_intensity is not None:
        if carbon_intensity > 0.6:
            score += 20
            drivers.append("Karbon yoğunluğu yüksek seviyede.")
        elif carbon_intensity > 0.35:
            score += 10
            drivers.append("Karbon yoğunluğu orta-yüksek seviyede.")

    score = round(min(score, 100), 1)

    if score >= 70:
        level = "Yüksek"
    elif score >= 40:
        level = "Orta"
    else:
        level = "Düşük"

    if drivers:
        reason_text = " ".join(drivers)
    else:
        reason_text = "Şu an belirgin bir risk yükseltici sinyal görünmüyor."

    return {
        "score": score,
        "level": level,
        "drivers": drivers,
        "reason_text": reason_text,
    }


def build_company_ai_insights(company_payload: dict) -> dict:
    summary = company_payload.get("summary", {})
    sustainability = company_payload.get("sustainability_metrics", {})
    sustainability_score = company_payload.get("sustainability_score", {})
    historical = company_payload.get("historical_analysis", {})
    anomaly = company_payload.get("anomaly_analysis", {})
    top_facilities = company_payload.get("top_facilities", [])
    forecast = company_payload.get("forecast_analysis", {})

    total_energy = summary.get("total_energy_mwh", 0)
    total_emissions = summary.get("total_direct_emissions_tons", 0)
    facility_count = summary.get("total_facilities", 0)

    energy_change = historical.get("energy_change_percent")
    emissions_change = historical.get("emissions_change_percent")
    energy_label = historical.get("energy_trend_label", "yetersiz veri")
    emissions_label = historical.get("emissions_trend_label", "yetersiz veri")

    carbon_intensity = sustainability.get("carbon_intensity_ton_per_mwh")
    anomaly_count = anomaly.get("total_anomalies", 0)
    risky_facilities = anomaly.get("risky_facilities", [])

    risk_assessment = build_risk_assessment(company_payload)

    if anomaly_count == 0:
        anomaly_comment = "Mevcut veri setinde belirgin bir anomali tespit edilmedi."
    else:
        anomaly_comment = f"Toplam {anomaly_count} anomali kaydı tespit edildi. Riskli tesisler önceliklendirilmeli."

    if emissions_label == "artıyor":
        emissions_comment = "Direct emissions trendi yukarı yönlü. Emisyon azaltım aksiyonları önceliklendirilmeli."
    elif emissions_label == "azalıyor":
        emissions_comment = "Direct emissions tarafında olumlu bir düşüş eğilimi var."
    else:
        emissions_comment = "Direct emissions tarafında belirgin bir yön değişimi görünmüyor."

    if energy_label == "artıyor":
        energy_comment = "Enerji tüketimi artış eğiliminde. Verimlilik ve operasyon planlaması gözden geçirilmeli."
    elif energy_label == "azalıyor":
        energy_comment = "Enerji tüketiminde düşüş gözleniyor. Bu iyileşmenin nedeni korunmalı."
    else:
        energy_comment = "Enerji tüketimi genel olarak stabil görünüyor."

    if carbon_intensity is None:
        carbon_comment = "Karbon yoğunluğu için yeterli veri bulunamadı."
    elif carbon_intensity > 0.6:
        carbon_comment = "Karbon yoğunluğu yüksek seviyede. Yakıt yapısı ve verimlilik tarafı incelenmeli."
    elif carbon_intensity > 0.35:
        carbon_comment = "Karbon yoğunluğu orta seviyede. İyileştirme alanları mevcut."
    else:
        carbon_comment = "Karbon yoğunluğu görece kontrollü görünüyor."

    top_facility_comment = None
    if top_facilities:
        top = top_facilities[0]
        top_facility_comment = (
            f"En yüksek enerji kullanan tesis {top.get('facility_name')} "
            f"({top.get('state_or_region')}) ve toplam {top.get('energy_mwh')} MWh."
        )

    forecast_comment = (
        f"Gelecek dönem için tahmini enerji {forecast.get('forecast_energy_mwh')} MWh ve "
        f"tahmini direct emissions {forecast.get('forecast_direct_emissions_tons')} ton. "
        f"{forecast.get('energy_forecast_comment', '')} {forecast.get('emissions_forecast_comment', '')}"
    )

    score_comment = (
        f"Sürdürülebilirlik skoru {sustainability_score.get('score')}/100, "
        f"grade {sustainability_score.get('grade')} ve durum {sustainability_score.get('label')}."
    )

    recommendations = []

    if energy_label == "artıyor":
        recommendations.append("Yüksek tüketim dönemleri için enerji verimliliği ve proses optimizasyonu analizi başlat.")
    if emissions_label == "artıyor":
        recommendations.append("Emisyon artışı görülen tesislerde yakıt, proses ve operasyon kaynaklı nedenleri incele.")
    if anomaly_count > 0:
        recommendations.append("Anomali görülen kayıtları operasyonel olaylar, bakım ve veri kalitesi açısından doğrula.")
    if carbon_intensity is not None and carbon_intensity > 0.35:
        recommendations.append("Karbon yoğunluğunu azaltmak için elektrik/fuel karışımı ve ekipman verimliliği gözden geçirilmeli.")
    if risk_assessment["level"] == "Yüksek":
        recommendations.append("Kısa vadede yüksek riskli tesisler için aksiyon planı ve haftalık izleme mekanizması oluştur.")
    if forecast.get("forecast_energy_mwh") is not None and forecast.get("forecast_energy_mwh", 0) > total_energy:
        recommendations.append("Tahmin edilen enerji artışı için erken önlem planı hazırlanmalı.")
    if sustainability_score.get("grade") in ["C", "D"]:
        recommendations.append("Sürdürülebilirlik skorunu yükseltmek için karbon yoğunluğu, anomali ve emisyon trendi birlikte iyileştirilmeli.")
    if not recommendations:
        recommendations.append("Mevcut performansı korumak için periyodik trend ve veri kalite izleme sürdürülmeli.")

    executive_summary_parts = [
        f"Şirket verisinde toplam {total_energy} MWh enerji ve {total_emissions} ton direct emissions raporlandı.",
        f"Analiz {facility_count} tesis üzerinden yapıldı.",
        f"Risk seviyesi {risk_assessment['level']} ve skor {risk_assessment['score']}/100.",
        score_comment,
        energy_comment,
        emissions_comment,
        carbon_comment,
        anomaly_comment,
        forecast_comment,
    ]

    if top_facility_comment:
        executive_summary_parts.append(top_facility_comment)

    return {
        "overview": {
            "total_energy_mwh": total_energy,
            "total_direct_emissions_tons": total_emissions,
            "facility_count": facility_count,
            "risk_level": risk_assessment["level"],
            "risk_score": risk_assessment["score"],
            "sustainability_score": sustainability_score.get("score"),
            "sustainability_grade": sustainability_score.get("grade"),
        },
        "risk_assessment": risk_assessment,
        "historical_commentary": {
            "energy_change_percent": energy_change,
            "emissions_change_percent": emissions_change,
            "energy_comment": energy_comment,
            "emissions_comment": emissions_comment,
        },
        "anomaly_commentary": {
            "total_anomalies": anomaly_count,
            "comment": anomaly_comment,
            "risky_facilities": risky_facilities,
        },
        "sustainability_commentary": {
            "carbon_intensity_ton_per_mwh": carbon_intensity,
            "comment": carbon_comment,
        },
        "sustainability_score_commentary": sustainability_score,
        "forecast_commentary": {
            "next_period": forecast.get("next_period"),
            "forecast_energy_mwh": forecast.get("forecast_energy_mwh"),
            "forecast_direct_emissions_tons": forecast.get("forecast_direct_emissions_tons"),
            "confidence": forecast.get("confidence"),
            "energy_forecast_comment": forecast.get("energy_forecast_comment"),
            "emissions_forecast_comment": forecast.get("emissions_forecast_comment"),
        },
        "recommendations": recommendations,
        "executive_summary": " ".join(executive_summary_parts),
    }


def answer_company_question(question: str, company_payload: dict) -> dict:
    q = (question or "").strip().lower()
    insights = build_company_ai_insights(company_payload)

    top_facilities = company_payload.get("top_facilities", [])
    summary = company_payload.get("summary", {})
    historical = insights.get("historical_commentary", {})
    anomaly = insights.get("anomaly_commentary", {})
    sustainability = insights.get("sustainability_commentary", {})
    sustainability_score = insights.get("sustainability_score_commentary", {})
    risk = insights.get("risk_assessment", {})
    forecast = insights.get("forecast_commentary", {})
    recommendations = insights.get("recommendations", [])

    if not q:
        return {
            "question_type": "empty",
            "answer": "Lütfen bir soru yaz. Örnek: Sürdürülebilirlik skorum kaç, risk seviyem neden yüksek, gelecek ay ne bekleniyor?",
        }

    if any(word in q for word in ["sürdürülebilirlik skoru", "sustainability", "score", "skor"]):
        strengths = ", ".join(sustainability_score.get("strengths", [])[:2])
        weaknesses = ", ".join(sustainability_score.get("weaknesses", [])[:2])
        return {
            "question_type": "sustainability_score",
            "answer": (
                f"Sürdürülebilirlik skorun {sustainability_score.get('score')}/100. "
                f"Grade {sustainability_score.get('grade')} ve durum {sustainability_score.get('label')}. "
                f"Güçlü yönler: {strengths if strengths else 'yok'}. "
                f"Geliştirme alanları: {weaknesses if weaknesses else 'yok'}."
            ),
        }

    if (
        any(word in q for word in ["tahmin", "gelecek", "sonraki", "önümüzdeki", "forecast"])
        and any(word in q for word in ["öner", "aksiyon", "önlem", "öncelik", "ne yap", "iyileştir"])
    ):
        recommendation_text = "\n".join([f"{idx+1}. {item}" for idx, item in enumerate(recommendations[:3])])

        return {
            "question_type": "forecast_recommendation",
            "answer": (
                f"{forecast.get('next_period')} dönemi için tahmini enerji {forecast.get('forecast_energy_mwh')} MWh "
                f"ve tahmini direct emissions {forecast.get('forecast_direct_emissions_tons')} ton. "
                f"{forecast.get('energy_forecast_comment', '')} {forecast.get('emissions_forecast_comment', '')} "
                f"Güven seviyesi: {forecast.get('confidence')}.\n\n"
                f"Tahmine göre öncelikli aksiyonlar:\n{recommendation_text}"
            ),
        }

    if any(word in q for word in ["karşılaştır", "kıyas", "benchmark", "referans"]):
        return {
            "question_type": "comparison",
            "answer": "Bu sürümde chatbox öncelikle yüklenen şirket verin üzerinden analiz yapıyor. Referans dashboard ile otomatik kıyas sonraki adımda geliştirilebilir.",
        }

    if any(word in q for word in ["risk", "riskli"]):
        drivers = risk.get("drivers", [])
        driver_text = " ".join(drivers) if drivers else risk.get("reason_text", "")
        return {
            "question_type": "risk",
            "answer": f"Risk skorun {risk.get('score')}/100 ve seviye {risk.get('level')}. {driver_text if driver_text else risk.get('reason_text')}",
        }

    if any(word in q for word in ["anomali", "anomaly", "olağandışı"]):
        risky_facilities = anomaly.get("risky_facilities", [])
        if risky_facilities:
            top_risky = risky_facilities[0]
            return {
                "question_type": "anomaly",
                "answer": (
                    f"Toplam {anomaly.get('total_anomalies')} anomali kaydı var. "
                    f"En riskli görünen tesis {top_risky.get('facility_name')} ({top_risky.get('state_or_region')}) "
                    f"ve anomaly count {top_risky.get('anomaly_count')}."
                ),
            }
        return {
            "question_type": "anomaly",
            "answer": anomaly.get("comment", "Şu an anomali tespit edilmedi."),
        }

    if any(word in q for word in ["öner", "aksiyon", "önlem", "öncelik", "ne yap", "iyileştir"]):
        return {
            "question_type": "recommendation",
            "answer": "\n".join([f"{idx+1}. {item}" for idx, item in enumerate(recommendations)]),
        }

    if any(word in q for word in ["tahmin", "gelecek", "sonraki", "önümüzdeki", "forecast"]):
        return {
            "question_type": "forecast",
            "answer": (
                f"{forecast.get('next_period')} dönemi için tahmini enerji {forecast.get('forecast_energy_mwh')} MWh "
                f"ve tahmini direct emissions {forecast.get('forecast_direct_emissions_tons')} ton. "
                f"{forecast.get('energy_forecast_comment', '')} {forecast.get('emissions_forecast_comment', '')} "
                f"Güven seviyesi: {forecast.get('confidence')}."
            ),
        }

    if any(word in q for word in ["enerji", "tüketim", "energy"]):
        answer = [
            f"Toplam enerji tüketimi {summary.get('total_energy_mwh')} MWh.",
            historical.get("energy_comment", ""),
            forecast.get("energy_forecast_comment", ""),
        ]
        if top_facilities:
            top = top_facilities[0]
            answer.append(f"En yüksek enerji kullanan tesis {top.get('facility_name')} ve değeri {top.get('energy_mwh')} MWh.")
        return {
            "question_type": "energy",
            "answer": " ".join([x for x in answer if x]),
        }

    if any(word in q for word in ["emisyon", "co2", "karbon"]):
        return {
            "question_type": "emissions",
            "answer": (
                f"Toplam direct emissions {summary.get('total_direct_emissions_tons')} ton. "
                f"{historical.get('emissions_comment', '')} "
                f"{sustainability.get('comment', '')} "
                f"{forecast.get('emissions_forecast_comment', '')}"
            ),
        }

    if any(word in q for word in ["hangi tesis", "tesis", "problemli"]):
        if top_facilities:
            top = top_facilities[0]
            return {
                "question_type": "facility",
                "answer": (
                    f"En yüksek enerji kullanan tesis {top.get('facility_name')} ({top.get('state_or_region')}). "
                    f"Toplam enerji {top.get('energy_mwh')} MWh ve direct emissions {top.get('direct_emissions_tons')} ton."
                ),
            }
        return {
            "question_type": "facility",
            "answer": "Tesis bazlı yorum için yeterli veri görünmüyor.",
        }

    if any(word in q for word in ["özet", "summary", "genel durum"]):
        return {
            "question_type": "summary",
            "answer": insights.get("executive_summary", "Genel özet üretilemedi."),
        }

    if any(word in q for word in ["geçmiş", "trend", "artıyor", "azalıyor"]):
        return {
            "question_type": "historical",
            "answer": f"{historical.get('energy_comment', '')} {historical.get('emissions_comment', '')}",
        }

    return {
        "question_type": "general",
        "answer": "Bu soruyu şirket verine göre yorumlamaya çalıştım ama daha net bir soru daha iyi olur. Şunları sorabilirsin: sürdürülebilirlik skorum kaç, risk seviyem neden yüksek, gelecek ay ne bekleniyor, ne önerirsin?",
    }
