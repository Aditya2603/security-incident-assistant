from fastapi import FastAPI

from models import Incident
from risk_engine import calculate_risk
from threat_intel import ip_reputation
from mitre_mapper import get_technique
from logs.logger import logger

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "running"
    }

@app.post("/incident")
def process_incident(incident: Incident):

    logger.info(
        f"Processing incident for {incident.user}"
    )

    risk_score = calculate_risk(
        incident.country,
        incident.severity
    )

    reputation = ip_reputation(
        incident.source_ip
    )

    mitre = get_technique(
        incident.alert_type
    )

    logger.info(
        f"Risk Score: {risk_score}"
    )

    logger.info(
        f"Reputation: {reputation}"
    )

    logger.info(
        f"MITRE: {mitre}"
    )

    return {
        "user": incident.user,
        "risk_score": risk_score,
        "ip_reputation": reputation,
        "mitre": mitre
    }