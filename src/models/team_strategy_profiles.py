"""
Team Strategy Profiles based on 2025 Season Data
Analyzes real 2025 race data to identify team strategy patterns
"""

import fastf1
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class TeamStrategyAnalyzer:
    """Analyzes team strategy patterns from 2025 season data"""
    
    def __init__(self, cache_dir: str = './cache'):
        """Initialize with FastF1 cache"""
        import os
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        fastf1.Cache.enable_cache(cache_dir)
        self.team_profiles = {}
        
    def analyze_2025_season(self, max_races: int = 21) -> Dict:
        """
        Analyze completed 2025 races to generate team strategy profiles.
        
        Returns:
            Dict with team strategy patterns and preferences
        """
        print("🏁 Analyzing 2025 season team strategies...")
        
        # Get 2025 schedule
        schedule = fastf1.get_event_schedule(2025)
        completed = schedule[schedule['EventDate'] < datetime.now()]
        
        # Limit to avoid timeout
        races_to_analyze = completed.head(max_races)
        
        team_stats = defaultdict(lambda: {
            'races': 0,
            'pit_stops': [],
            'pit_laps': [],
            'strategies': [],
            'compounds_used': [],
            'undercuts': 0,
            'overcuts': 0,
            'early_stops': 0,  # Before lap 15
            'late_stops': 0,   # After lap 35
            'one_stops': 0,
            'two_stops': 0,
            'three_stops': 0,
            'avg_pit_duration': [],
            'tire_preferences': defaultdict(int)
        })
        
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
                
                # Get race results
                results = session.results
                if results is None or len(results) == 0:
                    continue
                
                # Analyze each team
                for team in session.laps['Team'].unique():
                    if pd.isna(team):
                        continue
                    
                    team_laps = session.laps[session.laps['Team'] == team]
                    
                    if len(team_laps) == 0:
                        continue
                    
                    team_stats[team]['races'] += 1
                    
                    # Analyze pit stops for team drivers
                    for driver in team_laps['Driver'].unique():
                        if pd.isna(driver):
                            continue
                        
                        driver_laps = team_laps[team_laps['Driver'] == driver]
                        valid_laps = driver_laps[~driver_laps['LapTime'].isna()]
                        
                        if len(valid_laps) < 5:
                            continue
                        
                        # Detect pit stops (compound changes)
                        if 'Compound' in valid_laps.columns:
                            compounds = valid_laps['Compound'].tolist()
                            pit_laps_detected = []
                            
                            for i in range(1, len(compounds)):
                                if compounds[i] != compounds[i-1] and not pd.isna(compounds[i]):
                                    pit_lap = valid_laps.iloc[i]['LapNumber']
                                    pit_laps_detected.append(pit_lap)
                                    
                                    # Track pit timing preference
                                    if pit_lap < 15:
                                        team_stats[team]['early_stops'] += 1
                                    elif pit_lap > 35:
                                        team_stats[team]['late_stops'] += 1
                            
                            # Count stops
                            num_stops = len(pit_laps_detected)
                            if num_stops == 1:
                                team_stats[team]['one_stops'] += 1
                            elif num_stops == 2:
                                team_stats[team]['two_stops'] += 1
                            elif num_stops >= 3:
                                team_stats[team]['three_stops'] += 1
                            
                            team_stats[team]['pit_laps'].extend(pit_laps_detected)
                            team_stats[team]['pit_stops'].append(num_stops)
                            
                            # Track compound preferences
                            for compound in set(compounds):
                                if not pd.isna(compound):
                                    team_stats[team]['tire_preferences'][compound] += 1
                                    team_stats[team]['compounds_used'].append(compound)
                        
                        # Pit stop duration
                        if 'PitInTime' in valid_laps.columns and 'PitOutTime' in valid_laps.columns:
                            pit_durations = valid_laps[~valid_laps['PitInTime'].isna()]
                            for _, lap in pit_durations.iterrows():
                                if not pd.isna(lap['PitOutTime']) and not pd.isna(lap['PitInTime']):
                                    duration = (lap['PitOutTime'] - lap['PitInTime']).total_seconds()
                                    if 15 < duration < 60:  # Reasonable pit stop duration
                                        team_stats[team]['avg_pit_duration'].append(duration)
                
            except Exception as e:
                print(f"    ⚠️  Error analyzing {race_name}: {e}")
                continue
        
        # Calculate final profiles
        print("\n🎯 Calculating team strategy profiles...")
        self.team_profiles = self._calculate_profiles(team_stats)
        
        return self.team_profiles
    
    def _calculate_profiles(self, stats: Dict) -> Dict:
        """Calculate final team strategy profiles from collected stats"""
        profiles = {}
        
        for team, data in stats.items():
            if data['races'] < 3:  # Need minimum races
                continue
            
            # Calculate average pit stop count
            avg_stops = np.mean(data['pit_stops']) if data['pit_stops'] else 1.5
            
            # Calculate average pit lap
            avg_pit_lap = np.mean(data['pit_laps']) if data['pit_laps'] else 20
            
            # Calculate average pit duration
            avg_pit_duration = np.mean(data['avg_pit_duration']) if data['avg_pit_duration'] else 24.0
            
            # Determine strategy preference
            total_strategies = data['one_stops'] + data['two_stops'] + data['three_stops']
            if total_strategies > 0:
                one_stop_pct = (data['one_stops'] / total_strategies) * 100
                two_stop_pct = (data['two_stops'] / total_strategies) * 100
                three_stop_pct = (data['three_stops'] / total_strategies) * 100
            else:
                one_stop_pct = two_stop_pct = three_stop_pct = 0
            
            # Determine aggressiveness (early vs late stops)
            total_timed_stops = data['early_stops'] + data['late_stops']
            if total_timed_stops > 0:
                aggressiveness = (data['early_stops'] / total_timed_stops) * 100
            else:
                aggressiveness = 50  # Neutral
            
            # Preferred compounds
            tire_prefs = sorted(
                data['tire_preferences'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            preferred_compounds = [comp for comp, _ in tire_prefs[:3]]
            
            # Strategy style classification
            if avg_stops < 1.3:
                style = 'conservative'
            elif avg_stops > 1.7:
                style = 'aggressive'
            else:
                style = 'balanced'
            
            # Undercut/overcut preference (simplified - would need lap-by-lap positions)
            undercut_preference = 50  # Default neutral
            
            profiles[team] = {
                'style': style,
                'avg_pit_stops': round(avg_stops, 2),
                'avg_pit_lap': round(avg_pit_lap, 1),
                'avg_pit_duration': round(avg_pit_duration, 2),
                'aggressiveness': round(aggressiveness, 1),
                'one_stop_rate': round(one_stop_pct, 1),
                'two_stop_rate': round(two_stop_pct, 1),
                'three_stop_rate': round(three_stop_pct, 1),
                'preferred_compounds': preferred_compounds,
                'undercut_preference': round(undercut_preference, 1),
                'races_analyzed': data['races'],
                'characteristics': self._get_team_characteristics(
                    style, aggressiveness, avg_stops, avg_pit_lap
                )
            }
        
        return profiles
    
    def _get_team_characteristics(self, style: str, aggressiveness: float, 
                                   avg_stops: float, avg_pit_lap: float) -> List[str]:
        """Generate text descriptions of team characteristics"""
        chars = []
        
        if style == 'conservative':
            chars.append("Prefers fewer pit stops")
        elif style == 'aggressive':
            chars.append("Willing to take multi-stop risks")
        else:
            chars.append("Balanced strategy approach")
        
        if aggressiveness > 60:
            chars.append("Early undercut attempts")
        elif aggressiveness < 40:
            chars.append("Patient, waits for optimal window")
        else:
            chars.append("Flexible pit timing")
        
        if avg_pit_lap < 18:
            chars.append("Quick to pit if needed")
        elif avg_pit_lap > 25:
            chars.append("Extends first stint")
        
        return chars
    
    def get_team_profile(self, team_name: str) -> Dict:
        """Get strategy profile for specific team"""
        return self.team_profiles.get(team_name, {
            'style': 'balanced',
            'avg_pit_stops': 1.5,
            'avg_pit_lap': 20,
            'avg_pit_duration': 24.0,
            'aggressiveness': 50,
            'one_stop_rate': 50,
            'two_stop_rate': 40,
            'three_stop_rate': 10,
            'preferred_compounds': ['MEDIUM', 'SOFT'],
            'undercut_preference': 50,
            'races_analyzed': 0,
            'characteristics': ['Balanced strategy approach']
        })
    
    def get_pit_stop_duration(self, team_name: str) -> float:
        """Get average pit stop duration for team"""
        profile = self.get_team_profile(team_name)
        return profile.get('avg_pit_duration', 24.0)
    
    def save_profiles(self, filepath: str = './models/team_profiles_2025.pkl'):
        """Save profiles to file"""
        import pickle
        import os
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.team_profiles, f)
        print(f"💾 Team profiles saved: {filepath}")
    
    def load_profiles(self, filepath: str = './models/team_profiles_2025.pkl'):
        """Load profiles from file"""
        import pickle
        try:
            with open(filepath, 'rb') as f:
                self.team_profiles = pickle.load(f)
            print(f"✅ Team profiles loaded: {filepath}")
            return True
        except FileNotFoundError:
            print(f"⚠️  Profiles file not found: {filepath}")
            return False


def main():
    """Generate and save 2025 team strategy profiles"""
    print("🏁 2025 F1 Team Strategy Profile Analysis\n")
    
    analyzer = TeamStrategyAnalyzer()
    
    # Analyze season (limit to 10 races for speed)
    profiles = analyzer.analyze_2025_season(max_races=10)
    
    if not profiles:
        print("❌ No profiles generated")
        return
    
    # Display results
    print(f"\n{'='*80}")
    print("🏆 2025 TEAM STRATEGY PROFILES")
    print(f"{'='*80}\n")
    
    # Sort teams by name
    sorted_teams = sorted(profiles.items(), key=lambda x: x[0])
    
    for team, profile in sorted_teams:
        print(f"🏁 {team}")
        print(f"   Style: {profile['style'].upper()}")
        print(f"   Avg Pit Stops: {profile['avg_pit_stops']}")
        print(f"   Avg Pit Lap: {profile['avg_pit_lap']}")
        print(f"   Avg Pit Duration: {profile['avg_pit_duration']:.2f}s")
        print(f"   Aggressiveness: {profile['aggressiveness']:.1f}/100")
        print(f"   Strategy Distribution:")
        print(f"      1-stop: {profile['one_stop_rate']:.1f}%")
        print(f"      2-stop: {profile['two_stop_rate']:.1f}%")
        print(f"      3-stop: {profile['three_stop_rate']:.1f}%")
        print(f"   Preferred Compounds: {', '.join(profile['preferred_compounds'])}")
        print(f"   Characteristics:")
        for char in profile['characteristics']:
            print(f"      • {char}")
        print(f"   Races Analyzed: {profile['races_analyzed']}")
        print()
    
    # Summary statistics
    print(f"\n{'='*80}")
    print("📊 SUMMARY STATISTICS")
    print(f"{'='*80}\n")
    
    all_pit_durations = [p['avg_pit_duration'] for p in profiles.values()]
    print(f"Average pit stop duration across all teams: {np.mean(all_pit_durations):.2f}s")
    print(f"Fastest team: {min(all_pit_durations):.2f}s")
    print(f"Slowest team: {max(all_pit_durations):.2f}s")
    
    # Save profiles
    analyzer.save_profiles()
    
    print(f"\n{'='*80}")
    print("✅ Team strategy analysis complete!")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
