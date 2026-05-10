import numpy as np
import pandas as pd
import os
import joblib
import logging
import warnings
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

FEATURE_COLS = [
    'ph', 'Hardness', 'Solids', 'Chloramines',
    'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'
]
TARGET_COL = 'Potability'

SAFE_RANGES = {
    'ph':              (6.5, 8.5),
    'Hardness':        (0,   300),
    'Solids':          (0,   500),
    'Chloramines':     (0,   4.0),
    'Sulfate':         (0,   250),
    'Conductivity':    (0,   400),
    'Organic_carbon':  (0,   2.0),
    'Trihalomethanes': (0,   80),
    'Turbidity':       (0,   4.0),
}


class WaterQualityModel:
    def __init__(self, retrain=False):
        self.model        = None
        self.scaler       = RobustScaler()  # More robust to outliers
        self.imputer      = SimpleImputer(strategy='median')
        self.model_path   = os.path.join(os.path.dirname(__file__), 'water_quality_model.pkl')
        self.scaler_path  = os.path.join(os.path.dirname(__file__), 'water_quality_scaler.pkl')
        self.imputer_path = os.path.join(os.path.dirname(__file__), 'water_quality_imputer.pkl')
        self.test_path    = os.path.join(os.path.dirname(__file__), 'water_quality_test.pkl')
        self.dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'water_potability.csv')

        if os.path.exists(self.model_path) and not retrain:
            self._load()
            logger.info("✅ Water quality model loaded from disk")
            self._print_report()
        else:
            logger.info("🔄 Training water quality model from local dataset...")
            self._train()
            self._save()
            logger.info("✅ Water quality model trained and saved")

    def _train(self):
        if not os.path.exists(self.dataset_path):
            raise RuntimeError(f"Dataset not found at {self.dataset_path}")

        df = pd.read_csv(self.dataset_path)
        logger.info(f"✅ Loaded {len(df)} rows from water_potability.csv")

        X = df[FEATURE_COLS].values
        y = df[TARGET_COL].values
        logger.info(f"📊 Potable: {(y==1).sum()}, Not Potable: {(y==0).sum()}")

        # Impute and scale
        X = self.imputer.fit_transform(X)
        
        # Feature engineering - add interaction features
        X_engineered = self._engineer_features(X)
        X_scaled = self.scaler.fit_transform(X_engineered)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        # Apply SMOTE for class balancing
        logger.info("🔄 Applying SMOTE for class balancing...")
        smote = SMOTE(random_state=42, k_neighbors=3)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        logger.info(f"✅ Balanced training set: {len(X_train)} → {len(X_train_balanced)} samples")

        # Optimized ensemble - faster training, still high accuracy
        xgb_model = XGBClassifier(
            n_estimators=150, learning_rate=0.05, max_depth=7,
            subsample=0.85, colsample_bytree=0.85,
            random_state=42, n_jobs=-1, eval_metric='logloss'
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=150, learning_rate=0.05, max_depth=7,
            min_samples_split=3, subsample=0.85,
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

        # Store test data for later evaluation
        joblib.dump((X_test, y_test), self.test_path)
        
        # Print report after training
        y_pred = self.model.predict(X_test)
        acc    = accuracy_score(y_test, y_pred)
        f1     = f1_score(y_test, y_pred, average='weighted')
        report = classification_report(y_test, y_pred, target_names=['Not Potable', 'Potable'])
        logger.info(f"📈 Water quality model accuracy: {acc:.3f}, F1: {f1:.3f}")
        print(f"\n=== Water Quality Model Classification Report ===\n{report}")
    
    def _engineer_features(self, X):
        """Add engineered features for better prediction"""
        # X has 9 features: ph, Hardness, Solids, Chloramines, Sulfate, 
        #                   Conductivity, Organic_carbon, Trihalomethanes, Turbidity
        
        ph = X[:, 0]
        hardness = X[:, 1]
        solids = X[:, 2]
        chloramines = X[:, 3]
        sulfate = X[:, 4]
        conductivity = X[:, 5]
        organic_carbon = X[:, 6]
        trihalomethanes = X[:, 7]
        turbidity = X[:, 8]
        
        # Engineered features
        ph_deviation = np.abs(ph - 7.0)  # Deviation from neutral pH
        hardness_category = (hardness > 200).astype(float)  # Hard water indicator
        high_solids = (solids > 400).astype(float)  # High dissolved solids
        contamination_score = (
            (chloramines > 3) * 2 +
            (trihalomethanes > 60) * 2 +
            (turbidity > 3) * 1.5 +
            (organic_carbon > 1.5) * 1.5
        )
        
        # Interaction features
        ph_turbidity = ph * turbidity
        conductivity_solids = conductivity * solids / 1000
        
        # Stack all features
        X_engineered = np.column_stack([
            X,  # Original 9 features
            ph_deviation,
            hardness_category,
            high_solids,
            contamination_score,
            ph_turbidity,
            conductivity_solids
        ])
        
        return X_engineered

    def _print_report(self):
        try:
            # Try to load stored test data first
            if os.path.exists(self.test_path):
                X_test, y_test = joblib.load(self.test_path)
            else:
                # If test data doesn't exist, regenerate from dataset
                logger.info("Test data not found, regenerating from dataset...")
                df = pd.read_csv(self.dataset_path)
                X = self.imputer.transform(df[FEATURE_COLS].values)
                X_engineered = self._engineer_features(X)
                X_scaled = self.scaler.transform(X_engineered)
                y = df[TARGET_COL].values
                _, X_test, _, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
            
            y_pred = self.model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            report = classification_report(y_test, y_pred, target_names=['Not Potable', 'Potable'])
            print(f"\n=== Water Quality Model Classification Report ===")
            print(f"Accuracy: {acc:.3f}, F1-Score: {f1:.3f}")
            print(report)
        except Exception as e:
            logger.warning(f"Could not print classification report: {e}")

    def _save(self):
        joblib.dump(self.model,   self.model_path)
        joblib.dump(self.scaler,  self.scaler_path)
        joblib.dump(self.imputer, self.imputer_path)

    def _load(self):
        self.model   = joblib.load(self.model_path)
        self.scaler  = joblib.load(self.scaler_path)
        self.imputer = joblib.load(self.imputer_path)

    def predict(self, inputs: dict) -> dict:
        """
        inputs: dict with keys matching FEATURE_COLS (missing values are imputed).

        Expected keys (all optional):
            ph, Hardness, Solids, Chloramines, Sulfate,
            Conductivity, Organic_carbon, Trihalomethanes, Turbidity

        Returns:
            { potable, potabilityScore, waterRiskScore, violations, explanation }
        """
        try:
            row     = [inputs.get(col, np.nan) for col in FEATURE_COLS]
            X       = np.array([row], dtype=float)
            X       = self.imputer.transform(X)
            
            # Apply feature engineering
            X_engineered = self._engineer_features(X)
            X_scaled = self.scaler.transform(X_engineered)

            proba            = self.model.predict_proba(X_scaled)[0]
            potability_score = round(float(proba[1]) * 100, 1)

            violations = []
            for col, (lo, hi) in SAFE_RANGES.items():
                val = inputs.get(col)
                if val is not None:
                    fval = float(val)
                    if not np.isnan(fval) and (fval < lo or fval > hi):
                        violations.append(f"{col} ({fval:.2f} outside {lo}–{hi})")

            potable           = bool((len(violations) == 0) and (proba[1] >= 0.5))
            violation_penalty = min(len(violations) * 0.08, 0.5)
            water_risk        = round(min((1.0 - float(proba[1])) + violation_penalty, 1.0), 3)

            return {
                'potable':         potable,
                'potabilityScore': potability_score,
                'waterRiskScore':  water_risk,
                'violations':      violations,
                'explanation':     self._explain(potable, potability_score, violations),
            }
        except Exception as e:
            logger.error(f"Water quality prediction error: {e}")
            return {
                'potable':         None,
                'potabilityScore': 50.0,
                'waterRiskScore':  0.5,
                'violations':      [],
                'explanation':     f'Could not assess water quality: {e}',
            }

    def _explain(self, potable, score, violations):
        status = "POTABLE" if potable else "NOT POTABLE"
        msg    = f"Water is {status} (potability score: {score}%). "
        if violations:
            msg += f"Parameters out of safe range: {', '.join(violations)}. "
        else:
            msg += "All measured parameters are within safe limits. "
        if not potable:
            msg += "Contaminated water significantly increases waterborne disease risk."
        return msg
