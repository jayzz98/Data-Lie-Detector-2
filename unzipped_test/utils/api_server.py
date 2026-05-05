"""
Data Lie Detector — REST API Server

Run with:
    uvicorn utils.api_server:app --reload --port 8000

Endpoints:
    POST /analyze     — Upload CSV, get full analysis
    GET  /health      — Health check
"""

import io
import json

try:
    from fastapi import FastAPI, UploadFile, File, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

import pandas as pd

from utils.loader import load_file
from utils.profiler import profile_data
from utils.anomaly import detect_anomalies
from utils.trust import calculate_trust
from utils.explain import generate_explanation
from utils.suspicious import detect_suspicious_patterns
from utils.column_trust import column_trust_score
from utils.root_cause import find_root_causes
from utils.risk import decision_risk
from utils.alerts import generate_alerts

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Data Lie Detector API",
        description="Decision Safety AI — Analyze data quality via REST API",
        version="2.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Data Lie Detector API", "version": "2.0.0"}

    @app.post("/analyze")
    async def analyze(file: UploadFile = File(...)):
        """Upload a CSV file and receive a full quality analysis.

        Returns trust score, anomalies, alerts, risk level,
        column trust scores, suspicious patterns, root causes,
        and an AI explanation.
        """
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        try:
            contents = await file.read()
            df = pd.read_csv(io.BytesIO(contents), encoding='latin1')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

        # Run full analysis pipeline
        profile = profile_data(df)
        anomalies = detect_anomalies(df, profile["numeric_cols"])
        trust_score = calculate_trust(profile, anomalies, profile["rows"])
        risk_level = decision_risk(trust_score)
        explanation = generate_explanation(trust_score, profile, anomalies)
        suspicious = detect_suspicious_patterns(df, profile["numeric_cols"])
        col_scores = column_trust_score(df)
        causes = find_root_causes(df, anomalies)
        alerts = generate_alerts(trust_score, anomalies, profile)

        return {
            "filename": file.filename,
            "trust_score": trust_score,
            "decision_risk": risk_level,
            "explanation": explanation,
            "profile": {
                "rows": profile["rows"],
                "columns": profile["cols"],
                "numeric_columns": profile["numeric_cols"],
                "categorical_columns": profile["categorical_cols"],
                "missing_percentages": profile["missing"],
                "duplicate_count": int(profile["duplicates"]),
            },
            "anomalies": anomalies,
            "column_trust_scores": col_scores,
            "suspicious_patterns": suspicious,
            "root_causes": causes,
            "alerts": [{"severity": sev, "message": msg} for sev, msg in alerts],
        }
else:
    app = None
