import numpy as np
import pandas as pd
import os
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OutbreakPredictor:
    """
    ML-based outbreak prediction model
    Uses Random Forest with multiple health indicators
    """
    
    def __init__(self, model_path=None, retrain=False):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'diarrhea', 'vomiting', 'fever', 'headache', 'fatigue', 'nausea',
            'sanitation_score', 'rainfall_score', 'village_count'
        ]
        self.model_path = model_path or os.path.join(os.path.dirname(__file__), 'model.pkl')
        self.scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
        
        logger.info("🚀 Initializing Outbreak Predictor")
        
        # Try to load existing model, otherwise train new one
        if os.path.exists(self.model_path) and not retrain:
            self._load_model()
            logger.info("✅ Model loaded from disk")
        else:
            logger.info("🔄 Training new model...")
            self._train_model()
            self._save_model()
            logger.info("✅ Model trained and saved")
    
    def _train_model(self):
        """Train the outbreak prediction model"""
        try:
            # Load dataset
            dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'dataset.csv')
            
            if not os.path.exists(dataset_path):
                logger.warning(f"Dataset not found at {dataset_path}, using synthetic data")
                df = self._create_synthetic_data()
            else:
                df = pd.read_csv(dataset_path)
                logger.info(f"Loaded dataset with {len(df)} records")
            
            # Prepare features - handle both old and new column names
            feature_columns = []
            for feature in self.feature_names:
                if feature in df.columns:
                    feature_columns.append(feature)
                elif f'symptom_{feature}' in df.columns:
                    feature_columns.append(f'symptom_{feature}')
            
            # If we don't have all features, create them from what we have
            if len(feature_columns) < len(self.feature_names):
                feature_columns = self._prepare_features_from_data(df)
            
            X = df[feature_columns].fillna(0).values
            
            # Determine target variable
            if 'confirmed_outbreak' in df.columns:
                y = df['confirmed_outbreak'].values
            elif 'outbreak' in df.columns:
                y = df['outbreak'].values
            else:
                # Create target based on symptom counts
                y = (df[[col for col in df.columns if 'diarrhea' in col.lower()]].sum(axis=1) > 10).astype(int).values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model with better parameters
            self.model = RandomForestClassifier(
                n_estimators=150,           # More trees for better accuracy
                max_depth=15,               # Prevent overfitting
                min_samples_split=5,        # Minimum samples for split
                min_samples_leaf=2,         # Minimum samples in leaf
                random_state=42,
                n_jobs=-1,                  # Use all CPU cores
                verbose=0
            )
            
            # Split data for validation
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"Model Accuracy: {accuracy:.2%}")
            logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            # Fall back to a simple model
            self._create_fallback_model()
    
    def _prepare_features_from_data(self, df):
        """Prepare features from available data"""
        feature_columns = []
        
        # Map feature names to potential column names
        feature_mapping = {
            'diarrhea': ['symptom_diarrhea', 'diarrhea', 'diarrhea_count'],
            'vomiting': ['symptom_vomiting', 'vomiting', 'vomiting_count'],
            'fever': ['symptom_fever', 'fever', 'fever_count'],
            'headache': ['symptom_headache', 'headache', 'headache_count'],
            'fatigue': ['symptom_fatigue', 'fatigue', 'fatigue_count'],
            'nausea': ['symptom_nausea', 'nausea', 'nausea_count'],
            'sanitation_score': ['sanitation', 'sanitation_level', 'sanitation_score'],
            'rainfall_score': ['rainfall', 'rainfall_level', 'rainfall_score'],
            'village_count': ['villages', 'village_count', 'affected_villages']
        }
        
        for feature, alternatives in feature_mapping.items():
            for alt in alternatives:
                if alt in df.columns:
                    feature_columns.append(alt)
                    break
        
        if not feature_columns:
            # Use all numeric columns if mapping fails
            feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()[:9]
        
        return feature_columns[:9]  # Limit to 9 features
    
    def _create_fallback_model(self):
        """Create a simple fallback model"""
        logger.warning("Creating fallback model with minimal data")
        
        # Create minimal training data
        X = np.array([
            [10, 5, 3, 2, 1, 1, 2, 2, 1],   # High outbreak
            [5, 2, 1, 1, 0, 0, 1, 1, 1],    # Medium
            [1, 0, 0, 0, 0, 0, 0, 0, 1]     # Low
        ])
        
        y = np.array([1, 1, 0])  # outbreak, outbreak, no outbreak
        
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_scaled, y)
    
    def _load_model(self):
        """Load pre-trained model from disk"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}. Training new model.")
            self._train_model()
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def _create_synthetic_data(self):
        """Create synthetic training data if dataset not available"""
        np.random.seed(42)
        n_samples = 200
        
        data = {
            'diarrhea': np.random.poisson(lam=5, size=n_samples),
            'vomiting': np.random.poisson(lam=3, size=n_samples),
            'fever': np.random.poisson(lam=4, size=n_samples),
            'headache': np.random.poisson(lam=2, size=n_samples),
            'fatigue': np.random.poisson(lam=2, size=n_samples),
            'nausea': np.random.poisson(lam=1, size=n_samples),
            'sanitation_score': np.random.randint(0, 3, n_samples),
            'rainfall_score': np.random.randint(0, 3, n_samples),
            'village_count': np.random.randint(1, 10, n_samples),
        }
        
        # Create target: outbreak if diarrhea > 10 or multiple high symptoms
        data['confirmed_outbreak'] = (
            (data['diarrhea'] > 10) | 
            ((data['diarrhea'] > 5) & (data['vomiting'] > 5))
        ).astype(int)
        
        return pd.DataFrame(data)
    
    def predict(self, data):
        """
        Predict outbreak risk level
        
        Expected input:
        {
            'symptomCounts': {
                'diarrhea': int,
                'vomiting': int,
                'fever': int,
                'headache': int,
                'fatigue': int,
                'nausea': int
            },
            'sanitationLevel': 'low|medium|high',
            'rainfallLevel': 'low|medium|high',
            'villageCount': int,
            'totalReports': int
        }
        """
        try:
            # Extract symptom counts
            symptom_counts = data.get('symptomCounts', {})
            diarrhea = symptom_counts.get('diarrhea', 0)
            vomiting = symptom_counts.get('vomiting', 0)
            fever = symptom_counts.get('fever', 0)
            headache = symptom_counts.get('headache', 0)
            fatigue = symptom_counts.get('fatigue', 0)
            nausea = symptom_counts.get('nausea', 0)
            
            # Extract environmental factors
            sanitation_level = data.get('sanitationLevel', 'medium').lower()
            rainfall_level = data.get('rainfallLevel', 'medium').lower()
            village_count = data.get('villageCount', 0)
            total_reports = data.get('totalReports', 0)
            
            # Convert categorical to numeric
            sanitation_score = {'low': 2, 'medium': 1, 'high': 0}.get(sanitation_level, 1)
            rainfall_score = {'low': 0, 'medium': 1, 'high': 2}.get(rainfall_level, 1)
            
            # Prepare features for prediction
            features = np.array([[
                diarrhea, vomiting, fever, headache, fatigue, nausea,
                sanitation_score, rainfall_score, village_count
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            outbreak_prob = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            confidence = round(float(max(probabilities) * 100))
            
            # Get feature importance
            feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
            
            # Determine risk level and disease based on multiple factors
            risk_score = (
                (diarrhea * 0.3) + 
                (vomiting * 0.2) + 
                (fever * 0.15) + 
                (sanitation_score * 0.15) + 
                (rainfall_score * 0.1) + 
                (village_count * 0.1)
            )
            
            # Classification logic
            if outbreak_prob >= 0.65 or risk_score >= 15 or diarrhea >= 15:
                risk_level = 'HIGH'
                if diarrhea >= 10:
                    disease = 'Cholera outbreak'
                elif vomiting >= 8:
                    disease = 'Cholera outbreak'
                elif fever >= 10:
                    disease = 'Typhoid outbreak'
                else:
                    disease = 'Acute gastroenteritis outbreak'
            elif outbreak_prob >= 0.35 or risk_score >= 8 or diarrhea >= 8:
                risk_level = 'MEDIUM'
                if diarrhea >= 5:
                    disease = 'Diarrheal disease cluster'
                else:
                    disease = 'Hepatitis A suspected'
            else:
                risk_level = 'LOW'
                disease = 'No significant outbreak risk'
            
            # Build explanation
            explanation = self._build_explanation(
                diarrhea, vomiting, fever, village_count, 
                total_reports, sanitation_level, rainfall_level
            )
            
            result = {
                'riskLevel': risk_level,
                'confidenceScore': confidence,
                'predictedDisease': disease,
                'explanation': explanation,
                'timestamp': datetime.now().isoformat(),
                'riskScore': round(risk_score, 2),
                'topFactors': sorted(
                    feature_importance.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:3]
            }
            
            logger.info(f"Prediction: {risk_level} risk for {disease} (confidence: {confidence}%)")
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {
                'error': str(e),
                'riskLevel': 'UNKNOWN',
                'confidenceScore': 0,
                'predictedDisease': 'Unable to predict',
                'explanation': f'Error during prediction: {str(e)}'
            }
    
    def _build_explanation(self, diarrhea, vomiting, fever, village_count, 
                          total_reports, sanitation_level, rainfall_level):
        """Build human-readable explanation"""
        parts = []
        
        if diarrhea > 0:
            parts.append(f"{diarrhea} diarrhea cases")
        if vomiting > 0:
            parts.append(f"{vomiting} vomiting cases")
        if fever > 0:
            parts.append(f"{fever} fever cases")
        
        symptoms_text = ", ".join(parts) if parts else "minimal reported symptoms"
        
        explanation = f"Analyzed {total_reports} health reports: {symptoms_text} "
        explanation += f"across {village_count} villages. "
        explanation += f"Environmental conditions: {sanitation_level} sanitation, {rainfall_level} rainfall. "
        
        return explanation
