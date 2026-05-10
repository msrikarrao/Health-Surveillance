import os
import requests
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Northeastern Region (NER), India Bounding Box
NER_MIN_LAT = 21.0
NER_MAX_LAT = 29.5
NER_MIN_LON = 88.0
NER_MAX_LON = 97.5

RISK_THRESHOLDS = {
    "turbidity_ntu":        4.0,
    "ph_low":               6.5,
    "ph_high":              8.5,
    "bacterial_count_cfu_ml": 100,
    "nitrate_mg_l":         10.0,
    "chlorine_mg_l":        0.2,
}


def fetch_water_sources(lat: float, lon: float, radius_km: float = 50.0) -> list:
    if not (NER_MIN_LAT <= lat <= NER_MAX_LAT and NER_MIN_LON <= lon <= NER_MAX_LON):
        print("Location is outside Northeastern Region bounding box.")
        return []

    url = "https://api.obis.org/v3/occurrence"
    params = {
        "decimalLatitude": lat,
        "decimalLongitude": lon,
        "radius": int(radius_km * 1000),
        "marine": False,
        "size": 500,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"API error: {e}")
        return []

    return data.get("results", [])


def compute_contamination_risk(iot_data: dict, total_cases: int, village_count: int) -> tuple:
    score = 0.0

    turbidity = iot_data.get("turbidity_ntu", 0)
    ph = iot_data.get("ph", 7.0)
    bacterial = iot_data.get("bacterial_count_cfu_ml", 0)
    nitrate = iot_data.get("nitrate_mg_l", 0)
    chlorine = iot_data.get("chlorine_mg_l", 1.0)

    if turbidity > RISK_THRESHOLDS["turbidity_ntu"]:
        score += 0.25
    if ph < RISK_THRESHOLDS["ph_low"] or ph > RISK_THRESHOLDS["ph_high"]:
        score += 0.20
    if bacterial > RISK_THRESHOLDS["bacterial_count_cfu_ml"]:
        score += 0.30
    if nitrate > RISK_THRESHOLDS["nitrate_mg_l"]:
        score += 0.15
    if chlorine < RISK_THRESHOLDS["chlorine_mg_l"]:
        score += 0.10

    case_factor = min(total_cases / 100.0, 1.0) * 0.3
    village_factor = min(village_count / 10.0, 1.0) * 0.2

    rvi = round(min((score + case_factor + village_factor) * 100 / 1.5, 100.0), 2)

    if rvi >= 75:
        level = "HIGH"
    elif rvi >= 50:
        level = "MEDIUM"
    elif rvi >= 25:
        level = "LOW"
    else:
        level = "MINIMAL"

    return rvi, level


def train_response_model() -> RandomForestRegressor:
    X = np.array([
        [10,  1],
        [50,  2],
        [100, 3],
        [300, 5],
        [500, 8],
    ])
    y = np.array([5, 20, 50, 150, 300])

    model = RandomForestRegressor(n_estimators=20, random_state=42)
    model.fit(X, y)
    return model


def predict_response_personnel(model: RandomForestRegressor, total_cases: int, village_count: int) -> int:
    pred = model.predict([[total_cases, village_count]])[0]
    return int(round(pred))


def recommend_response_strategy(risk_level: str, water_source: str) -> str:
    if risk_level == "HIGH":
        return "Immediate water source shutdown + emergency medical teams + mass ORS distribution"
    if risk_level == "MEDIUM":
        return "Chlorination of water sources + ASHA worker mobilization + health camp setup"
    if water_source in ["river", "well"]:
        return "Water testing + boiling advisory + sanitation awareness drive"
    return "Routine monitoring + preventive health education"


def send_alert_email(alert_text: str,
                     recipient_email: str,
                     sender_email: str,
                     app_password: str):
    recipient_email = recipient_email.strip()
    sender_email = sender_email.strip()

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "🚨 JeevanDhara — Water Contamination Alert"

    msg.attach(MIMEText(alert_text, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Alert email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Email sending failed: {e}")


def generate_alert_message(
    district: str,
    village_count: int,
    total_cases: int,
    water_source: str,
    iot_data: dict,
    rvi: float,
    risk_level: str,
    personnel: int,
    strategy: str
) -> str:
    return f"""\
🚨 JEEVANDHARA — WATER CONTAMINATION ALERT 🚨
Smart Health Surveillance & Early Warning System
District: {district}

Outbreak Summary:
• Affected Villages : {village_count}
• Total Cases (7-day): {total_cases}
• Primary Water Source: {water_source.capitalize()}

Water Quality Readings:
• Turbidity     : {iot_data.get('turbidity_ntu', 'N/A')} NTU  (safe: < 4.0)
• pH            : {iot_data.get('ph', 'N/A')}             (safe: 6.5 – 8.5)
• Bacterial Count: {iot_data.get('bacterial_count_cfu_ml', 'N/A')} CFU/mL (safe: < 100)
• Nitrate       : {iot_data.get('nitrate_mg_l', 'N/A')} mg/L   (safe: < 10.0)
• Chlorine      : {iot_data.get('chlorine_mg_l', 'N/A')} mg/L   (safe: > 0.2)

Risk Assessment:
• Contamination Risk Index : {rvi}/100
• Risk Level               : {risk_level}

Response Plan:
• Estimated Health Workers Required: {personnel}
• Recommended Strategy: {strategy}

— JeevanDhara Automated Alert System
"""


contamination_bp = Blueprint('contamination', __name__)

@contamination_bp.route('/contamination-alert', methods=['POST'])
def contamination_alert():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    recipient_email    = data.get('recipient_email')
    recipient_name     = data.get('recipient_name', 'Health Official')
    district           = data.get('district', 'Unknown')
    total_cases        = data.get('total_cases', 0)
    village_count      = data.get('village_count', 0)
    water_source       = data.get('water_source', 'unknown')
    risk_level         = data.get('risk_level', 'LOW')
    predicted_disease  = data.get('predicted_disease', 'N/A')
    confidence_score   = data.get('confidence_score', 0)

    if not recipient_email:
        return jsonify({'error': 'recipient_email is required'}), 400

    response_model     = train_response_model()
    estimated_personnel = predict_response_personnel(response_model, total_cases, village_count)
    strategy           = recommend_response_strategy(risk_level, water_source)

    alert_text = f"""\n🚨 JEEVANDHARA — OUTBREAK ALERT 🚨
Smart Health Surveillance & Early Warning System

Dear {recipient_name},

District        : {district}
Risk Level      : {risk_level}
Predicted Disease: {predicted_disease}
Confidence      : {confidence_score}%

Outbreak Summary:
• Affected Villages  : {village_count}
• Total Cases (7-day): {total_cases}
• Primary Water Source: {water_source.capitalize()}

Response Plan:
• Estimated Health Workers Required: {estimated_personnel}
• Recommended Strategy: {strategy}

— JeevanDhara Automated Alert System
"""

    sender    = os.getenv('EMAIL_USER')
    password  = os.getenv('EMAIL_PASS')

    if not sender or not password:
        return jsonify({'error': 'Email credentials not configured'}), 503

    send_alert_email(alert_text, recipient_email, sender, password)
    return jsonify({'status': 'Alert email sent', 'recipient': recipient_email}), 200


def main():
    district = "Kamrup"
    village_count = 4
    total_cases = 85
    water_source = "river"
    latitude = 26.1
    longitude = 91.7

    iot_data = {
        "turbidity_ntu": 6.2,
        "ph": 6.1,
        "bacterial_count_cfu_ml": 180,
        "nitrate_mg_l": 12.5,
        "chlorine_mg_l": 0.05,
    }

    print("Fetching regional water source data...")
    fetch_water_sources(latitude, longitude, radius_km=50.0)

    rvi_score, risk_level = compute_contamination_risk(iot_data, total_cases, village_count)

    response_model = train_response_model()
    estimated_personnel = predict_response_personnel(response_model, total_cases, village_count)

    strategy = recommend_response_strategy(risk_level, water_source)

    alert_text = generate_alert_message(
        district, village_count, total_cases, water_source,
        iot_data, rvi_score, risk_level, estimated_personnel, strategy
    )

    print("\n" + "=" * 80)
    print(alert_text)
    print("=" * 80)

    YOUR_GMAIL = os.getenv("EMAIL_USER")
    GMAIL_APP_PASSWORD = os.getenv("EMAIL_PASS")
    RECIPIENT_EMAIL = os.getenv("EMAIL_USER")

    send_alert_email(
        alert_text=alert_text,
        recipient_email=RECIPIENT_EMAIL,
        sender_email=YOUR_GMAIL,
        app_password=GMAIL_APP_PASSWORD
    )


if __name__ == "__main__":
    main()
