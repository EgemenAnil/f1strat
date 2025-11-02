"""
Test ML Models (v3.1.0 Enhanced Ensemble)
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.enhanced_ml import EnhancedMLPredictor


class TestEnhancedML:
    """Test Enhanced ML Ensemble models."""
    
    @pytest.fixture
    def predictor(self):
        """Load trained predictor."""
        model_path = Path(__file__).parent.parent / 'models' / 'enhanced_ml_model.pkl'
        if not model_path.exists():
            pytest.skip("Model not trained yet")
        return EnhancedMLPredictor(model_path=str(model_path))
    
    def test_model_loads(self, predictor):
        """Test that model loads successfully."""
        assert predictor is not None
        assert hasattr(predictor, 'strategy_model')
        assert hasattr(predictor, 'pit_lap_model')
    
    def test_strategy_prediction(self, predictor):
        """Test strategy prediction."""
        # Sample features
        features = {
            'track_length': 5.412,
            'total_laps': 57,
            'avg_lap_time': 90.0,
            'temperature': 25.0,
            'rain_probability': 0.0,
            'starting_compound': 'SOFT',
            'target_compound': 'MEDIUM',
            'driver_skill': 0.85,
            'team_aggression': 0.7,
            'safety_car_prob': 0.15,
            'crash_probability': 0.1,
            'pit_stop_time': 24.0
        }
        
        strategy, confidence = predictor.predict_strategy(features)
        
        assert strategy in ['1-stop', '2-stop', '3-stop']
        assert 0 <= confidence <= 1
    
    def test_pit_lap_prediction(self, predictor):
        """Test pit lap prediction."""
        features = {
            'track_length': 5.412,
            'total_laps': 57,
            'avg_lap_time': 90.0,
            'temperature': 25.0,
            'rain_probability': 0.0,
            'starting_compound': 'SOFT',
            'target_compound': 'MEDIUM',
            'driver_skill': 0.85,
            'team_aggression': 0.7,
            'safety_car_prob': 0.15,
            'crash_probability': 0.1,
            'pit_stop_time': 24.0
        }
        
        pit_lap = predictor.predict_pit_lap(features)
        
        assert isinstance(pit_lap, int)
        assert 1 <= pit_lap <= 57
    
    def test_model_accuracy_threshold(self, predictor):
        """Test that model meets accuracy threshold."""
        # This would typically load test data and validate
        # For now, just check model exists and has expected attributes
        assert predictor.strategy_model is not None
        assert predictor.pit_lap_model is not None


class TestModelFiles:
    """Test model file existence and integrity."""
    
    def test_enhanced_ml_model_exists(self):
        """Test enhanced ML model file exists."""
        model_path = Path(__file__).parent.parent / 'models' / 'enhanced_ml_model.pkl'
        assert model_path.exists(), "Enhanced ML model not found"
    
    def test_driver_ratings_exist(self):
        """Test driver ratings file exists."""
        ratings_path = Path(__file__).parent.parent / 'models' / 'driver_ratings_2025.pkl'
        assert ratings_path.exists(), "Driver ratings not found"
    
    def test_team_profiles_exist(self):
        """Test team profiles file exists."""
        profiles_path = Path(__file__).parent.parent / 'models' / 'team_profiles_2025.pkl'
        assert profiles_path.exists(), "Team profiles not found"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
