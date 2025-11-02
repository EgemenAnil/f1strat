"""
2025 Season Validation Script
Tests strategy predictions against actual 2025 race results
"""

import fastf1
import pandas as pd
import warnings
from src.models.strategy_optimizer import StrategyOptimizer
from src.data.fetcher import F1DataFetcher

warnings.filterwarnings('ignore')

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')

def get_2025_races():
    """Get list of available 2025 races"""
    try:
        schedule = fastf1.get_event_schedule(2025)
        print(f"\n{'='*80}")
        print(f"2025 F1 SEASON - {len(schedule)} races found")
        print(f"{'='*80}\n")
        
        races = []
        for idx, event in schedule.iterrows():
            race_info = {
                'round': idx + 1,
                'name': event['EventName'],
                'location': event['Location'],
                'date': event['EventDate'],
                'country': event.get('Country', 'Unknown')
            }
            races.append(race_info)
            print(f"{race_info['round']:2d}. {race_info['name']:30s} - {race_info['location']:20s} ({race_info['date']})")
        
        return races
    except Exception as e:
        print(f"Error loading 2025 schedule: {e}")
        return []

def test_race(year, race_name):
    """Test a single race prediction vs actual results"""
    print(f"\n{'='*80}")
    print(f"TESTING: {year} {race_name}")
    print(f"{'='*80}\n")
    
    try:
        # Load race data
        session = fastf1.get_session(year, race_name, 'R')
        print(f"Loading race data...")
        session.load()
        
        # Get track info
        track_name = session.event['EventName']
        location = session.event['Location']
        
        print(f"Track: {track_name}")
        print(f"Location: {location}")
        print(f"Total laps: {session.total_laps}")
        
        # Analyze actual strategies used
        laps = session.laps
        if laps.empty:
            print("❌ No lap data available")
            return None
        
        # Get strategy distribution
        print(f"\n📊 ACTUAL RACE STRATEGIES:")
        drivers = laps['Driver'].unique()
        
        strategy_counts = {}
        for driver in drivers:
            driver_laps = laps[laps['Driver'] == driver]
            compounds = driver_laps['Compound'].dropna().unique()
            num_stops = len(compounds) - 1  # Number of pit stops
            
            if num_stops >= 0:
                strategy_key = f"{num_stops}-stop"
                strategy_counts[strategy_key] = strategy_counts.get(strategy_key, 0) + 1
        
        # Find most common strategy
        if strategy_counts:
            most_common = max(strategy_counts, key=strategy_counts.get)
            total_drivers = sum(strategy_counts.values())
            
            print(f"Strategy Distribution:")
            for strategy, count in sorted(strategy_counts.items()):
                percentage = (count / total_drivers) * 100
                print(f"  {strategy}: {count} drivers ({percentage:.1f}%)")
            
            print(f"\n✅ Most Common Strategy: {most_common}")
            
            # Now test our prediction
            print(f"\n🤖 SYSTEM PREDICTION:")
            print(f"Generating optimal strategy for {track_name}...")
            
            # Create optimizer with race parameters
            optimizer = StrategyOptimizer(
                track_name=track_name,
                total_laps=session.total_laps
            )
            
            # Optimize strategy
            strategies = optimizer.optimize(
                weather_forecast={'temperature': 25, 'humidity': 60, 'rain_probability': 0},
                track_name=track_name,
                num_simulations=50
            )
            
            if strategies:
                # Get best strategy
                best_strategy = strategies[0]
                predicted_stops = len(best_strategy.pit_laps)
                predicted_strategy = f"{predicted_stops}-stop"
                
                print(f"Predicted Strategy: {predicted_strategy}")
                print(f"Predicted Compounds: {' → '.join(best_strategy.compounds)}")
                print(f"Predicted Pit Laps: {best_strategy.pit_laps}")
                print(f"Expected Time: {best_strategy.expected_time:.2f}s")
                
                # Compare
                print(f"\n{'='*80}")
                if predicted_strategy == most_common:
                    print(f"✅ CORRECT! Predicted {predicted_strategy}, Actual most common: {most_common}")
                    return True
                else:
                    print(f"❌ INCORRECT! Predicted {predicted_strategy}, Actual most common: {most_common}")
                    return False
            else:
                print("❌ Prediction failed")
                return None
        else:
            print("❌ Could not determine actual strategies")
            return None
            
    except Exception as e:
        print(f"❌ Error testing race: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main validation function"""
    print("\n" + "="*80)
    print("2025 F1 SEASON VALIDATION")
    print("="*80)
    
    # Get 2025 races
    races = get_2025_races()
    
    if not races:
        print("\n⚠️  No 2025 races found. FastF1 may not have 2025 data yet.")
        print("Note: FastF1 typically updates data during/after the actual season.")
        return
    
    # Test key races
    test_races = [
        (2025, 'Bahrain'),      # Season opener
        (2025, 'Monaco'),       # Street circuit (our special case)
        (2025, 'Silverstone'),  # Normal circuit
        (2025, 'Singapore'),    # Night race
        (2025, 'Spa'),          # Power circuit
    ]
    
    print(f"\n{'='*80}")
    print(f"TESTING {len(test_races)} KEY RACES")
    print(f"{'='*80}")
    
    results = []
    for year, race_name in test_races:
        result = test_race(year, race_name)
        if result is not None:
            results.append((race_name, result))
    
    # Summary
    if results:
        correct = sum(1 for _, r in results if r)
        total = len(results)
        accuracy = (correct / total) * 100
        
        print(f"\n{'='*80}")
        print(f"2025 SEASON VALIDATION SUMMARY")
        print(f"{'='*80}")
        print(f"Races tested: {total}")
        print(f"Correct predictions: {correct}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"{'='*80}\n")
        
        for race_name, result in results:
            status = "✅" if result else "❌"
            print(f"{status} {race_name}")

if __name__ == '__main__':
    main()
