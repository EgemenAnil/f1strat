#!/usr/bin/env python3
"""
Validate F1 Strategy System against historical race data.
Compare predicted strategies vs actual race results.
"""

import fastf1
import pandas as pd
import numpy as np
from datetime import datetime
from src.models.strategy_optimizer import StrategyOptimizer
from src.features.driver_ratings import DriverRatings, TeamPerformance

# Suppress FastF1 warnings
import warnings
warnings.filterwarnings('ignore')

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')


def load_historical_race(year: int, gp_name: str, session_type: str = 'R'):
    """Load historical race data from FastF1."""
    print(f"\n📥 Loading {year} {gp_name} {session_type}...")
    session = fastf1.get_session(year, gp_name, session_type)
    session.load()
    return session


def get_actual_strategies(session):
    """Extract actual pit stop strategies from race data."""
    strategies = {}
    
    for driver in session.drivers:
        driver_info = session.get_driver(driver)
        
        # Get laps data
        laps = session.laps.pick_driver(driver)
        
        if len(laps) == 0:
            continue
        
        # Reset index to use integer indexing
        laps = laps.reset_index(drop=True)
            
        # Find pit stops by compound changes
        pit_laps = []
        compounds_used = []
        
        for i in range(len(laps)):
            # Check for compound change (pit stop)
            if i > 0:
                prev_compound = laps.loc[i-1, 'Compound']
                curr_compound = laps.loc[i, 'Compound']
                if pd.notna(prev_compound) and pd.notna(curr_compound):
                    if prev_compound != curr_compound:
                        pit_laps.append(int(laps.loc[i, 'LapNumber']))
                        if curr_compound not in compounds_used:
                            compounds_used.append(curr_compound)
        
        # Get all unique compounds used
        all_compounds = laps['Compound'].dropna().unique().tolist()
        
        strategies[driver] = {
            'driver_code': driver,
            'team': driver_info['TeamName'] if hasattr(driver_info, 'TeamName') else 'Unknown',
            'pit_stops': len(pit_laps),
            'pit_laps': pit_laps,
            'compounds': all_compounds,
            'total_laps': len(laps),
            'finish_position': laps.iloc[-1]['Position'] if len(laps) > 0 else None
        }
    
    return strategies


def predict_strategies(race_info):
    """Predict optimal strategies using our system."""
    print(f"\n🤖 Predicting strategies for {race_info['circuit']}...")
    
    optimizer = StrategyOptimizer(
        total_laps=race_info['total_laps'],
        track_name=race_info['circuit']
    )
    
    # Use full optimization with Monte Carlo simulation
    optimized_strategies = optimizer.optimize(
        weather_forecast=None,
        track_name=race_info['circuit'],
        num_simulations=50  # Reduced for speed (default is 100)
    )
    
    return optimized_strategies[:10]  # Return top 10


def compare_results(actual_strategies, predicted_strategies):
    """Compare actual vs predicted strategies."""
    print("\n" + "="*80)
    print("📊 VALIDATION RESULTS - ACTUAL vs PREDICTED")
    print("="*80)
    
    # Count pit stop distribution
    actual_1stop = sum(1 for s in actual_strategies.values() if s['pit_stops'] == 1)
    actual_2stop = sum(1 for s in actual_strategies.values() if s['pit_stops'] == 2)
    actual_3stop = sum(1 for s in actual_strategies.values() if s['pit_stops'] >= 3)
    
    total_drivers = len(actual_strategies)
    
    print(f"\n🏁 ACTUAL RACE RESULTS ({total_drivers} drivers):")
    print(f"   1-stop strategies: {actual_1stop} ({actual_1stop/total_drivers*100:.1f}%)")
    print(f"   2-stop strategies: {actual_2stop} ({actual_2stop/total_drivers*100:.1f}%)")
    print(f"   3+ stop strategies: {actual_3stop} ({actual_3stop/total_drivers*100:.1f}%)")
    
    # Top 3 predicted
    print(f"\n🤖 TOP 3 PREDICTED STRATEGIES:")
    for i, strategy in enumerate(predicted_strategies[:3], 1):
        race_time_min = strategy.expected_time / 60
        print(f"   {i}. {strategy.name} - {len(strategy.pit_laps)}-stop")
        print(f"      Expected time: {race_time_min:.1f} minutes")
        print(f"      Compounds: {' → '.join([c[:1] for c in strategy.compounds])}")
    
    # Most common actual strategy
    print(f"\n📈 MOST COMMON ACTUAL STRATEGIES:")
    strategy_counts = {}
    for driver, data in actual_strategies.items():
        key = f"{data['pit_stops']}-stop"
        strategy_counts[key] = strategy_counts.get(key, 0) + 1
    
    for strategy, count in sorted(strategy_counts.items(), key=lambda x: -x[1])[:3]:
        print(f"   {strategy}: {count} drivers ({count/total_drivers*100:.1f}%)")
    
    # Accuracy check
    predicted_stops = len(predicted_strategies[0].pit_laps)
    most_common_stops = max(strategy_counts.items(), key=lambda x: x[1])[0]
    most_common_stops_num = int(most_common_stops.split('-')[0])
    
    print(f"\n✅ ACCURACY CHECK:")
    print(f"   Predicted optimal: {predicted_stops}-stop")
    print(f"   Most used in race: {most_common_stops_num}-stop")
    
    if predicted_stops == most_common_stops_num:
        print(f"   ✅ MATCH! Our prediction aligns with real race!")
    else:
        print(f"   ⚠️  MISMATCH - Difference: {abs(predicted_stops - most_common_stops_num)} stops")
    
    return {
        'predicted_stops': predicted_stops,
        'actual_most_common': most_common_stops_num,
        'match': predicted_stops == most_common_stops_num,
        'actual_1stop_pct': actual_1stop/total_drivers*100,
        'actual_2stop_pct': actual_2stop/total_drivers*100,
    }


def validate_race(year: int, gp_name: str, circuit_name: str):
    """Complete validation workflow for a single race."""
    print("\n" + "="*80)
    print(f"🏎️  VALIDATING: {year} {gp_name}")
    print("="*80)
    
    # Load actual race data
    session = load_historical_race(year, gp_name, 'R')
    
    # Get race info
    total_laps = session.total_laps
    
    print(f"\n📋 Race Info:")
    print(f"   Circuit: {circuit_name}")
    print(f"   Total Laps: {total_laps}")
    print(f"   Date: {session.date}")
    
    # Extract actual strategies
    actual_strategies = get_actual_strategies(session)
    
    # Predict strategies
    race_info = {
        'circuit': circuit_name,
        'total_laps': total_laps
    }
    predicted_strategies = predict_strategies(race_info)
    
    # Compare
    results = compare_results(actual_strategies, predicted_strategies)
    
    return results


def validate_multiple_races():
    """Test system against multiple races with different characteristics."""
    
    # Define test races with various characteristics
    test_races = [
        # Normal dry race - baseline
        {
            'year': 2023,
            'gp_name': 'Bahrain',
            'circuit_name': 'Bahrain',
            'category': '🏜️ DESERT TRACK - Baseline',
            'characteristics': 'Low degradation, hard to overtake'
        },
        
        # High degradation track
        {
            'year': 2023,
            'gp_name': 'British',
            'circuit_name': 'Silverstone',
            'category': '🔥 HIGH DEGRADATION',
            'characteristics': 'High-speed corners, tire stress'
        },
        
        # Street circuit
        {
            'year': 2023,
            'gp_name': 'Monaco',
            'circuit_name': 'Monaco',
            'category': '🏙️ STREET CIRCUIT',
            'characteristics': 'Slow, narrow, overtaking nearly impossible'
        },
        
        # Wet/variable conditions (Belgium often has rain)
        {
            'year': 2023,
            'gp_name': 'Belgian',
            'circuit_name': 'Belgium',
            'category': '🌧️ VARIABLE WEATHER',
            'characteristics': 'High-speed, often wet, long lap'
        },
        
        # Chaotic race (Singapore is physically demanding, often has safety cars)
        {
            'year': 2023,
            'gp_name': 'Singapore',
            'circuit_name': 'Singapore',
            'category': '🌙 NIGHT STREET RACE',
            'characteristics': 'Hot, humid, high safety car probability'
        },
        
        # High-speed power track
        {
            'year': 2023,
            'gp_name': 'Italian',
            'circuit_name': 'Monza',
            'category': '⚡ HIGH-SPEED POWER',
            'characteristics': 'Fastest circuit, low downforce, slipstream crucial'
        },
        
        # EXTREME CONDITIONS - Rain/Red Flags
        {
            'year': 2021,
            'gp_name': 'Belgium',
            'circuit_name': 'Belgium',
            'category': '🌧️ EXTREME RAIN (Belgium 2021)',
            'characteristics': 'Shortest race ever - 2 laps behind SC, red flag'
        },
        {
            'year': 2020,
            'gp_name': 'Turkey',
            'circuit_name': 'Turkey',
            'category': '☔ WET RACE (Turkey 2020)',
            'characteristics': 'Very wet, intermediate tires entire race'
        },
        {
            'year': 2022,
            'gp_name': 'Singapore',
            'circuit_name': 'Singapore',
            'category': '🚨 SAFETY CAR CHAOS (Singapore 2022)',
            'characteristics': 'Multiple safety cars, varied conditions'
        },
        
        # EXTREME CONDITIONS - Crashes/Red Flags
        {
            'year': 2021,
            'gp_name': 'Hungary',
            'circuit_name': 'Hungary',
            'category': '💥 MULTI-CAR CRASH (Hungary 2021)',
            'characteristics': 'Lap 1 bowling, red flag, strategic chaos'
        },
        {
            'year': 2022,
            'gp_name': 'Saudi Arabia',
            'circuit_name': 'Jeddah',
            'category': '🚩 RED FLAG RACE (Saudi 2022)',
            'characteristics': 'Schumacher massive crash, red flag'
        },
        {
            'year': 2021,
            'gp_name': 'Azerbaijan',
            'circuit_name': 'Azerbaijan',
            'category': '💥 TIRE FAILURE (Azerbaijan 2021)',
            'characteristics': 'Verstappen tire failure, red flag restart'
        },
        {
            'year': 2022,
            'gp_name': 'Britain',
            'circuit_name': 'Silverstone',
            'category': '🚩 CRASH & RED FLAG (Britain 2022)',
            'characteristics': 'Zhou massive crash, red flag, strategic reset'
        },
        
        # EXTREME CONDITIONS - Strategic battles
        {
            'year': 2021,
            'gp_name': 'France',
            'circuit_name': 'France',
            'category': '♟️ STRATEGIC BATTLE (France 2021)',
            'characteristics': 'Ver vs Ham, different strategies, undercut'
        },
        {
            'year': 2022,
            'gp_name': 'Monaco',
            'circuit_name': 'Monaco',
            'category': '☔ LATE RAIN CHAOS (Monaco 2022)',
            'characteristics': 'Ferrari strategy disaster, late rain'
        },
    ]
    
    print("\n" + "="*80)
    print("🏁 COMPREHENSIVE F1 STRATEGY VALIDATION")
    print("="*80)
    print("\nTesting across different track types and race conditions...")
    print("Looking for: rain races, safety cars, crashes, and extreme scenarios")
    
    all_results = []
    successful_tests = 0
    total_tests = 0
    
    for race in test_races:
        try:
            print(f"\n\n{'='*80}")
            print(f"{race['category']}")
            print(f"{'='*80}")
            print(f"📍 {race['characteristics']}")
            
            result = validate_race(
                year=race['year'],
                gp_name=race['gp_name'],
                circuit_name=race['circuit_name']
            )
            
            result['race'] = f"{race['year']} {race['gp_name']}"
            result['category'] = race['category']
            all_results.append(result)
            total_tests += 1
            
            if result['match']:
                successful_tests += 1
            
        except Exception as e:
            print(f"\n⚠️  Could not validate {race['gp_name']}: {str(e)}")
            print(f"   (Data may not be cached - run get_data.py first)")
            continue
    
    # Final summary
    print("\n\n" + "="*80)
    print("📊 COMPREHENSIVE VALIDATION SUMMARY")
    print("="*80)
    
    if len(all_results) == 0:
        print("\n⚠️  No races could be validated.")
        print("💡 Run get_data.py to download race data first:")
        print("   python get_data.py")
        return
    
    overall_accuracy = (successful_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n🎯 Overall Performance:")
    print(f"   Races tested: {total_tests}")
    print(f"   Successful predictions: {successful_tests}")
    print(f"   Overall accuracy: {overall_accuracy:.1f}%")
    
    print(f"\n� Results by Track Type:")
    for result in all_results:
        status = "✅" if result['match'] else "⚠️"
        print(f"   {status} {result['race']}: {result['predicted_stops']}-stop predicted, "
              f"{result['actual_most_common']}-stop most common "
              f"({result['actual_1stop_pct']:.0f}% 1-stop, {result['actual_2stop_pct']:.0f}% 2-stop)")
    
    # Track type analysis
    print(f"\n💡 Key Insights:")
    
    # Find highest 1-stop usage
    max_1stop = max(all_results, key=lambda x: x['actual_1stop_pct'])
    print(f"   🔒 Most 1-stop friendly: {max_1stop['race']} ({max_1stop['actual_1stop_pct']:.0f}%)")
    
    # Find highest 2-stop usage
    max_2stop = max(all_results, key=lambda x: x['actual_2stop_pct'])
    print(f"   🔄 Most 2-stop friendly: {max_2stop['race']} ({max_2stop['actual_2stop_pct']:.0f}%)")
    
    print(f"\n🎓 System Reliability:")
    if overall_accuracy >= 80:
        print(f"   ✅ EXCELLENT - System is highly reliable across different conditions!")
    elif overall_accuracy >= 60:
        print(f"   ✔️  GOOD - System performs well, minor improvements possible")
    else:
        print(f"   ⚠️  NEEDS IMPROVEMENT - System struggles with varied conditions")
    
    print("\n" + "="*80)
    print("✅ Comprehensive Validation Complete!")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏁 F1 STRATEGY VALIDATION SYSTEM v2.0")
    print("="*80)
    print("\n🔬 Testing system against multiple race scenarios:")
    print("   • Normal conditions (Bahrain)")
    print("   • High degradation (Silverstone)")
    print("   • Street circuits (Monaco, Singapore)")
    print("   • Variable weather (Spa)")
    print("   • High-speed power tracks (Monza)")
    
    results = validate_multiple_races()
    
    if results and len(results) > 0:
        print(f"\n📊 Successfully validated {len(results)} races!")
        print(f"\n💾 All data cached in: cache/")
    else:
        print(f"\n💡 TIP: Download more race data with:")
        print(f"   python get_data.py")
