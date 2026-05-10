from flask import Flask, request, jsonify
from flask_cors import CORS
from model_advanced import AdvancedOutbreakPredictor
from water_quality_model import WaterQualityModel
from water_contamination_alert import contamination_bp
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(contamination_bp)

# Initialize advanced predictor
try:
    predictor = AdvancedOutbreakPredictor()
    logger.info("✅ Advanced ML Predictor initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize predictor: {e}")
    predictor = None

# Initialize water quality model
try:
    water_model = WaterQualityModel()
    logger.info("✅ Water Quality Model initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize water quality model: {e}")
    water_model = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'Advanced ML Prediction Service',
            'version': '2.0',
            'model_status': 'ready' if predictor else 'error',
            'model_type': 'Gradient Boosting Classifier',
            'data_sources': [
                'health_symptoms',
                'water_quality',
                'sanitation_environment',
                'demographics_infrastructure'
            ]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict disease outbreak risk using multiple data sources
    
    Expected JSON (all optional, but more sources = better predictions):
    {
        "symptomCounts": {
            "diarrhea": 10,
            "vomiting": 5,
            "fever": 3,
            "headache": 2,
            "fatigue": 1,
            "nausea": 1
        },
        "asha_data": {
            "vaccination_coverage": 0.75,
            "awareness_level": "high|medium|low",
            "previous_outbreaks": 1,
            "reports_count": 15
        },
        "seasonal_data": {
            "season": "monsoon|post_monsoon|winter|summer",
            "average_humidity": 85,
            "average_rainfall_mm": 450,
            "disease_risk_factor": 0.8
        },
        "iot_data": {
            "turbidity_ntu": 2.5,
            "ph": 7.2,
            "bacterial_count_cfu_ml": 50,
            "nitrate_mg_l": 5,
            "chlorine_mg_l": 1.0
        },
        "water_source": {
            "source_type": "well|tap|river|tank",
            "maintenance_status": "excellent|good|fair|poor",
            "chlorination": 1,
            "age_years": 5
        },
        "villageCount": 3,
        "totalReports": 15
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("❌ No JSON data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        if 'symptomCounts' not in data:
            return jsonify({'error': 'symptomCounts is required'}), 400
        
        logger.info(f"📊 Advanced prediction request with {len(data)} data sources")
        
        if not predictor:
            logger.error("❌ Predictor not initialized")
            return jsonify({'error': 'ML service not initialized'}), 503
        
        prediction = predictor.predict(data)
        
        if 'error' in prediction:
            logger.error(f"Prediction error: {prediction['error']}")
            return jsonify(prediction), 500
        
        logger.info(f"✅ Prediction: {prediction['riskLevel']} risk ({prediction['confidenceScore']}% confidence)")
        return jsonify(prediction), 200
    
    except Exception as e:
        error_message = str(e)
        error_trace = traceback.format_exc()
        logger.error(f"❌ Prediction failed: {error_message}\n{error_trace}")
        
        return jsonify({
            'error': error_message,
            'riskLevel': 'UNKNOWN',
            'confidenceScore': 0,
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the model"""
    try:
        if not predictor or not predictor.model:
            return jsonify({'error': 'Model not initialized'}), 503
        
        info = {
            'status': 'ready',
            'model_type': 'Gradient Boosting Classifier',
            'n_estimators': predictor.model.n_estimators,
            'features': predictor.feature_names,
            'feature_count': len(predictor.feature_names),
            'data_sources': [
                'Health Symptoms (8 features)',
                'Water Quality (9 features)',
                'Sanitation & Environment (6 features)',
                'Demographics & Infrastructure (5 features)'
            ],
            'total_feature_count': len(predictor.feature_names)
        }
        return jsonify(info), 200
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain the model"""
    try:
        logger.info("🔄 Retraining model with all data sources...")
        global predictor
        predictor = AdvancedOutbreakPredictor(retrain=True)
        logger.info("✅ Model retrained successfully")
        return jsonify({
            'status': 'success',
            'message': 'Model retrained successfully with all data sources'
        }), 200
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/water-quality', methods=['POST'])
def water_quality():
    """
    Predict water potability from sensor readings.

    Expected JSON (all optional — missing values are imputed):
    {
        "ph": 7.2,
        "turbidity_ntu": 5.0,
        "fecal_coliform_per_100ml": 0,
        "total_coliform_per_100ml": 0,
        "tds_mg_l": 400,
        "nitrate_mg_l": 10,
        "bod_mg_l": 2.0,
        "dissolved_oxygen_mg_l": 7.5,
        "fluoride_mg_l": 0.8,
        "arsenic_ug_l": 5.0
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if not water_model:
            return jsonify({'error': 'Water quality model not initialized'}), 503

        result = water_model.predict(data)
        logger.info(f"💧 Water quality: {'Potable' if result['potable'] else 'Not Potable'} ({result['potabilityScore']}%)")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"❌ Water quality prediction failed: {e}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 ADVANCED ML PREDICTION SERVICE v2.0")
    print("=" * 70)
    print("📊 Features:")
    print("   • Health Symptoms Analysis")
    print("   • ASHA Worker Reports Integration")
    print("   • Seasonal Pattern Recognition")
    print("   • IoT Water Quality Monitoring")
    print("   • Water Infrastructure Assessment")
    print("\n🤖 Model: Gradient Boosting Classifier with 200 estimators")
    print("📈 Features: 24 input features from 5 data sources")
    print("✅ Service ready for multi-source predictions\n")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        use_reloader=False,
        threaded=True
    )
