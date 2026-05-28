import os
import google.generativeai as genai

# Load Gemini API Key if available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(incident_data: dict, risk_score: int, reputation: str, mitre_technique: str) -> str:
    """
    Generates a professional security incident response summary.
    If Gemini API key is configured, uses LLM to generate a dynamic summary.
    Otherwise, falls back to a clean, rule-based fallback summary.
    """
    # 1. Try LLM Generation if API key exists
    if GEMINI_API_KEY:
        try:
            # Using modern Gemini 1.5 Flash
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            You are a highly experienced Security Operations Center (SOC) Analyst AI.
            Analyze the following incident telemetry and generate a highly professional, concise, action-oriented summary (max 4 sentences).
            
            Incident Details:
            - User: {incident_data.get('user')}
            - Source IP: {incident_data.get('source_ip')} (Reputation: {reputation})
            - Country: {incident_data.get('country')}
            - Severity: {incident_data.get('severity')}
            - Alert Type: {incident_data.get('alert_type')}
            
            Derived Threat Context:
            - Calculated Risk Score: {risk_score}/100
            - Mapped MITRE ATT&CK Technique: {mitre_technique}
            
            Response Format:
            - Summarize the high-level detection (e.g. High-risk impossible travel login detected).
            - Note the malicious nature of the IP and mapped MITRE technique.
            - Recommend an immediate action (e.g., immediate account lock, credential rotation).
            Do not include introductory or conversational filler. Get straight to the analysis.
            """
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            # Log failure if logging is integrated or just fallback
            pass

    # 2. Rule-based / Hardcoded Fallback (Step 10 criteria)
    reputation_status = "appears malicious" if reputation == "malicious" else "is clean/unknown"
    summary_parts = [
        f"High-risk {incident_data.get('alert_type', 'security alert')} login detected for user {incident_data.get('user', 'unknown')}.",
        f"Source IP {reputation_status}.",
        f"Mapped to MITRE {mitre_technique}."
    ]
    if risk_score >= 80:
        summary_parts.append("Recommend immediate account lock and security credential rotation.")
    elif risk_score >= 40:
        summary_parts.append("Recommend monitoring user activity and triggering an MFA prompt.")
    else:
        summary_parts.append("Recommend standard audit trail logging.")
        
    return " ".join(summary_parts)
