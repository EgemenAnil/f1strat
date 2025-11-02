"""
Quick test script for F1 Race Prediction System
Tests all major components without requiring full data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.features.engineering import F1FeatureEngineer
        print("  ✓ Feature engineering module")
    except Exception as e:
        print(f"  ✗ Feature engineering: {e}")
    
    try:
        from src.features.track_features import TrackFeatures
        print("  ✓ Track features module")
    except Exception as e:
        print(f"  ✗ Track features: {e}")
    
    try:
        from src.models.strategy_optimizer import StrategyOptimizer
        print("  ✓ Strategy optimizer module")
    except Exception as e:
        print(f"  ✗ Strategy optimizer: {e}")
    
    try:
        from src.models.crash_predictor import CrashPredictor
        print("  ✓ Crash predictor module")
    except Exception as e:
        print(f"  ✗ Crash predictor: {e}")
    
    print()


def test_track_features():
    """Test track features."""
    print("Testing track features...")
    
    from src.features.track_features import TrackFeatures
    
    # Test track info retrieval
    bahrain = TrackFeatures.get_track_info('Bahrain')
    if bahrain:
        print(f"  ✓ Bahrain track data: {bahrain['length_km']} km, {bahrain['corners']} corners")
    
    monaco = TrackFeatures.get_track_info('Monaco')
    if monaco:
        print(f"  ✓ Monaco track data: Overtaking difficulty {monaco['overtaking_difficulty']:.0%}")
    
    # Test optimal compounds
    compounds = TrackFeatures.get_optimal_compounds('Bahrain')
    print(f"  ✓ Bahrain optimal compounds: {compounds}")
    
    print()


def test_feature_engineering():
    """Test feature engineering."""
    print("Testing feature engineering...")
    
    import pandas as pd
    from src.features.engineering import F1FeatureEngineer
    
    # Create sample data
    sample_df = pd.DataFrame({
        'LapNumber': range(1, 11),
        'Stint': [1] * 10,
        'TyreLife': range(1, 11),
        'Compound': ['SOFT'] * 10,
        'AirTemp': [25] * 10,
        'TrackTemp': [35] * 10,
        'Rainfall': [0] * 10,
        'Position': [5] * 10,
    })
    
    engineer = F1FeatureEngineer()
    
    # Test individual feature creation
    df = engineer.create_basic_features(sample_df.copy())
    print(f"  ✓ Basic features: {len(df.columns)} columns")
    
    df = engineer.create_weather_features(sample_df.copy())
    print(f"  ✓ Weather features created")
    
    df = engineer.create_fuel_features(sample_df.copy(), total_laps=57)
    print(f"  ✓ Fuel features created")
    
    df = engineer.create_tire_degradation_features(sample_df.copy())
    print(f"  ✓ Tire degradation features created")
    
    # Test all features
    df_all = engineer.create_all_features(sample_df.copy(), total_laps=57)
    print(f"  ✓ All features: {len(df_all.columns)} total columns")
    
    print()


def test_crash_predictor():
    """Test crash prediction."""
    print("Testing crash predictor...")
    
    from src.models.crash_predictor import CrashPredictor
    
    predictor = CrashPredictor()
    
    # Test track risk analysis
    monaco_risk = predictor.analyze_track_risk('Monaco')
    print(f"  ✓ Monaco risk: {monaco_risk['risk_category']} ({monaco_risk['incident_rate']:.0%})")
    
    bahrain_risk = predictor.analyze_track_risk('Bahrain')
    print(f"  ✓ Bahrain risk: {bahrain_risk['risk_category']} ({bahrain_risk['incident_rate']:.0%})")
    
    # Test lap-specific incident probability
    weather = {'temperature': 25, 'rain_probability': 0.1}
    lap_prob = predictor.calculate_lap_incident_probability(
        lap_number=1,
        total_laps=57,
        weather=weather,
        track_name='Monaco'
    )
    print(f"  ✓ Lap 1 incident probability: {lap_prob['total']:.1%}")
    
    print()


def test_strategy_optimizer():
    """Test strategy optimization."""
    print("Testing strategy optimizer...")
    
    from src.models.strategy_optimizer import StrategyOptimizer
    
    optimizer = StrategyOptimizer(total_laps=57)
    
    # Test strategy generation
    weather = {
        'temperature': 25,
        'rain_probability': 0.2,
        'humidity': 60
    }
    
    strategies = optimizer.generate_strategies(weather)
    print(f"  ✓ Generated {len(strategies)} viable strategies")
    
    # Test strategy simulation
    if strategies:
        test_strategy = strategies[0]
        total_time, results = optimizer.simulate_strategy(
            test_strategy,
            weather_forecast=weather,
            track_name='Bahrain'
        )
        print(f"  ✓ Simulated strategy: {test_strategy.name}")
        print(f"    Expected time: {total_time:.1f}s")
        print(f"    Avg lap time: {results['avg_lap_time']:.3f}s")
    
    print()


def test_full_pipeline():
    """Test complete prediction pipeline."""
    print("Testing full pipeline (without API calls)...")
    
    try:
        from predict_race import F1RacePredictionPipeline
        
        pipeline = F1RacePredictionPipeline()
        print("  ✓ Pipeline initialized")
        
        # Test would require API key and network access
        print("  ℹ Full prediction requires API key and network access")
        print("  ℹ Run: python predict_race.py")
        
    except Exception as e:
        print(f"  ✗ Pipeline test failed: {e}")
    
    print()


def main():
    """Run all tests."""
    print("=" * 80)
    print("F1 RACE PREDICTION SYSTEM - COMPONENT TESTS")
    print("=" * 80)
    print()
    
    test_imports()
    test_track_features()
    test_feature_engineering()
    test_crash_predictor()
    test_strategy_optimizer()
    test_full_pipeline()
    
    print("=" * 80)
    print("TESTS COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Set up .env file with OpenWeatherMap API key")
    print("2. Run: python predict_race.py")
    print()


if __name__ == "__main__":
    main()
