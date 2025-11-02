"""
Train v3.0 Features - Driver Ratings & Team Profiles
Generates 2025 season-based driver and team data
"""

import sys
import warnings
warnings.filterwarnings('ignore')

print("🏎️  F1 Strategy Prediction v3.0 - Feature Training\n")
print("="*80)

# Train Driver Performance Ratings
print("\n1️⃣  DRIVER PERFORMANCE ANALYSIS")
print("="*80)

try:
    from src.models.driver_performance import DriverPerformanceAnalyzer
    
    print("\n📊 Analyzing 2025 driver performance...")
    driver_analyzer = DriverPerformanceAnalyzer()
    
    # Analyze first 10 races (for speed)
    ratings = driver_analyzer.analyze_2025_season(max_races=10)
    
    if ratings:
        print(f"\n✅ Generated ratings for {len(ratings)} drivers")
        
        # Show top 5
        top_5 = driver_analyzer.get_top_drivers(5, 'overall')
        print("\n🏆 Top 5 Drivers:")
        for i, (driver, rating) in enumerate(top_5, 1):
            print(f"   {i}. {driver}: {rating['overall']:.1f}/100 "
                  f"(Tire: {rating['tire_management']:.1f}, "
                  f"Pace: {rating['pace']:.1f})")
        
        # Save
        driver_analyzer.save_ratings()
    else:
        print("⚠️  No driver ratings generated (data may not be available)")
        
except Exception as e:
    print(f"❌ Driver analysis failed: {e}")
    print("   Continuing with team profiles...")

# Train Team Strategy Profiles
print("\n\n2️⃣  TEAM STRATEGY ANALYSIS")
print("="*80)

try:
    from src.models.team_strategy_profiles import TeamStrategyAnalyzer
    
    print("\n🏁 Analyzing 2025 team strategies...")
    team_analyzer = TeamStrategyAnalyzer()
    
    # Analyze first 10 races (for speed)
    profiles = team_analyzer.analyze_2025_season(max_races=10)
    
    if profiles:
        print(f"\n✅ Generated profiles for {len(profiles)} teams")
        
        # Show summary
        print("\n📊 Team Summary:")
        for team, profile in sorted(profiles.items())[:5]:
            print(f"   {team}:")
            print(f"      Style: {profile['style']}")
            print(f"      Avg Stops: {profile['avg_pit_stops']}")
            print(f"      Pit Duration: {profile['avg_pit_duration']:.2f}s")
        
        # Save
        team_analyzer.save_profiles()
    else:
        print("⚠️  No team profiles generated (data may not be available)")
        
except Exception as e:
    print(f"❌ Team analysis failed: {e}")
    print("   Continuing...")

# Advanced ML (optional - requires PyTorch)
print("\n\n3️⃣  ADVANCED ML (LSTM)")
print("="*80)

try:
    from src.models.advanced_ml import AdvancedMLPredictor, PYTORCH_AVAILABLE
    
    if PYTORCH_AVAILABLE:
        print("\n🧠 Training LSTM neural network...")
        
        predictor = AdvancedMLPredictor()
        
        # Create training data
        from src.models.advanced_ml import create_training_data_from_fast_ml
        training_data = create_training_data_from_fast_ml()
        
        print(f"   Training samples: {len(training_data)}")
        
        # Train (quick version - 20 epochs)
        predictor.train(training_data, epochs=20, batch_size=8)
        
        # Test
        test_context = {
            'total_laps': 57,
            'lap_time': 90,
            'weather': {'temperature': 29, 'rain_probability': 30},
            'track_type': 'road'
        }
        pred = predictor.predict(test_context)
        print(f"\n   Test prediction: {pred['strategy_type']}-stop, lap {pred['pit_lap']}")
        
        # Save
        predictor.save()
        print("   ✅ LSTM model saved")
        
    else:
        print("\n⚠️  PyTorch not installed - LSTM features disabled")
        print("   Install with: pip install torch")
        print("   System will use RandomForest ML instead")
        
except Exception as e:
    print(f"❌ Advanced ML training failed: {e}")
    print("   System will use RandomForest ML as fallback")

# Summary
print("\n\n" + "="*80)
print("📋 TRAINING SUMMARY")
print("="*80)

import os

print("\n✅ Generated Models:")
if os.path.exists('./models/driver_ratings_2025.pkl'):
    print("   ✓ Driver Performance Ratings (2025)")
else:
    print("   ✗ Driver Performance Ratings (not available)")

if os.path.exists('./models/team_profiles_2025.pkl'):
    print("   ✓ Team Strategy Profiles (2025)")
else:
    print("   ✗ Team Strategy Profiles (not available)")

if os.path.exists('./models/fast_ml_model.pkl'):
    print("   ✓ ML Strategy Predictor (RandomForest)")
else:
    print("   ✗ ML Strategy Predictor (not trained)")

if os.path.exists('./models/advanced_ml_model.pkl'):
    print("   ✓ Advanced ML (LSTM)")
else:
    print("   ✗ Advanced ML (not available - requires PyTorch)")

print("\n💡 Usage:")
print("   Run: python predict_upcoming_race.py")
print("   System will automatically use available features")

print("\n" + "="*80)
print("✅ v3.0 Feature training complete!")
print("="*80)
