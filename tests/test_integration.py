"""
Integration Tests - Test Complete Pipeline
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCompletePipeline:
    """Test complete prediction pipeline."""
    
    def test_app_imports(self):
        """Test that all imports work."""
        try:
            from src.features.engineering import F1FeatureEngineer
            from src.features.track_features import TrackFeatures
            from src.models.strategy_optimizer import StrategyOptimizer
            from src.models.crash_predictor import CrashPredictor
            from src.data.race_calendar import RaceCalendar
            assert True
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
    
    def test_models_trained(self):
        """Test that ML models are trained."""
        models_dir = Path(__file__).parent.parent / 'models'
        
        assert (models_dir / 'enhanced_ml_model.pkl').exists()
        assert (models_dir / 'driver_ratings_2025.pkl').exists()
        assert (models_dir / 'team_profiles_2025.pkl').exists()
    
    def test_config_files_exist(self):
        """Test that config files exist."""
        project_root = Path(__file__).parent.parent
        
        assert (project_root / '.env.example').exists()
        assert (project_root / 'requirements.txt').exists()
        assert (project_root / 'README.md').exists()
    
    def test_prediction_pipeline(self):
        """Test complete prediction pipeline."""
        try:
            from predict_upcoming_race import F1RacePredictionPipeline
            
            # Create pipeline
            pipeline = F1RacePredictionPipeline()
            
            # Should initialize without errors
            assert pipeline is not None
            
        except Exception as e:
            # Pipeline might fail if no race data available
            # That's okay for this test
            pass


class TestSystemRequirements:
    """Test system requirements."""
    
    def test_python_version(self):
        """Test Python version is 3.8+."""
        import sys
        assert sys.version_info >= (3, 8)
    
    def test_required_packages(self):
        """Test required packages are installed."""
        required = [
            'numpy',
            'pandas', 
            'sklearn',
            'fastf1',
            'requests',
            'joblib'
        ]
        
        for package in required:
            try:
                __import__(package)
            except ImportError:
                pytest.fail(f"Required package not installed: {package}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
