"""
Machine Learning Strategy Predictor
Uses historical F1 data (2023-2025) to predict optimal pit strategies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, mean_absolute_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️  scikit-learn not available. ML features disabled.")

import fastf1


class MLStrategyPredictor:
    """
    Machine Learning based F1 strategy predictor.
    Trained on 2023-2025 race data.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize ML predictor."""
        self.model_path = model_path or "./models/ml_strategy_model.pkl"
        
        # Models
        self.strategy_classifier = None  # 1-stop vs 2-stop vs 3-stop
        self.pit_lap_regressor = None    # Optimal pit lap prediction
        self.scaler = StandardScaler()
        
        # Feature names for consistency
        self.feature_names = [
            # Track features
            'total_laps',
            'avg_lap_time',
            'track_length',
            'track_type_street',
            'track_type_road',
            'track_type_mixed',
            
            # Weather features
            'temperature',
            'humidity',
            'rain_probability',
            
            # Historical features
            'historical_avg_stops',
            'safety_car_probability',
            'overtaking_difficulty',
            
            # Practice features (if available)
            'practice_soft_deg',
            'practice_medium_deg',
            'practice_hard_deg',
        ]
        
        # Load pre-trained model if exists
        if Path(self.model_path).exists():
            self.load_model()
    
    def prepare_features(self, race_context: Dict) -> np.ndarray:
        """
        Prepare feature vector from race context.
        
        Args:
            race_context: Dictionary with race information
            
        Returns:
            Feature vector as numpy array
        """
        features = []
        
        # Track features
        features.append(race_context.get('total_laps', 57))
        features.append(race_context.get('avg_lap_time', 90.0))
        features.append(race_context.get('circuit_length', 5.0))
        
        # Track type (one-hot encoding)
        track_type = race_context.get('track_type', 'road')
        features.append(1 if track_type == 'street' else 0)
        features.append(1 if track_type == 'road' else 0)
        features.append(1 if track_type == 'mixed' else 0)
        
        # Weather features
        weather = race_context.get('weather', {})
        features.append(weather.get('temperature', 25.0))
        features.append(weather.get('humidity', 50.0))
        features.append(weather.get('rain_probability', 0.0))
        
        # Historical features
        features.append(race_context.get('historical_avg_stops', 1.5))
        features.append(race_context.get('safety_car_prob', 0.3))
        features.append(race_context.get('overtaking_difficulty', 0.5))
        
        # Practice features
        practice = race_context.get('practice', {})
        practice_deg = practice.get('tire_degradation', {})
        
        features.append(practice_deg.get('SOFT', {}).get('avg_degradation', 0.05))
        features.append(practice_deg.get('MEDIUM', {}).get('avg_degradation', 0.03))
        features.append(practice_deg.get('HARD', {}).get('avg_degradation', 0.02))
        
        return np.array(features).reshape(1, -1)
    
    def extract_race_features_and_labels(self, year: int, race_name: str) -> Optional[Tuple[np.ndarray, Dict]]:
        """
        Extract features and actual strategy (labels) from a completed race.
        
        Args:
            year: Season year
            race_name: Race name or location
            
        Returns:
            Tuple of (features, labels) or None if data unavailable
        """
        try:
            # Load race session
            session = fastf1.get_session(year, race_name, 'R')
            session.load()
            
            laps = session.laps
            
            if laps is None or len(laps) == 0:
                return None
            
            # Extract features
            features_dict = {
                'total_laps': len(laps['LapNumber'].unique()),
                'avg_lap_time': laps['LapTime'].mean().total_seconds() if 'LapTime' in laps.columns else 90.0,
                'circuit_length': 5.0,  # Default
                'track_type': 'road',
                'temperature': 25.0,
                'humidity': 50.0,
                'rain_probability': 0.0,
                'historical_avg_stops': 1.5,
                'safety_car_prob': 0.3,
                'overtaking_difficulty': 0.5,
                'practice_soft_deg': 0.05,
                'practice_medium_deg': 0.03,
                'practice_hard_deg': 0.02,
            }
            
            # Extract actual strategy (most common strategy used by top 10)
            top_drivers = laps.groupby('Driver').agg({
                'LapNumber': 'count'
            }).nlargest(10, 'LapNumber').index
            
            pit_stops_per_driver = {}
            pit_laps_per_driver = {}
            
            for driver in top_drivers:
                driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
                
                # Count pit stops (compound changes)
                compounds = driver_laps['Compound'].dropna().tolist()
                pit_stops = 0
                pit_laps = []
                
                for i in range(1, len(compounds)):
                    if compounds[i] != compounds[i-1]:
                        pit_stops += 1
                        pit_laps.append(driver_laps.iloc[i]['LapNumber'])
                
                pit_stops_per_driver[driver] = pit_stops
                pit_laps_per_driver[driver] = pit_laps
            
            # Most common strategy
            if pit_stops_per_driver:
                most_common_stops = max(set(pit_stops_per_driver.values()), 
                                       key=list(pit_stops_per_driver.values()).count)
                
                # Average pit lap for most common strategy
                avg_pit_lap = 0
                pit_lap_samples = []
                for driver, stops in pit_stops_per_driver.items():
                    if stops == most_common_stops and pit_laps_per_driver[driver]:
                        pit_lap_samples.append(pit_laps_per_driver[driver][0])
                
                if pit_lap_samples:
                    avg_pit_lap = int(np.mean(pit_lap_samples))
            else:
                most_common_stops = 1
                avg_pit_lap = 20
            
            labels = {
                'strategy_type': most_common_stops,
                'first_pit_lap': avg_pit_lap
            }
            
            features = self.prepare_features(features_dict)
            
            return features, labels
            
        except Exception as e:
            print(f"⚠️  Error extracting data from {year} {race_name}: {e}")
            return None
    
    def collect_training_data(self, years: List[int] = [2023, 2024, 2025]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Collect training data from multiple seasons.
        
        Args:
            years: List of years to collect data from
            
        Returns:
            Tuple of (X_strategy, y_strategy, y_pit_lap)
        """
        print(f"\n📚 Collecting training data from {years}...")
        
        X_list = []
        y_strategy_list = []
        y_pit_lap_list = []
        
        for year in years:
            try:
                schedule = fastf1.get_event_schedule(year)
                
                # Get completed races
                if year == 2025:
                    # Only use completed 2025 races
                    today = pd.Timestamp.now()
                    races = schedule[schedule['EventDate'] < today]
                else:
                    # Use all races from past years
                    races = schedule
                
                print(f"\n  {year} Season: {len(races)} races")
                
                for idx, race in races.iterrows():
                    race_name = race['EventName']
                    
                    # Skip pre-season testing
                    if 'Testing' in race_name or 'Pre-Season' in race_name:
                        continue
                    
                    try:
                        result = self.extract_race_features_and_labels(year, race_name)
                        
                        if result:
                            features, labels = result
                            X_list.append(features.flatten())
                            y_strategy_list.append(labels['strategy_type'])
                            y_pit_lap_list.append(labels['first_pit_lap'])
                            print(f"    ✅ {race_name:30s} - {labels['strategy_type']}-stop, pit lap {labels['first_pit_lap']}")
                        else:
                            print(f"    ⚠️  {race_name:30s} - No data")
                    
                    except Exception as e:
                        print(f"    ❌ {race_name:30s} - Error: {e}")
                        continue
            
            except Exception as e:
                print(f"  Error loading {year} schedule: {e}")
                continue
        
        if len(X_list) == 0:
            raise ValueError("No training data collected!")
        
        X = np.array(X_list)
        y_strategy = np.array(y_strategy_list)
        y_pit_lap = np.array(y_pit_lap_list)
        
        print(f"\n✅ Training data collected:")
        print(f"   Total samples: {len(X)}")
        print(f"   Features: {X.shape[1]}")
        print(f"   Strategy distribution: {np.bincount(y_strategy)}")
        
        return X, y_strategy, y_pit_lap
    
    def train(self, years: List[int] = [2023, 2024, 2025], save_model: bool = True):
        """
        Train ML models on historical data.
        
        Args:
            years: Years to include in training
            save_model: Whether to save trained model
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for training. Install with: pip install scikit-learn")
        
        print("🤖 TRAINING ML STRATEGY PREDICTOR")
        print("="*80)
        
        # Collect training data
        X, y_strategy, y_pit_lap = self.collect_training_data(years)
        
        # Scale features
        print("\n📊 Scaling features...")
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_strat_train, y_strat_test, y_pit_train, y_pit_test = train_test_split(
            X_scaled, y_strategy, y_pit_lap, test_size=0.2, random_state=42
        )
        
        # Train strategy classifier (1-stop vs 2-stop vs 3-stop)
        print("\n🎯 Training strategy classifier...")
        self.strategy_classifier = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.strategy_classifier.fit(X_train, y_strat_train)
        
        # Evaluate
        train_acc = accuracy_score(y_strat_train, self.strategy_classifier.predict(X_train))
        test_acc = accuracy_score(y_strat_test, self.strategy_classifier.predict(X_test))
        
        print(f"   Training accuracy: {train_acc*100:.1f}%")
        print(f"   Test accuracy: {test_acc*100:.1f}%")
        
        # Cross-validation
        cv_scores = cross_val_score(self.strategy_classifier, X_scaled, y_strategy, cv=5)
        print(f"   Cross-validation: {cv_scores.mean()*100:.1f}% (±{cv_scores.std()*100:.1f}%)")
        
        # Train pit lap regressor
        print("\n⏱️  Training pit lap predictor...")
        self.pit_lap_regressor = GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.pit_lap_regressor.fit(X_train, y_pit_train)
        
        # Evaluate
        train_mae = mean_absolute_error(y_pit_train, self.pit_lap_regressor.predict(X_train))
        test_mae = mean_absolute_error(y_pit_test, self.pit_lap_regressor.predict(X_test))
        
        print(f"   Training MAE: {train_mae:.1f} laps")
        print(f"   Test MAE: {test_mae:.1f} laps")
        
        # Feature importance
        print("\n📈 Feature Importance (Top 5):")
        importances = self.strategy_classifier.feature_importances_
        indices = np.argsort(importances)[::-1][:5]
        
        for i, idx in enumerate(indices):
            if idx < len(self.feature_names):
                print(f"   {i+1}. {self.feature_names[idx]:25s} {importances[idx]:.3f}")
        
        # Save model
        if save_model:
            self.save_model()
        
        print("\n" + "="*80)
        print("✅ ML model training complete!")
        print(f"   Strategy prediction accuracy: {test_acc*100:.1f}%")
        print(f"   Pit lap prediction error: ±{test_mae:.1f} laps")
    
    def predict(self, race_context: Dict) -> Dict:
        """
        Predict optimal strategy using trained ML model.
        
        Args:
            race_context: Dictionary with race information
            
        Returns:
            Prediction dictionary with strategy and confidence
        """
        if self.strategy_classifier is None or self.pit_lap_regressor is None:
            raise ValueError("Model not trained! Call train() first or load pre-trained model.")
        
        # Prepare features
        X = self.prepare_features(race_context)
        X_scaled = self.scaler.transform(X)
        
        # Predict strategy type
        strategy_type = self.strategy_classifier.predict(X_scaled)[0]
        strategy_proba = self.strategy_classifier.predict_proba(X_scaled)[0]
        confidence = max(strategy_proba)
        
        # Predict pit lap
        pit_lap = int(self.pit_lap_regressor.predict(X_scaled)[0])
        
        return {
            'strategy_type': int(strategy_type),  # 1, 2, or 3 stops
            'confidence': float(confidence),
            'pit_lap': pit_lap,
            'probabilities': {
                '1-stop': float(strategy_proba[0]) if len(strategy_proba) > 0 else 0.0,
                '2-stop': float(strategy_proba[1]) if len(strategy_proba) > 1 else 0.0,
                '3-stop': float(strategy_proba[2]) if len(strategy_proba) > 2 else 0.0,
            }
        }
    
    def save_model(self):
        """Save trained model to disk."""
        model_dir = Path(self.model_path).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'strategy_classifier': self.strategy_classifier,
            'pit_lap_regressor': self.pit_lap_regressor,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'training_date': datetime.now().isoformat(),
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Model saved to: {self.model_path}")
    
    def load_model(self):
        """Load pre-trained model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.strategy_classifier = model_data['strategy_classifier']
            self.pit_lap_regressor = model_data['pit_lap_regressor']
            self.scaler = model_data['scaler']
            self.feature_names = model_data['feature_names']
            
            training_date = model_data.get('training_date', 'Unknown')
            print(f"✅ Model loaded from: {self.model_path}")
            print(f"   Training date: {training_date}")
            
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")


if __name__ == "__main__":
    """
    Train ML model on historical data.
    """
    print("🤖 F1 ML Strategy Predictor - Training Script")
    print("="*80)
    
    # Initialize predictor
    predictor = MLStrategyPredictor()
    
    # Train model
    predictor.train(years=[2023, 2024, 2025], save_model=True)
    
    # Test prediction
    print("\n" + "="*80)
    print("🧪 TESTING PREDICTION")
    
    test_context = {
        'total_laps': 57,
        'avg_lap_time': 90.0,
        'circuit_length': 5.0,
        'track_type': 'road',
        'weather': {
            'temperature': 29.0,
            'humidity': 47.0,
            'rain_probability': 30.0
        },
        'historical_avg_stops': 1.5,
        'safety_car_prob': 0.3,
        'overtaking_difficulty': 0.5,
    }
    
    prediction = predictor.predict(test_context)
    
    print(f"\n📊 Test Prediction:")
    print(f"   Strategy: {prediction['strategy_type']}-stop")
    print(f"   Confidence: {prediction['confidence']*100:.1f}%")
    print(f"   Pit lap: {prediction['pit_lap']}")
    print(f"   Probabilities:")
    for strategy, prob in prediction['probabilities'].items():
        print(f"      {strategy}: {prob*100:.1f}%")
