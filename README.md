@'
# Industrial Sustainability Platform

An industrial sustainability analytics platform for monitoring **energy consumption**, **carbon intensity**, **benchmark performance**, **anomalies**, **forecasting**, and **automated PDF reporting**.

This project was developed as a decision-support system for industrial facilities to help analyze sustainability performance, identify inefficiencies, compare against reference benchmarks, and generate actionable reports.

---

## Features

- Data loading and preprocessing
- Missing value checks
- Type conversion and data cleaning
- KPI cards for energy and emissions
- Carbon intensity calculation
- State-based benchmark analysis
- Sector benchmark analysis
- Sustainability score
- Anomaly detection
- Forecasting
- AI-powered chat / question answering
- Automatic PDF report generation

---

## Project Goals

The main goal of this project is to transform raw industrial energy and emissions data into a **decision-support platform**.

Instead of only displaying data, the platform helps users:

- understand their current sustainability performance,
- compare against reference values,
- detect unusual behavior,
- estimate future performance,
- and export findings as structured PDF reports.

---

## Screens / Modules

### 1. Company Dashboard
Displays the main sustainability indicators for a selected facility and/or state.

Includes:
- Company Carbon Intensity
- Selected State
- State Status
- Sector Column Detection
- eGRID State Benchmark
- GHGRP State Reference
- Sector Benchmark

### 2. Sustainability Analysis
Calculates sustainability-related metrics and scoring outputs.

Includes:
- carbon intensity
- sustainability score
- strengths / weaknesses
- high-level evaluation

### 3. Smart Modules
Advanced analytics components for better decision support.

Includes:
- anomaly detection
- forecasting
- AI chat
- benchmark commentary
- explainability-oriented outputs

### 4. Reporting
Generates downloadable PDF reports that summarize the selected company/facility analysis.

---

## Tech Stack

### Backend
- Python
- FastAPI
- Pandas
- NumPy
- ReportLab

### Frontend
- React
- TypeScript
- Tailwind CSS
- Vite

### Data / Analytics
- KPI analysis
- benchmark comparison
- anomaly detection
- forecasting
- sustainability scoring

---

## Repository Structure

```text
industrial-sustainability-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── ...
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── ...
│   └── ...
│
└── README.md
