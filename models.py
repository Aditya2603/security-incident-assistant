from pydantic import BaseModel

class Incident(BaseModel):
    user: str
    source_ip: str
    country: str
    severity: str
    alert_type: str