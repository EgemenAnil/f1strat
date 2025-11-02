"""
Driver Performance Ratings based on 2025 Season Data
Analyzes real 2025 race data to rate drivers on various performance metrics
"""

import fastf1
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DriverPerformanceAnalyzer:
    """Analyzes driver performance from 2025 season data"""
    
    def __init__(self, cache_dir: str = './cache'):
        """Initialize with FastF1 cache"""
        fastf1.Cache.enable_cache(cache_dir)
        self.driver_ratings = {}
        self.season_data = []
        
    def analyze_2025_season(self, max_races: int = 21) -> Dict:
        """
        Analyze completed 2025 races to generate driver ratings.
        
        Returns:
            Dict with driver ratings across multiple dimensions
        """
        print("📊 Analyzing 2025 season driver performance...")
        
        # Get 2025 schedule
        schedule = fastf1.get_event_schedule(2025)
        completed = schedule[schedule['EventDate'] < datetime.now()]
        
        # Limit to avoid timeout
        races_to_analyze = completed.head(max_races)
        
        driver_stats = {}
        
        for idx, race in races_to_analyze.iterrows():
            race_name = race['EventName']
            
            # Skip testing
            if 'Testing' in race_name:
                continue
                
            print(f"  Analyzing: {race_name}...")
            
            try:
                # Load race session
                session = fastf1.get_session(2025, race_name, 'R')
                session.load(laps=True, telemetry=False, weather=False, messages=False)
                
                if session.laps is None or len(session.laps) == 0:
                    continue
                
                # Analyze each driver
                for driver in session.laps['Driver'].unique():
                    if pd.isna(driver):
                        continue
                        
                    driver_laps = session.laps[session.laps['Driver'] == driver]
                    
                    if len(driver_laps) == 0:
                        continue
                    
                    if driver not in driver_stats:
                        driver_stats[driver] = {
                            'races': 0,
                            'total_laps': 0,
                            'consistent_laps': 0,
                            'fast_laps': 0,
                            'tire_management_score': [],
                            'consistency_score': [],
                            'pace_score': [],
                            'positions': [],
                            'compounds_used': []
                        }
                    
                    # Count valid laps
                    valid_laps = driver_laps[~driver_laps['LapTime'].isna()]
                    
                    if len(valid_laps) < 5:  # Need minimum laps
                        continue
                    
                    driver_stats[driver]['races'] += 1
                    driver_stats[driver]['total_laps'] += len(valid_laps)
                    
                    # Calculate consistency (std deviation of lap times)
                    lap_times = valid_laps['LapTime'].dt.total_seconds()
                    if len(lap_times) > 3:
                        std_dev = lap_times.std()
                        mean_time = lap_times.mean()
                        consistency = max(0, 100 - (std_dev / mean_time * 100))
                        driver_stats[driver]['consistency_score'].append(consistency)
                    
                    # Tire management (lap time degradation over stint)
                    if 'Compound' in valid_laps.columns:
                        for compound in valid_laps['Compound'].unique():
                            if pd.isna(compound):
                                continue
                            compound_laps = valid_laps[valid_laps['Compound'] == compound]
                            if len(compound_laps) >= 5:
                                # Measure degradation
                                times = compound_laps['LapTime'].dt.total_seconds().values
                                if len(times) > 5:
                                    first_5_avg = np.mean(times[:5])
                                    last_5_avg = np.mean(times[-5:])
                                    degradation = (last_5_avg - first_5_avg) / first_5_avg * 100
                                    # Lower degradation = better tire management
                                    tire_mgmt = max(0, 100 - degradation * 10)
                                    driver_stats[driver]['tire_management_score'].append(tire_mgmt)
                                    driver_stats[driver]['compounds_used'].append(compound)
                    
                    # Pace score (comparison to fastest lap)
                    fastest_lap = valid_laps['LapTime'].min()
                    median_lap = valid_laps['LapTime'].median()
                    if fastest_lap.total_seconds() > 0:
                        pace = (fastest_lap.total_seconds() / median_lap.total_seconds()) * 100
                        driver_stats[driver]['pace_score'].append(pace)
                    
                    # Track position
                    if 'Position' in valid_laps.columns:
                        final_pos = valid_laps.iloc[-1]['Position']
                        if not pd.isna(final_pos):
                            driver_stats[driver]['positions'].append(final_pos)
                
            except Exception as e:
                print(f"    ⚠️  Error analyzing {race_name}: {e}")
                continue
        
        # Calculate final ratings
        print("\n🎯 Calculating driver ratings...")
        self.driver_ratings = self._calculate_ratings(driver_stats)
        
        return self.driver_ratings
    
    def _calculate_ratings(self, stats: Dict) -> Dict:
        """Calculate final driver ratings from collected stats"""
        ratings = {}
        
        for driver, data in stats.items():
            if data['races'] < 3:  # Need minimum races
                continue
            
            # Tire management (1-100)
            tire_mgmt = np.mean(data['tire_management_score']) if data['tire_management_score'] else 50
            tire_mgmt = np.clip(tire_mgmt, 0, 100)
            
            # Consistency (1-100)
            consistency = np.mean(data['consistency_score']) if data['consistency_score'] else 50
            consistency = np.clip(consistency, 0, 100)
            
            # Pace (1-100)
            pace = np.mean(data['pace_score']) if data['pace_score'] else 50
            pace = np.clip(pace, 0, 100)
            
            # Overtaking skill (based on position changes - simplified)
            overtaking = 50  # Default, would need lap-by-lap position data
            
            # Wet weather ability (would need weather data per race)
            wet_weather = 50  # Default
            
            # Overall rating (weighted average)
            overall = (
                tire_mgmt * 0.25 +
                consistency * 0.25 +
                pace * 0.30 +
                overtaking * 0.10 +
                wet_weather * 0.10
            )
            
            ratings[driver] = {
                'overall': round(overall, 1),
                'tire_management': round(tire_mgmt, 1),
                'consistency': round(consistency, 1),
                'pace': round(pace, 1),
                'overtaking': round(overtaking, 1),
                'wet_weather': round(wet_weather, 1),
                'races_analyzed': data['races'],
                'total_laps': data['total_laps'],
                'compounds_mastered': list(set(data['compounds_used']))
            }
        
        return ratings
    
    def get_driver_rating(self, driver_code: str) -> Dict:
        """Get rating for specific driver"""
        return self.driver_ratings.get(driver_code, {
            'overall': 50,
            'tire_management': 50,
            'consistency': 50,
            'pace': 50,
            'overtaking': 50,
            'wet_weather': 50,
            'races_analyzed': 0,
            'total_laps': 0,
            'compounds_mastered': []
        })
    
    def get_top_drivers(self, n: int = 10, metric: str = 'overall') -> List:
        """Get top N drivers by metric"""
        sorted_drivers = sorted(
            self.driver_ratings.items(),
            key=lambda x: x[1].get(metric, 0),
            reverse=True
        )
        return sorted_drivers[:n]
    
    def save_ratings(self, filepath: str = './models/driver_ratings_2025.pkl'):
        """Save ratings to file"""
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self.driver_ratings, f)
        print(f"💾 Driver ratings saved: {filepath}")
    
    def load_ratings(self, filepath: str = './models/driver_ratings_2025.pkl'):
        """Load ratings from file"""
        import pickle
        try:
            with open(filepath, 'rb') as f:
                self.driver_ratings = pickle.load(f)
            print(f"✅ Driver ratings loaded: {filepath}")
            return True
        except FileNotFoundError:
            print(f"⚠️  Ratings file not found: {filepath}")
            return False


def main():
    """Generate and save 2025 driver ratings"""
    print("🏎️  2025 F1 Driver Performance Analysis\n")
    
    analyzer = DriverPerformanceAnalyzer()
    
    # Analyze season (limit to 10 races for speed)
    ratings = analyzer.analyze_2025_season(max_races=10)
    
    if not ratings:
        print("❌ No ratings generated")
        return
    
    # Display results
    print(f"\n{'='*80}")
    print("🏆 2025 DRIVER PERFORMANCE RATINGS")
    print(f"{'='*80}\n")
    
    # Top 10 overall
    top_drivers = analyzer.get_top_drivers(10, 'overall')
    
    print("📊 TOP 10 DRIVERS (Overall Rating):\n")
    for i, (driver, rating) in enumerate(top_drivers, 1):
        print(f"{i:2d}. {driver:3s} - {rating['overall']:5.1f}/100")
        print(f"    Tire Mgmt: {rating['tire_management']:5.1f} | "
              f"Consistency: {rating['consistency']:5.1f} | "
              f"Pace: {rating['pace']:5.1f}")
        print(f"    Races: {rating['races_analyzed']} | "
              f"Laps: {rating['total_laps']} | "
              f"Compounds: {', '.join(rating['compounds_mastered'][:3])}")
        print()
    
    # Best tire managers
    print("\n🛞 BEST TIRE MANAGERS:\n")
    tire_masters = analyzer.get_top_drivers(5, 'tire_management')
    for i, (driver, rating) in enumerate(tire_masters, 1):
        print(f"{i}. {driver}: {rating['tire_management']:.1f}/100")
    
    # Most consistent
    print("\n📈 MOST CONSISTENT DRIVERS:\n")
    consistent = analyzer.get_top_drivers(5, 'consistency')
    for i, (driver, rating) in enumerate(consistent, 1):
        print(f"{i}. {driver}: {rating['consistency']:.1f}/100")
    
    # Fastest pace
    print("\n⚡ FASTEST PACE:\n")
    fastest = analyzer.get_top_drivers(5, 'pace')
    for i, (driver, rating) in enumerate(fastest, 1):
        print(f"{i}. {driver}: {rating['pace']:.1f}/100")
    
    # Save ratings
    analyzer.save_ratings()
    
    print(f"\n{'='*80}")
    print("✅ Driver performance analysis complete!")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
