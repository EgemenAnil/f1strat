"""
Main F1 Race Prediction Pipeline
Integrates all components to predict upcoming F1 races.
"""

import sys
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.fetcher import F1DataFetcher
from src.features.engineering import F1FeatureEngineer
from src.features.track_features import TrackFeatures
from src.models.strategy_optimizer import StrategyOptimizer
from src.models.crash_predictor import CrashPredictor


class F1RacePredictionPipeline:
    """Complete pipeline for predicting upcoming F1 races."""
    
    def __init__(self, cache_dir: str = './cache'):
        """
        Initialize prediction pipeline.
        
        Args:
            cache_dir: Directory for caching data
        """
        self.cache_dir = cache_dir
        self.fetcher = F1DataFetcher(cache_dir)
        self.feature_engineer = F1FeatureEngineer()
        self.crash_predictor = CrashPredictor()
        
        self.race_predictor = None  # Will be loaded or trained
        self.strategy_optimizer = None
    
    def predict_upcoming_race(self, race_name: Optional[str] = None,
                            year: Optional[int] = None) -> Dict:
        """
        Predict the next upcoming F1 race.
        
        Args:
            race_name: Specific race to predict (None = next race)
            year: Year (None = current year)
        
        Returns:
            Dictionary with complete race prediction
        """
        print("=" * 80)
        print("F1 RACE PREDICTION SYSTEM")
        print("=" * 80)
        
        # Step 1: Get upcoming race info
        print("\n[1/7] Fetching upcoming race information...")
        upcoming_race = self.fetcher.get_upcoming_race()
        
        if upcoming_race is None:
            print("No upcoming race found. Season may have ended.")
            return None
        
        print(f"✓ Next Race: {upcoming_race['race_name']}")
        print(f"  Date: {upcoming_race['date']}")
        print(f"  Circuit: {upcoming_race['circuit']}")
        
        # Step 2: Get weather forecast
        print("\n[2/7] Fetching weather forecast...")
        weather = self._get_weather_forecast(upcoming_race)
        
        if weather:
            print(f"✓ Weather Forecast:")
            print(f"  Temperature: {weather.get('temperature', 'N/A')}°C")
            print(f"  Rain Probability: {weather.get('rain_probability', 0):.0%}")
            print(f"  Humidity: {weather.get('humidity', 'N/A')}%")
        
        # Step 3: Get track characteristics
        print("\n[3/7] Analyzing track characteristics...")
        track_info = TrackFeatures.get_track_info(upcoming_race['circuit'])
        
        if track_info:
            print(f"✓ Track Analysis:")
            print(f"  Length: {track_info['length_km']} km")
            print(f"  Corners: {track_info['corners']}")
            print(f"  Overtaking Difficulty: {track_info['overtaking_difficulty']:.1%}")
            print(f"  Typical Pit Loss: {track_info['pit_loss_seconds']}s")
        
        # Step 4: Analyze crash/incident risk
        print("\n[4/7] Calculating incident probabilities...")
        track_risk = self.crash_predictor.analyze_track_risk(upcoming_race['circuit'])
        sc_probability = self.crash_predictor.calculate_safety_car_probability(
            total_laps=upcoming_race.get('total_laps', 57),
            weather=weather,
            track_name=upcoming_race['circuit']
        )
        
        print(f"✓ Risk Analysis:")
        print(f"  Risk Level: {track_risk['risk_category']}")
        print(f"  Safety Car Probability: {sc_probability:.0%}")
        print(f"  Expected Incidents: {track_risk['expected_incidents_per_race']:.2f}")
        
        # Step 5: Load/Train race prediction model
        print("\n[5/7] Preparing race prediction model...")
        if self.race_predictor is None:
            print("  Note: Full ML model requires historical training data")
            print("  Using simulation-based predictions...")
        
        # Step 6: Optimize pit stop strategy
        print("\n[6/7] Optimizing pit stop strategies...")
        self.strategy_optimizer = StrategyOptimizer(
            race_predictor=self.race_predictor,
            total_laps=upcoming_race.get('total_laps', 57)
        )
        
        # Find optimal strategies for different risk levels
        strategies = {
            'conservative': self.strategy_optimizer.get_optimal_strategy(
                weather_forecast=weather,
                track_name=upcoming_race['circuit'],
                risk_tolerance='conservative'
            ),
            'balanced': self.strategy_optimizer.get_optimal_strategy(
                weather_forecast=weather,
                track_name=upcoming_race['circuit'],
                risk_tolerance='medium'
            ),
            'aggressive': self.strategy_optimizer.get_optimal_strategy(
                weather_forecast=weather,
                track_name=upcoming_race['circuit'],
                risk_tolerance='aggressive'
            )
        }
        
        print(f"✓ Strategy Optimization Complete")
        
        # Step 7: Compile final prediction
        print("\n[7/7] Compiling predictions...")
        
        prediction = {
            'race_info': upcoming_race,
            'weather_forecast': weather,
            'track_characteristics': track_info,
            'risk_analysis': track_risk,
            'safety_car_probability': sc_probability,
            'optimal_strategies': strategies,
            'recommendations': self._generate_recommendations(
                strategies, weather, track_risk
            ),
            'timestamp': datetime.now().isoformat()
        }
        
        print("\n✓ Prediction Complete!")
        
        return prediction
    
    def _get_weather_forecast(self, race_info: Dict) -> Optional[Dict]:
        """Get weather forecast for race."""
        try:
            # Get track coordinates
            from src.data.fetcher import F1DataFetcher
            coords = F1DataFetcher.TRACK_COORDINATES.get(race_info['circuit'])
            
            if coords:
                weather = self.fetcher.get_weather_forecast(
                    coords['lat'],
                    coords['lon'],
                    race_info['date']
                )
                return weather
        except Exception as e:
            print(f"  Warning: Could not fetch weather forecast: {e}")
        
        return None
    
    def _generate_recommendations(self, strategies: Dict,
                                 weather: Optional[Dict],
                                 track_risk: Dict) -> List[str]:
        """Generate race recommendations."""
        recommendations = []
        
        # Primary strategy recommendation
        best_strategy = strategies['balanced']
        recommendations.append(
            f"OPTIMAL STRATEGY: {best_strategy.name}"
        )
        recommendations.append(
            f"  Compounds: {' → '.join(best_strategy.compounds)}"
        )
        recommendations.append(
            f"  Pit on laps: {', '.join(map(str, best_strategy.pit_laps))}"
        )
        
        # Weather-based recommendations
        if weather:
            rain_prob = weather.get('rain_probability', 0)
            if rain_prob > 0.5:
                recommendations.append(
                    f"⚠ HIGH RAIN RISK ({rain_prob:.0%}): Have intermediates ready, "
                    "consider early pit stop for tire change"
                )
            elif rain_prob > 0.2:
                recommendations.append(
                    f"⚡ RAIN POSSIBLE ({rain_prob:.0%}): Monitor radar, "
                    "be flexible with strategy"
                )
            
            temp = weather.get('temperature', 20)
            if temp > 35:
                recommendations.append(
                    f"🌡 HOT CONDITIONS ({temp}°C): Expect higher tire degradation, "
                    "consider extra pit stop"
                )
        
        # Risk-based recommendations
        if track_risk['risk_category'] in ['High', 'Very High']:
            recommendations.append(
                f"🚨 {track_risk['risk_category'].upper()} INCIDENT RISK: "
                f"{track_risk['recommendations'][0]}"
            )
        
        # Alternative strategies
        if strategies['aggressive'].expected_time < best_strategy.expected_time * 1.02:
            recommendations.append(
                f"💡 ALTERNATIVE: Aggressive strategy ({strategies['aggressive'].name}) "
                "could gain positions if willing to take risks"
            )
        
        return recommendations
    
    def print_prediction(self, prediction: Dict):
        """Pretty print prediction results."""
        print("\n" + "=" * 80)
        print("RACE PREDICTION SUMMARY")
        print("=" * 80)
        
        # Race info
        race_info = prediction['race_info']
        print(f"\n📍 {race_info['race_name']}")
        print(f"   {race_info['circuit']}")
        print(f"   {race_info['date']}")
        
        # Weather
        weather = prediction.get('weather_forecast')
        if weather:
            print(f"\n🌤 Weather Forecast:")
            print(f"   Temperature: {weather.get('temperature', 'N/A')}°C")
            print(f"   Rain Probability: {weather.get('rain_probability', 0):.0%}")
            print(f"   Conditions: {weather.get('description', 'Unknown')}")
        
        # Risk
        print(f"\n⚠️  Risk Assessment:")
        print(f"   Track Risk: {prediction['risk_analysis']['risk_category']}")
        print(f"   Safety Car Probability: {prediction['safety_car_probability']:.0%}")
        
        # Optimal strategy
        print(f"\n🏁 RECOMMENDED STRATEGY:")
        for rec in prediction['recommendations']:
            print(f"   {rec}")
        
        # Alternative strategies
        print(f"\n📊 Alternative Strategies:")
        for risk_level, strategy in prediction['optimal_strategies'].items():
            print(f"\n   {risk_level.upper()}:")
            print(f"     {strategy.name}")
            print(f"     Expected Time: {strategy.expected_time:.1f}s")
            print(f"     Confidence: {strategy.confidence:.0%}")
        
        print("\n" + "=" * 80)
    
    def train_model_from_historical_data(self, years: List[int] = [2023, 2024]):
        """
        Train race prediction model on historical data.
        
        Args:
            years: Years to include in training
        """
        print(f"Training model on historical data from {years}...")
        
        # This would require:
        # 1. Fetch all races from specified years
        # 2. Process and create features
        # 3. Train XGBoost/Neural Network model
        # 4. Save model for future predictions
        
        print("Note: Full model training requires extensive historical data")
        print("For now, using simulation-based predictions")


def main():
    """Main entry point for race prediction."""
    print("\n🏎️  F1 Race Prediction System v1.0\n")
    
    # Initialize pipeline
    pipeline = F1RacePredictionPipeline()
    
    # Predict next race
    prediction = pipeline.predict_upcoming_race()
    
    if prediction:
        # Print results
        pipeline.print_prediction(prediction)
        
        # Save to file
        output_file = f"prediction_{prediction['race_info']['race_name'].replace(' ', '_')}.json"
        import json
        with open(output_file, 'w') as f:
            # Convert to JSON-serializable format
            json_prediction = {
                k: v for k, v in prediction.items()
                if k not in ['optimal_strategies']  # Skip Strategy objects
            }
            json_prediction['strategies'] = {
                level: {
                    'name': strat.name,
                    'compounds': strat.compounds,
                    'pit_laps': strat.pit_laps,
                    'expected_time': strat.expected_time
                }
                for level, strat in prediction['optimal_strategies'].items()
            }
            json.dump(json_prediction, f, indent=2)
        
        print(f"\n💾 Prediction saved to: {output_file}")
    else:
        print("❌ Could not generate prediction")


if __name__ == "__main__":
    main()
