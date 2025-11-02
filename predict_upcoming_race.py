"""
F1 Race Prediction Pipeline - Standalone version
Predicts upcoming F1 races with optimal pit strategies.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from src.data.fetcher import F1DataFetcher
from src.data.enhanced_services import EnhancedF1DataService
from src.features.engineering import F1FeatureEngineer
from src.features.track_features import TrackFeatures
from src.models.strategy_optimizer import StrategyOptimizer
from src.models.crash_predictor import CrashPredictor

# Try to import ML predictors
try:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from train_enhanced_ml import EnhancedMLPredictor
    ML_AVAILABLE = True
except ImportError:
    try:
        from train_fast_ml import FastMLPredictor
        ML_AVAILABLE = True
    except ImportError:
        ML_AVAILABLE = False
        print("⚠️  ML predictor not available. Using rule-based predictions.")

# Try to import v3.0 features
try:
    from src.models.driver_performance import DriverPerformanceAnalyzer
    from src.models.team_strategy_profiles import TeamStrategyAnalyzer
    V3_FEATURES_AVAILABLE = True
except ImportError:
    V3_FEATURES_AVAILABLE = False

# Try to import advanced ML (LSTM)
try:
    from src.models.advanced_ml import AdvancedMLPredictor, PYTORCH_AVAILABLE
    ADVANCED_ML_AVAILABLE = PYTORCH_AVAILABLE
except ImportError:
    ADVANCED_ML_AVAILABLE = False


class F1RacePredictionPipeline:
    """Complete pipeline for predicting upcoming F1 races with enhanced data and ML."""
    
    def __init__(self, cache_dir: str = './cache', use_ml: bool = True, use_v3: bool = True):
        """Initialize prediction pipeline with v3.0 features."""
        self.cache_dir = cache_dir
        self.fetcher = F1DataFetcher(cache_dir)
        self.enhanced_service = EnhancedF1DataService(cache_dir)
        self.feature_engineer = F1FeatureEngineer()
        self.crash_predictor = CrashPredictor()
        
        # ML Predictor (v3.1 - Enhanced)
        self.ml_predictor = None
        self.use_ml = use_ml and ML_AVAILABLE
        
        if self.use_ml:
            try:
                self.ml_predictor = EnhancedMLPredictor()
                self.ml_predictor.load()
                print("✅ Enhanced ML predictor loaded (v3.1)!")
            except Exception as e:
                try:
                    # Fallback to v2.5
                    from train_fast_ml import FastMLPredictor
                    self.ml_predictor = FastMLPredictor()
                    self.ml_predictor.load()
                    print("✅ ML predictor loaded (v2.5)!")
                except Exception as e2:
                    print(f"⚠️  ML model not found: {e}")
                    print("   Run: python train_enhanced_ml.py")
                    self.use_ml = False
        
        # v3.0 Features
        self.driver_analyzer = None
        self.team_analyzer = None
        self.advanced_ml = None
        self.use_v3 = use_v3 and V3_FEATURES_AVAILABLE
        
        if self.use_v3:
            try:
                # Load driver ratings
                self.driver_analyzer = DriverPerformanceAnalyzer()
                if self.driver_analyzer.load_ratings():
                    print("✅ Driver performance ratings loaded!")
                else:
                    print("⚠️  Driver ratings not found. Run: python train_v3_features.py")
                    self.driver_analyzer = None
                
                # Load team profiles
                self.team_analyzer = TeamStrategyAnalyzer()
                if self.team_analyzer.load_profiles():
                    print("✅ Team strategy profiles loaded!")
                else:
                    print("⚠️  Team profiles not found. Run: python train_v3_features.py")
                    self.team_analyzer = None
                    
            except Exception as e:
                print(f"⚠️  v3.0 features unavailable: {e}")
                self.use_v3 = False
        
        # Advanced ML (LSTM)
        if ADVANCED_ML_AVAILABLE:
            try:
                self.advanced_ml = AdvancedMLPredictor()
                if self.advanced_ml.load():
                    print("✅ Advanced ML (LSTM) loaded!")
            except:
                self.advanced_ml = None
        
        # Track name mapping
        self.track_mapping = {
            'Bahrain': 'Bahrain', 'Saudi Arabia': 'Jeddah',
            'Australia': 'Melbourne', 'Azerbaijan': 'Baku',
            'Miami': 'Miami', 'Monaco': 'Monaco',
            'Spain': 'Catalunya', 'Canada': 'Montreal',
            'Austria': 'Red Bull Ring', 'Great Britain': 'Silverstone',
            'Hungary': 'Hungaroring', 'Belgium': 'Spa',
            'Netherlands': 'Zandvoort', 'Italy': 'Monza',
            'Singapore': 'Singapore', 'Japan': 'Suzuka',
            'Qatar': 'Losail', 'United States': 'Austin',
            'Mexico': 'Mexico City', 'Brazil': 'Interlagos',
            'São Paulo': 'Interlagos', 'Las Vegas': 'Las Vegas',
            'Abu Dhabi': 'Yas Marina'
        }
    
    def get_next_race(self, year: Optional[int] = None) -> Optional[Dict]:
        """Get information about the next upcoming F1 race."""
        try:
            import fastf1
            
            if year is None:
                year = datetime.now().year
            
            schedule = fastf1.get_event_schedule(year)
            today = pd.Timestamp.now()
            
            upcoming_races = schedule[schedule['EventDate'] > today]
            
            if upcoming_races.empty:
                return None
            
            next_race = upcoming_races.iloc[0]
            
            race_info = {
                'race_name': next_race['EventName'],
                'race_date': next_race['EventDate'],
                'location': next_race['Location'],
                'country': next_race['Country'],
                'circuit': next_race.get('Circuit', next_race['Location']),
                'year': year,
                'round': next_race['RoundNumber'],
                'days_until_race': (next_race['EventDate'] - today).days
            }
            
            race_info['track_name'] = self.track_mapping.get(
                race_info['location'], race_info['location']
            )
            
            track_features = TrackFeatures()
            if race_info['track_name'] in track_features.TRACK_DATA:
                track_data = track_features.TRACK_DATA[race_info['track_name']]
                race_info['total_laps'] = track_data.get('total_laps', 57)
                race_info['avg_lap_time'] = track_data.get('base_lap_time', 90.0)
                race_info['circuit_length'] = track_data.get('length_km', 5.0)
            else:
                race_info['total_laps'] = 57
                race_info['avg_lap_time'] = 90.0
                race_info['circuit_length'] = 5.0
            
            return race_info
            
        except Exception as e:
            print(f"Error getting next race: {e}")
            return None
    
    def predict_race_strategies(self, race_info: Dict) -> Dict:
        """Predict optimal strategies for a race with ML enhancement and v3.0 features."""
        try:
            # Get team for pit stop duration (v3.0 feature)
            avg_pit_duration = 24.0  # Default F1 pit stop duration
            team_style = 'balanced'
            
            if self.use_v3 and self.team_analyzer:
                # Get team profile (use first team as example, or could analyze all)
                team_profiles = self.team_analyzer.team_profiles
                if team_profiles:
                    # Average pit duration across all teams
                    durations = [p['avg_pit_duration'] for p in team_profiles.values()]
                    avg_pit_duration = np.mean(durations) if durations else 24.0
                    print(f"   🏁 Avg pit stop duration (2025 data): {avg_pit_duration:.2f}s")
            
            # Get ML prediction if available
            ml_prediction = None
            advanced_ml_prediction = None
            
            # Try advanced ML (LSTM) first
            if self.advanced_ml and self.advanced_ml.is_trained:
                try:
                    advanced_ml_prediction = self.advanced_ml.predict(race_info)
                    print(f"   🧠 Advanced ML (LSTM): {advanced_ml_prediction['strategy_type']}-stop, "
                          f"pit lap {advanced_ml_prediction['pit_lap']} "
                          f"(confidence: {advanced_ml_prediction['confidence']*100:.1f}%)")
                    ml_prediction = advanced_ml_prediction  # Use advanced if available
                except Exception as e:
                    print(f"   ⚠️  Advanced ML failed: {e}")
            
            # Fallback to RandomForest ML
            if ml_prediction is None and self.use_ml and self.ml_predictor:
                try:
                    ml_prediction = self.ml_predictor.predict(race_info)
                    print(f"   🤖 ML Prediction (RF): {ml_prediction['strategy_type']}-stop, "
                          f"pit lap {ml_prediction['pit_lap']} "
                          f"(confidence: {ml_prediction['confidence']*100:.1f}%)")
                except Exception as e:
                    print(f"   ⚠️  ML prediction failed: {e}")
                    ml_prediction = None
            
            # Generate strategies using optimizer
            optimizer = StrategyOptimizer(
                track_name=race_info['track_name'],
                total_laps=race_info['total_laps']
            )
            
            strategies = optimizer.generate_strategies()
            
            if not strategies:
                return {'success': False, 'error': 'No strategies generated'}
            
            # Adjust strategy times with pit stop duration
            for strat in strategies:
                # Add pit stop time loss: number of stops * pit duration
                num_stops = len(strat.pit_laps)
                pit_time_loss = num_stops * avg_pit_duration
                strat.expected_time += pit_time_loss
            
            # Use ML to select optimal strategy if available
            if ml_prediction:
                # Find strategy closest to ML prediction
                ml_target_stops = ml_prediction['strategy_type']
                ml_target_lap = ml_prediction['pit_lap']
                
                best_match = None
                best_score = float('inf')
                
                for strat in strategies:
                    if len(strat.pit_laps) == ml_target_stops:
                        # Score based on pit lap proximity
                        if strat.pit_laps:
                            lap_diff = abs(strat.pit_laps[0] - ml_target_lap)
                            if lap_diff < best_score:
                                best_score = lap_diff
                                best_match = strat
                
                if best_match:
                    optimal_strategy = best_match
                    print(f"   ✅ ML-optimized strategy selected!")
                else:
                    optimal_strategy = strategies[0]
            else:
                optimal_strategy = strategies[0]
            
            strategies_by_stops = {}
            for strat in strategies:
                stop_count = len(strat.pit_laps)
                if stop_count not in strategies_by_stops:
                    strategies_by_stops[stop_count] = []
                strategies_by_stops[stop_count].append(strat)
            
            best_strategies = {'conservative': None, 'balanced': None, 'aggressive': None}
            if 1 in strategies_by_stops:
                best_strategies['conservative'] = strategies_by_stops[1][0]
            if 2 in strategies_by_stops:
                best_strategies['balanced'] = strategies_by_stops[2][0]
            if 3 in strategies_by_stops:
                best_strategies['aggressive'] = strategies_by_stops[3][0]
            
            for level in best_strategies:
                if best_strategies[level] is None:
                    best_strategies[level] = optimal_strategy
            
            crash_prob = {
                'safety_car': self.crash_predictor.calculate_safety_car_probability(
                    total_laps=race_info['total_laps'],
                    track_name=race_info['track_name']
                ),
                'red_flag': 0.1  # Default red flag probability
            }
            
            return {
                'success': True,
                'optimal_strategy': optimal_strategy,
                'strategies_by_risk': best_strategies,
                'all_strategies': strategies[:10],
                'strategies_by_stops': strategies_by_stops,
                'crash_probability': crash_prob,
                'total_strategies_evaluated': len(strategies),
                'ml_prediction': ml_prediction,  # Include ML prediction
                'ml_enhanced': ml_prediction is not None
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def predict_upcoming_race(self, race_name: Optional[str] = None,
                            year: Optional[int] = None,
                            use_enhanced_data: bool = True) -> Optional[Dict]:
        """Complete prediction for upcoming race with enhanced data."""
        try:
            race_info = self.get_next_race(year)
            
            if race_info is None:
                print(f"No upcoming races found for {year or datetime.now().year}")
                return None
            
            print(f"\n🏁 Predicting: {race_info['race_name']}")
            print(f"📍 Location: {race_info['location']}, {race_info['country']}")
            print(f"📅 Date: {race_info['race_date'].strftime('%B %d, %Y')}")
            print(f"⏰ Days until race: {race_info['days_until_race']}")
            print(f"🛣️  Track: {race_info['track_name']}")
            print(f"🔄 Total laps: {race_info['total_laps']}")
            
            # Get enhanced data if enabled
            enhanced_data = None
            if use_enhanced_data:
                print(f"\n� Fetching enhanced race data...")
                try:
                    enhanced_data = self.enhanced_service.get_complete_race_context(
                        year=race_info['year'],
                        race=race_info['location'],
                        race_info=race_info
                    )
                    
                    # Update race_info with enhanced data
                    if enhanced_data.get('weather'):
                        race_info['weather'] = enhanced_data['weather']
                    
                    if enhanced_data.get('qualifying'):
                        race_info['qualifying'] = enhanced_data['qualifying']
                    
                    if enhanced_data.get('practice'):
                        race_info['practice'] = enhanced_data['practice']
                    
                    if enhanced_data.get('tire_allocation'):
                        race_info['tire_allocation'] = enhanced_data['tire_allocation']
                    
                except Exception as e:
                    print(f"⚠️  Enhanced data fetch error (continuing with basic data): {e}")
                    enhanced_data = None
            
            print(f"\n�🔧 Generating optimal strategies...")
            strategy_predictions = self.predict_race_strategies(race_info)
            
            if not strategy_predictions['success']:
                print(f"❌ Strategy prediction failed: {strategy_predictions.get('error')}")
                return None
            
            # Determine model version
            model_version = '2.5.0'  # Base with ML
            if self.use_v3:
                model_version = '3.0.0'  # With driver ratings and team profiles
            if self.advanced_ml and self.advanced_ml.is_trained:
                model_version = '3.0.0-LSTM'  # With advanced ML
            
            return {
                'race_info': race_info,
                'strategies': strategy_predictions,
                'enhanced_data': enhanced_data,
                'data_completeness': enhanced_data.get('data_completeness', 0.0) if enhanced_data else 0.0,
                'prediction_time': datetime.now(),
                'model_version': model_version,
                'v3_features_active': self.use_v3,
                'advanced_ml_active': self.advanced_ml is not None and self.advanced_ml.is_trained
            }
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def print_prediction(self, prediction: Dict):
        """Print prediction results in a nice format with enhanced data."""
        if not prediction:
            print("❌ No prediction to display")
            return
        
        race_info = prediction['race_info']
        strategies = prediction['strategies']
        enhanced_data = prediction.get('enhanced_data')
        data_completeness = prediction.get('data_completeness', 0.0)
        
        print("\n" + "="*80)
        print(f"🏎️  F1 RACE PREDICTION - {race_info['race_name'].upper()}")
        
        # Enhanced version display
        version_str = f"Model Version: {prediction['model_version']}"
        if prediction.get('v3_features_active'):
            version_str += " [v3.0 Features Active]"
        if prediction.get('advanced_ml_active'):
            version_str += " [LSTM]"
        
        print(f"{version_str} | Data Completeness: {data_completeness*100:.0f}%")
        print("="*80)
        
        print(f"\n📋 RACE INFORMATION:")
        print(f"   Location: {race_info['location']}, {race_info['country']}")
        print(f"   Date: {race_info['race_date'].strftime('%B %d, %Y (%A)')}")
        print(f"   Days until race: {race_info['days_until_race']}")
        print(f"   Circuit: {race_info['track_name']}")
        print(f"   Total laps: {race_info['total_laps']}")
        print(f"   Circuit length: {race_info['circuit_length']:.3f} km")
        print(f"   Avg lap time: {race_info['avg_lap_time']:.1f}s")
        
        # Weather forecast
        if race_info.get('weather'):
            weather = race_info['weather']
            print(f"\n🌤️  WEATHER FORECAST:")
            print(f"   Temperature: {weather.get('temperature', 'N/A')}°C")
            print(f"   Humidity: {weather.get('humidity', 'N/A')}%")
            print(f"   Conditions: {weather.get('description', 'Unknown')}")
            print(f"   Rain Probability: {weather.get('rain_probability', 0)}%")
            if weather.get('rain_probability', 0) > 50:
                print(f"   ⚠️  HIGH RAIN RISK - Consider wet tire strategy!")
        
        # Qualifying info
        if race_info.get('qualifying'):
            quali = race_info['qualifying']
            print(f"\n🏁 QUALIFYING DATA:")
            print(f"   Status: {quali.get('session_status', 'Not available')}")
            if quali.get('grid_positions'):
                print(f"   Grid positions: {len(quali['grid_positions'])} drivers")
                # Show pole position
                pole_driver = min(quali['grid_positions'].items(), key=lambda x: x[1])
                print(f"   Pole position: {pole_driver[0]}")
        
        # Practice session data
        if race_info.get('practice'):
            practice = race_info['practice']
            print(f"\n🔧 PRACTICE SESSION ANALYSIS:")
            print(f"   Sessions analyzed: {', '.join(practice.get('sessions_analyzed', []))}")
            
            # Tire degradation
            if practice.get('tire_degradation'):
                print(f"   📉 Tire Degradation Data:")
                for session, deg_data in list(practice['tire_degradation'].items())[:1]:  # Show first session
                    if deg_data:
                        for compound, data in list(deg_data.items())[:3]:  # Show top 3 compounds
                            print(f"      {compound}: {data['avg_degradation']:.3f}s/lap "
                                  f"(±{data['std_degradation']:.3f}s, {data['samples']} samples)")
        
        # Tire allocation
        if race_info.get('tire_allocation'):
            tires = race_info['tire_allocation']
            print(f"\n🛞 PIRELLI TIRE ALLOCATION:")
            print(f"   Compounds: {', '.join(tires.get('compounds', []))}")
            if tires.get('soft'):
                print(f"   ✅ Soft compound available")
            if tires.get('medium'):
                print(f"   ✅ Medium compound available")
            if tires.get('hard'):
                print(f"   ✅ Hard compound available")
        
        if strategies['success']:
            optimal = strategies['optimal_strategy']
            
            # Show ML prediction if available
            if strategies.get('ml_prediction'):
                ml_pred = strategies['ml_prediction']
                model_version = "v3.1 (Ensemble)" if hasattr(self.ml_predictor, 'strategy_ensemble') else "v2.5"
                print(f"\n🤖 MACHINE LEARNING PREDICTION ({model_version}):")
                print(f"   Strategy Type: {ml_pred['strategy_type']}-stop")
                print(f"   Optimal Pit Lap: Lap {ml_pred['pit_lap']}")
                print(f"   Confidence: {ml_pred['confidence']*100:.1f}%")
                if ml_pred.get('model'):
                    print(f"   Model: {ml_pred['model']}")
                if ml_pred.get('features_used'):
                    print(f"   Features: {ml_pred['features_used']} enhanced features")
                if strategies.get('ml_enhanced'):
                    print(f"   ✅ ML-optimized strategy selected")
            
            print(f"\n🏆 OPTIMAL STRATEGY:")
            print(f"   Name: {optimal.name}")
            print(f"   Compounds: {' → '.join(optimal.compounds)}")
            print(f"   Pit stops: {len(optimal.pit_laps)}")
            print(f"   Pit laps: {optimal.pit_laps}")
            print(f"   Expected time: {optimal.expected_time:.1f}s")
            
            print(f"\n📊 STINT BREAKDOWN:")
            for i, compound in enumerate(optimal.compounds):
                if i < len(optimal.pit_laps):
                    stint_laps = optimal.pit_laps[i] - (optimal.pit_laps[i-1] if i > 0 else 0)
                else:
                    last_pit = optimal.pit_laps[-1] if optimal.pit_laps else 0
                    stint_laps = race_info['total_laps'] - last_pit
                print(f"   Stint {i+1}: {compound:6s} - {stint_laps:2d} laps")
            
            print(f"\n🎯 ALTERNATIVE STRATEGIES:")
            risk_levels = strategies['strategies_by_risk']
            for level, strat in risk_levels.items():
                if strat:
                    stops_str = ' → '.join(strat.compounds)
                    print(f"   {level.capitalize():12s}: {strat.name:20s} ({stops_str}) - {strat.expected_time:.1f}s")
            
            print(f"\n📈 STRATEGY DISTRIBUTION:")
            for stop_count in sorted(strategies['strategies_by_stops'].keys()):
                count = len(strategies['strategies_by_stops'][stop_count])
                print(f"   {stop_count}-stop: {count:3d} strategies")
            
            crash_prob = strategies.get('crash_probability', {})
            if crash_prob:
                print(f"\n⚠️  INCIDENT PROBABILITY:")
                print(f"   Safety Car: {crash_prob.get('safety_car', 0.3)*100:.1f}%")
                print(f"   Red Flag: {crash_prob.get('red_flag', 0.1)*100:.1f}%")
            
            print(f"\n✅ Total strategies evaluated: {strategies['total_strategies_evaluated']}")
        else:
            print(f"\n❌ Strategy prediction failed: {strategies.get('error')}")
        
        print(f"\n⏰ Prediction generated: {prediction['prediction_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 Model version: {prediction['model_version']}")
        print("="*80 + "\n")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='F1 Race Prediction System')
    parser.add_argument('--year', type=int, help='Year to predict')
    parser.add_argument('--save', action='store_true', help='Save prediction to JSON')
    args = parser.parse_args()
    
    pipeline = F1RacePredictionPipeline()
    prediction = pipeline.predict_upcoming_race(year=args.year)
    
    if prediction:
        pipeline.print_prediction(prediction)
        
        if args.save:
            import json
            race_name = prediction['race_info']['race_name'].replace(' ', '_')
            filename = f"prediction_{race_name}.json"
            
            json_data = {
                'race_info': {k: str(v) if isinstance(v, (pd.Timestamp, datetime)) else v 
                             for k, v in prediction['race_info'].items()},
                'optimal_strategy': {
                    'name': prediction['strategies']['optimal_strategy'].name,
                    'compounds': prediction['strategies']['optimal_strategy'].compounds,
                    'pit_laps': prediction['strategies']['optimal_strategy'].pit_laps,
                    'expected_time': prediction['strategies']['optimal_strategy'].expected_time
                },
                'prediction_time': prediction['prediction_time'].isoformat(),
                'model_version': prediction['model_version']
            }
            
            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=2)
            print(f"✅ Prediction saved to: {filename}")
