import numpy as np
import pandas as pd
import os
import joblib
import logging
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score
from datetime import datetime
from xgboost import XGBClassifier
from imblearn.combine import SMOTETomek
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

FEATURE_NAMES = [
    # Symptoms (8)
    'symptom_diarrhea', 'symptom_vomiting', 'symptom_fever', 'symptom_abdominal_pain',
    'symptom_dehydration', 'symptom_jaundice', 'symptom_bloody_stool', 'symptom_skin_rash',
    # Water quality (9)
    'ph', 'turbidity_ntu', 'fecal_coliform_per_100ml', 'total_coliform_per_100ml',
    'tds_mg_l', 'nitrate_mg_l', 'bod_mg_l', 'dissolved_oxygen_mg_l', 'water_quality_index',
    # Sanitation / environment (6)
    'open_defecation_rate', 'toilet_access', 'sewage_treatment_pct',
    'avg_rainfall_mm', 'avg_humidity_pct', 'flooding',
    # Demographics / source (5)
    'is_urban', 'population_density', 'age',
    'water_source_risk', 'water_treatment_risk',
    # Engineered features (6)
    'symptom_count', 'water_contamination_score', 'sanitation_risk',
    'environmental_risk', 'age_vulnerability', 'population_risk'
]

WATER_SOURCE_RISK  = {'Piped': 0.1, 'Borewell': 0.3, 'Rainwater': 0.3,
                      'Open Well': 0.6, 'Tanker': 0.6, 'Pond': 0.8, 'River': 0.9}
WATER_TREATMENT_RISK = {'Chlorinated': 0.1, 'Filtered': 0.2, 'Boiled': 0.3, 'Untreated': 1.0}
SEASON_MAP         = {'Winter': 1, 'Summer': 2, 'Monsoon': 3, 'Post-Monsoon': 4}
HANDWASH_MAP       = {'Always': 1.0, 'Sometimes': 0.5, 'Never': 0.0}

DISEASE_LABELS = ['No_Disease', 'Cholera', 'Dysentery', 'Giardiasis',
                  'Hepatitis_A', 'Hepatitis_E', 'Leptospirosis', 'Typhoid']

SAMPLE_SIZE = 5_000  # Reduced for faster training


class AdvancedOutbreakPredictor:
    """
    ML-based disease risk predictor trained on waterborne_disease_dataset.csv.
    Predicts one of 8 disease classes (including No_Disease).
    """

    def __init__(self, model_path=None, retrain=False):
        self.model       = None
        self.scaler      = StandardScaler()
        self.feature_names = FEATURE_NAMES
        self.model_path  = model_path or os.path.join(os.path.dirname(__file__), 'model.pkl')
        self.scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
        self.test_path   = os.path.join(os.path.dirname(__file__), 'disease_test.pkl')
        self.dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'waterborne_disease_dataset.csv')

        logger.info("🚀 Initializing Advanced Outbreak Predictor")

        if os.path.exists(self.model_path) and not retrain:
            self._load_model()
            logger.info("✅ Model loaded from disk")
            self._print_report()
        else:
            logger.info("🔄 Training new model from local dataset...")
            self._train_model()
            self._save_model()
            logger.info("✅ Model trained and saved")

    # ------------------------------------------------------------------
    # Data preparation
    # ------------------------------------------------------------------

    def _load_dataset(self):
        if not os.path.exists(self.dataset_path):
            logger.error(f"❌ Dataset not found at {self.dataset_path}")
            return None
        df = pd.read_csv(self.dataset_path)
        logger.info(f"✅ Loaded {len(df)} rows from waterborne_disease_dataset.csv")
        return df

    def _build_features(self, df):
        """Build features with advanced feature engineering"""
        # Original features
        features = []
        
        # Symptoms (8)
        symptom_cols = ['symptom_diarrhea', 'symptom_vomiting', 'symptom_fever', 
                       'symptom_abdominal_pain', 'symptom_dehydration', 
                       'symptom_jaundice', 'symptom_bloody_stool', 'symptom_skin_rash']
        for col in symptom_cols:
            features.append(df[col].fillna(0).values)
        
        # Symptom count (engineered feature)
        symptom_count = sum(df[col].fillna(0).values for col in symptom_cols)
        
        # Water quality features (9)
        ph = df['ph'].fillna(7.3).values
        turbidity = df['turbidity_ntu'].fillna(5.0).values
        fecal = df['fecal_coliform_per_100ml'].fillna(0).values
        total_coliform = df['total_coliform_per_100ml'].fillna(0).values
        tds = df['tds_mg_l'].fillna(500).values
        nitrate = df['nitrate_mg_l'].fillna(10).values
        bod = df['bod_mg_l'].fillna(3.0).values
        do_level = df['dissolved_oxygen_mg_l'].fillna(7.0).values
        wqi = df['water_quality_index'].fillna(50).values
        
        features.extend([ph, turbidity, fecal, total_coliform, tds, nitrate, bod, do_level, wqi])
        
        # Engineered water quality features
        water_contamination_score = (
            (fecal > 100).astype(float) * 3 +
            (total_coliform > 500).astype(float) * 2 +
            (turbidity > 5).astype(float) * 1.5 +
            (bod > 5).astype(float) * 1.5 +
            np.abs(ph - 7.0) * 0.5
        )
        
        # Sanitation / environment (6)
        open_def = df['open_defecation_rate'].fillna(30).values
        toilet = df['toilet_access'].fillna(0).values
        sewage = df['sewage_treatment_pct'].fillna(30).values
        rainfall = df['avg_rainfall_mm'].fillna(100).values
        humidity = df['avg_humidity_pct'].fillna(60).values
        flooding = df['flooding'].fillna(0).values
        
        features.extend([open_def, toilet, sewage, rainfall, humidity, flooding])
        
        # Engineered sanitation score
        sanitation_risk = (
            (open_def / 100) * 2 +
            (1 - toilet) * 1.5 +
            (1 - sewage / 100) * 1.5
        )
        
        # Demographics / source (5)
        is_urban = df['is_urban'].fillna(0).values
        pop_density = df['population_density'].fillna(500).values
        age = df['age'].fillna(25).values
        water_source_risk = df['water_source'].map(WATER_SOURCE_RISK).fillna(0.5).values
        water_treatment_risk = df['water_treatment'].map(WATER_TREATMENT_RISK).fillna(0.5).values
        
        features.extend([is_urban, pop_density, age, water_source_risk, water_treatment_risk])
        
        # Additional engineered features
        features.append(symptom_count)
        features.append(water_contamination_score)
        features.append(sanitation_risk)
        
        # Environmental risk interaction
        env_risk = (rainfall / 100) * humidity / 100 * (1 + flooding)
        features.append(env_risk)
        
        # Age vulnerability (children and elderly more vulnerable)
        age_vulnerability = np.where(age < 5, 2.0, 
                           np.where(age > 60, 1.5,
                           np.where(age < 15, 1.2, 1.0)))
        features.append(age_vulnerability)
        
        # Population density risk
        pop_risk = np.log1p(pop_density) / 10
        features.append(pop_risk)
        
        X = np.column_stack(features).astype(float)
        return X

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def _train_model(self):
        df = self._load_dataset()
        if df is None or len(df) == 0:
            logger.warning("Dataset unavailable — using synthetic fallback")
            X, y = self._synthetic_data()
        else:
            # Stratified sample to keep training fast
            n_per_class = SAMPLE_SIZE // df['disease'].nunique()
            sampled = [
                g.sample(min(len(g), n_per_class), random_state=42)
                for _, g in df.groupby('disease', sort=False)
            ]
            df = pd.concat(sampled, ignore_index=True)
            logger.info(f"📊 Using {len(df)} stratified samples for training")

            X = self._build_features(df)
            y = df['disease'].astype(str).to_numpy()

        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        # Apply SMOTE for handling class imbalance
        logger.info("🔄 Applying SMOTE for class balancing...")
        smote_tomek = SMOTETomek(random_state=42)
        X_train_balanced, y_train_balanced = smote_tomek.fit_resample(X_train, y_train)
        logger.info(f"✅ Balanced training set: {len(X_train)} → {len(X_train_balanced)} samples")

        # Optimized ensemble - faster training, still high accuracy
        xgb_model = XGBClassifier(
            n_estimators=150, learning_rate=0.05, max_depth=7,
            subsample=0.85, colsample_bytree=0.85,
            random_state=42, n_jobs=-1, eval_metric='mlogloss'
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=150, learning_rate=0.05, max_depth=7,
            min_samples_split=3, min_samples_leaf=2, subsample=0.85,
            random_state=42
        )
        
        rf_model = RandomForestClassifier(
            n_estimators=150, max_depth=12, min_samples_split=3,
            min_samples_leaf=2, max_features='sqrt',
            random_state=42, n_jobs=-1, class_weight='balanced'
        )
        
        # Use Voting instead of Stacking for faster training
        self.model = VotingClassifier(
            estimators=[
                ('xgb', xgb_model),
                ('gb', gb_model),
                ('rf', rf_model)
            ],
            voting='soft',
            n_jobs=-1
        )
        
        logger.info("🔄 Training voting ensemble (XGB + GB + RF)...")
        self.model.fit(X_train_balanced, y_train_balanced)
        
        # Store test data and print report
        joblib.dump((X_test, y_test), self.test_path)
        
        # Print classification report
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        report = classification_report(y_test, y_pred)
        print(f"\n=== Disease Risk Model ===")
        print(f"Accuracy: {acc:.3f}, F1-Score: {f1:.3f}")
        print(report)

    def _print_report(self):
        try:
            # Try to load stored test data first
            if os.path.exists(self.test_path):
                X_test, y_test = joblib.load(self.test_path)
            else:
                # If test data doesn't exist, skip printing (model needs retraining)
                logger.warning("Test data not found. Retrain the model to see classification report.")
                return
            
            y_pred = self.model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            report = classification_report(y_test, y_pred)
            print(f"\n=== Disease Risk Model ===")
            print(f"Accuracy: {acc:.3f}, F1-Score: {f1:.3f}")
            print(report)
        except Exception as e:
            logger.warning(f"Could not print classification report: {e}")

    def _synthetic_data(self):
        np.random.seed(42)
        n = 300
        X = np.random.randn(n, len(FEATURE_NAMES))
        y = np.random.choice(DISEASE_LABELS, n)
        return X, y

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save_model(self):
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

    def _load_model(self):
        try:
            self.model  = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        except Exception as e:
            logger.error(f"Error loading model: {e} — retraining")
            self._train_model()

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict(self, data: dict) -> dict:
        """
        Predict disease risk for a single report.

        Expected input:
        {
            "symptomCounts": {
                "diarrhea": 0|1, "vomiting": 0|1, "fever": 0|1,
                "abdominal_pain": 0|1, "dehydration": 0|1, "jaundice": 0|1,
                "bloody_stool": 0|1, "skin_rash": 0|1
            },
            "waterQuality": {
                "ph": 7.2, "turbidity_ntu": 5.0,
                "fecal_coliform_per_100ml": 100, "total_coliform_per_100ml": 200,
                "tds_mg_l": 400, "nitrate_mg_l": 10, "bod_mg_l": 3.0,
                "dissolved_oxygen_mg_l": 7.0, "water_quality_index": 50
            },
            "sanitationLevel": "low|medium|high",
            "rainfallLevel": "low|medium|high",
            "waterSourceType": "Piped|Borewell|Open Well|River|Pond|Tanker|Rainwater",
            "waterTreatment": "Filtered|Boiled|Chlorinated|Untreated",
            "flooding": 0|1,
            "isUrban": 0|1,
            "populationDensity": 500,
            "patientAge": 25
        }
        """
        try:
            sc = data.get('symptomCounts', {})
            wq = data.get('waterQuality', {})

            sanitation = data.get('sanitationLevel', 'medium').lower()
            open_def   = {'low': 10, 'medium': 40, 'high': 70}.get(sanitation, 40)
            toilet     = {'low': 0, 'medium': 1, 'high': 1}.get(sanitation, 1)
            sewage     = {'low': 10, 'medium': 40, 'high': 80}.get(sanitation, 40)

            rainfall_level = data.get('rainfallLevel', 'medium').lower()
            rainfall_mm    = {'low': 25, 'medium': 150, 'high': 500}.get(rainfall_level, 150)
            humidity       = {'low': 40, 'medium': 65, 'high': 85}.get(rainfall_level, 65)

            water_source    = data.get('waterSourceType', 'Borewell')
            water_treatment = data.get('waterTreatment', 'Untreated')
            age = float(data.get('patientAge', 25))
            pop_density = float(data.get('populationDensity', 500))
            flooding = float(data.get('flooding', 0))
            
            # Base features
            symptom_diarrhea = int(bool(sc.get('diarrhea', 0)))
            symptom_vomiting = int(bool(sc.get('vomiting', 0)))
            symptom_fever = int(bool(sc.get('fever', 0)))
            symptom_abdominal = int(bool(sc.get('abdominal_pain', 0)))
            symptom_dehydration = int(bool(sc.get('dehydration', 0)))
            symptom_jaundice = int(bool(sc.get('jaundice', 0)))
            symptom_bloody = int(bool(sc.get('bloody_stool', 0)))
            symptom_rash = int(bool(sc.get('skin_rash', 0)))
            
            ph = float(wq.get('ph', 7.3))
            turbidity = float(wq.get('turbidity_ntu', 5.0))
            fecal = float(wq.get('fecal_coliform_per_100ml', 0))
            total_coliform = float(wq.get('total_coliform_per_100ml', 0))
            tds = float(wq.get('tds_mg_l', 500))
            nitrate = float(wq.get('nitrate_mg_l', 10))
            bod = float(wq.get('bod_mg_l', 3.0))
            do_level = float(wq.get('dissolved_oxygen_mg_l', 7.0))
            wqi_val = float(wq.get('water_quality_index', 50))
            
            # Engineered features
            symptom_count = sum([symptom_diarrhea, symptom_vomiting, symptom_fever,
                               symptom_abdominal, symptom_dehydration, symptom_jaundice,
                               symptom_bloody, symptom_rash])
            
            water_contamination_score = (
                (fecal > 100) * 3 +
                (total_coliform > 500) * 2 +
                (turbidity > 5) * 1.5 +
                (bod > 5) * 1.5 +
                abs(ph - 7.0) * 0.5
            )
            
            sanitation_risk = (
                (open_def / 100) * 2 +
                (1 - toilet) * 1.5 +
                (1 - sewage / 100) * 1.5
            )
            
            env_risk = (rainfall_mm / 100) * (humidity / 100) * (1 + flooding)
            
            age_vulnerability = 2.0 if age < 5 else (1.5 if age > 60 else (1.2 if age < 15 else 1.0))
            
            pop_risk = np.log1p(pop_density) / 10

            features = [
                symptom_diarrhea, symptom_vomiting, symptom_fever, symptom_abdominal,
                symptom_dehydration, symptom_jaundice, symptom_bloody, symptom_rash,
                ph, turbidity, fecal, total_coliform, tds, nitrate, bod, do_level, wqi_val,
                float(open_def), float(toilet), float(sewage),
                float(rainfall_mm), float(humidity), flooding,
                float(data.get('isUrban', 0)), pop_density, age,
                float(WATER_SOURCE_RISK.get(water_source, 0.5)),
                float(WATER_TREATMENT_RISK.get(water_treatment, 0.5)),
                symptom_count, water_contamination_score, sanitation_risk,
                env_risk, age_vulnerability, pop_risk
            ]

            X = np.array([features], dtype=float)
            X_scaled = self.scaler.transform(X)

            probabilities = self.model.predict_proba(X_scaled)[0]
            classes       = self.model.classes_
            predicted_cls = classes[np.argmax(probabilities)]
            confidence    = round(float(np.max(probabilities)) * 100)

            is_disease    = predicted_cls != 'No_Disease'
            disease_prob  = 1.0 - float(probabilities[list(classes).index('No_Disease')]) \
                            if 'No_Disease' in classes else float(np.max(probabilities))

            if disease_prob >= 0.65:
                risk_level = 'HIGH'
            elif disease_prob >= 0.35:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'

            risk_score = round(
                sc.get('diarrhea', 0) * 3.0 + sc.get('vomiting', 0) * 2.0 +
                sc.get('fever', 0) * 1.5 + sc.get('jaundice', 0) * 2.5 +
                sc.get('abdominal_pain', 0) * 1.5 + sc.get('bloody_stool', 0) * 2.0 +
                WATER_SOURCE_RISK.get(water_source, 0.5) * 2.0 +
                WATER_TREATMENT_RISK.get(water_treatment, 0.5) * 2.0 +
                data.get('flooding', 0) * 1.5, 2
            )

            explanation = self._build_explanation(sc, sanitation, rainfall_level,
                                                   water_source, water_treatment,
                                                   risk_level, data.get('waterQuality'))

            logger.info(f"Prediction: {predicted_cls} | {risk_level} ({confidence}% confidence)")
            return {
                'riskLevel':        risk_level,
                'confidenceScore':  confidence,
                'predictedDisease': predicted_cls.replace('_', ' '),
                'explanation':      explanation,
                'timestamp':        datetime.now().isoformat(),
                'riskScore':        risk_score,
            }

        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {
                'error':            str(e),
                'riskLevel':        'UNKNOWN',
                'confidenceScore':  0,
                'predictedDisease': 'Unable to predict',
            }

    def _build_explanation(self, sc, sanitation, rainfall, water_source,
                           water_treatment, risk_level, wq=None):
        present = [s.replace('_', ' ') for s, v in sc.items() if v]
        symptoms_text = ', '.join(present) if present else 'no symptoms'

        msg = f"Patient presents with: {symptoms_text}. "
        msg += f"Environment: {sanitation} sanitation, {rainfall} rainfall, "
        msg += f"{water_source} water source ({water_treatment}). "

        if wq:
            wqi = wq.get('water_quality_index')
            if wqi is not None:
                msg += f"Water quality index: {wqi}. "

        if risk_level == 'HIGH':
            msg += "High risk — immediate medical attention recommended."
        elif risk_level == 'MEDIUM':
            msg += "Moderate risk — monitor closely and consider medical consultation."
        else:
            msg += "Low risk based on current symptoms and environment."

        return msg
