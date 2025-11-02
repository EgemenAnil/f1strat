"""
Enhanced F1 Data Services
Advanced data fetching for qualifying, practice sessions, tire allocations, and weather.
"""

import fastf1
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .fetcher import F1DataFetcher, TRACK_COORDINATES


class EnhancedF1DataService:
    """Enhanced F1 data service with qualifying, practice, weather, and tire data."""
    
    def __init__(self, cache_dir: str = "./cache"):
        """Initialize enhanced data service."""
        self.cache_dir = Path(cache_dir)
        self.fetcher = F1DataFetcher(cache_dir)
        
    def get_qualifying_data(self, year: int, race: str) -> Optional[Dict]:
        """
        Get qualifying session data including grid positions and lap times.
        
        Args:
            year: Season year
            race: Race name or round number
            
        Returns:
            Dictionary with qualifying data or None if not available
        """
        try:
            print(f"📊 Fetching qualifying data for {race} {year}...")
            
            # Load qualifying session
            quali_session = fastf1.get_session(year, race, 'Q')
            quali_session.load()
            
            # Get results
            results = quali_session.results
            
            if results is None or len(results) == 0:
                print("⚠️  No qualifying data available yet")
                return None
            
            # Extract relevant data
            quali_data = {
                'session_status': 'Completed',
                'grid_positions': {},
                'quali_times': {},
                'q1_times': {},
                'q2_times': {},
                'q3_times': {},
                'team_performance': {}
            }
            
            for idx, driver in results.iterrows():
                driver_code = driver.get('Abbreviation', driver.get('DriverNumber', 'UNK'))
                
                quali_data['grid_positions'][driver_code] = driver.get('Position', 20)
                quali_data['quali_times'][driver_code] = driver.get('Q3', driver.get('Q2', driver.get('Q1')))
                quali_data['q1_times'][driver_code] = driver.get('Q1')
                quali_data['q2_times'][driver_code] = driver.get('Q2')
                quali_data['q3_times'][driver_code] = driver.get('Q3')
                quali_data['team_performance'][driver.get('TeamName', 'Unknown')] = driver.get('Position', 20)
            
            # Calculate pole time
            if 'Q3' in results.columns:
                pole_time = results['Q3'].min()
                quali_data['pole_time'] = pole_time
                
            print(f"✅ Qualifying data loaded: {len(quali_data['grid_positions'])} drivers")
            
            return quali_data
            
        except Exception as e:
            print(f"⚠️  Qualifying data not available: {e}")
            return None
    
    def get_practice_session_data(self, year: int, race: str, 
                                   sessions: List[str] = ['FP1', 'FP2', 'FP3']) -> Optional[Dict]:
        """
        Get practice session data for tire degradation and performance analysis.
        
        Args:
            year: Season year
            race: Race name or round number
            sessions: List of practice sessions to analyze
            
        Returns:
            Dictionary with practice session analytics
        """
        try:
            print(f"🔧 Fetching practice session data for {race} {year}...")
            
            practice_data = {
                'sessions_analyzed': [],
                'tire_degradation': {},
                'compound_performance': {},
                'lap_time_averages': {},
                'fuel_corrected_times': {},
                'long_run_pace': {}
            }
            
            for session_name in sessions:
                try:
                    session = fastf1.get_session(year, race, session_name)
                    session.load()
                    
                    laps = session.laps
                    
                    if laps is None or len(laps) == 0:
                        print(f"⚠️  {session_name}: No data available")
                        continue
                    
                    practice_data['sessions_analyzed'].append(session_name)
                    
                    # Analyze tire degradation
                    tire_deg = self._analyze_tire_degradation(laps)
                    practice_data['tire_degradation'][session_name] = tire_deg
                    
                    # Analyze compound performance
                    compound_perf = self._analyze_compound_performance(laps)
                    practice_data['compound_performance'][session_name] = compound_perf
                    
                    # Calculate average lap times
                    avg_times = self._calculate_average_lap_times(laps)
                    practice_data['lap_time_averages'][session_name] = avg_times
                    
                    # Estimate long run pace
                    long_run = self._analyze_long_run_pace(laps)
                    practice_data['long_run_pace'][session_name] = long_run
                    
                    print(f"✅ {session_name} analyzed: {len(laps)} laps")
                    
                except Exception as e:
                    print(f"⚠️  {session_name} not available: {e}")
                    continue
            
            if len(practice_data['sessions_analyzed']) == 0:
                print("⚠️  No practice session data available")
                return None
            
            print(f"✅ Practice data loaded: {len(practice_data['sessions_analyzed'])} sessions")
            
            return practice_data
            
        except Exception as e:
            print(f"⚠️  Practice session data error: {e}")
            return None
    
    def _analyze_tire_degradation(self, laps: pd.DataFrame) -> Dict:
        """Analyze tire degradation from lap data."""
        try:
            degradation = {}
            
            # Group by driver and stint
            for driver in laps['Driver'].unique():
                driver_laps = laps[laps['Driver'] == driver]
                
                # Identify stints (consecutive laps on same tire)
                stints = []
                current_stint = []
                prev_compound = None
                
                for idx, lap in driver_laps.iterrows():
                    compound = lap.get('Compound', 'UNKNOWN')
                    
                    if compound != prev_compound and len(current_stint) > 0:
                        stints.append(current_stint)
                        current_stint = []
                    
                    current_stint.append({
                        'lap_number': lap.get('LapNumber', 0),
                        'lap_time': lap.get('LapTime', pd.Timedelta(0)).total_seconds(),
                        'compound': compound,
                        'tire_life': lap.get('TyreLife', 0)
                    })
                    prev_compound = compound
                
                if len(current_stint) > 0:
                    stints.append(current_stint)
                
                # Calculate degradation per stint
                for stint in stints:
                    if len(stint) >= 5:  # Need at least 5 laps for meaningful data
                        compound = stint[0]['compound']
                        
                        # Calculate degradation rate (seconds per lap)
                        lap_times = [s['lap_time'] for s in stint if s['lap_time'] > 0]
                        if len(lap_times) >= 5:
                            # Simple linear fit
                            x = np.arange(len(lap_times))
                            y = np.array(lap_times)
                            
                            # Remove outliers (safety car, traffic, etc.)
                            median = np.median(y)
                            mad = np.median(np.abs(y - median))
                            mask = np.abs(y - median) < 3 * mad
                            
                            if mask.sum() >= 3:
                                x_clean = x[mask]
                                y_clean = y[mask]
                                
                                # Linear regression
                                if len(x_clean) >= 3:
                                    slope, intercept = np.polyfit(x_clean, y_clean, 1)
                                    
                                    if compound not in degradation:
                                        degradation[compound] = []
                                    
                                    degradation[compound].append({
                                        'degradation_rate': slope,
                                        'base_time': intercept,
                                        'stint_length': len(stint),
                                        'driver': driver
                                    })
            
            # Average degradation per compound
            avg_degradation = {}
            for compound, data_list in degradation.items():
                rates = [d['degradation_rate'] for d in data_list]
                avg_degradation[compound] = {
                    'avg_degradation': np.mean(rates),
                    'std_degradation': np.std(rates),
                    'samples': len(rates)
                }
            
            return avg_degradation
            
        except Exception as e:
            print(f"Error analyzing tire degradation: {e}")
            return {}
    
    def _analyze_compound_performance(self, laps: pd.DataFrame) -> Dict:
        """Analyze performance of different tire compounds."""
        try:
            performance = {}
            
            for compound in laps['Compound'].unique():
                if pd.isna(compound) or compound == 'UNKNOWN':
                    continue
                
                compound_laps = laps[laps['Compound'] == compound]
                
                # Get valid lap times (exclude outliers)
                lap_times = compound_laps['LapTime'].dropna()
                lap_times_sec = [lt.total_seconds() for lt in lap_times if lt.total_seconds() > 0]
                
                if len(lap_times_sec) >= 3:
                    # Remove extreme outliers
                    median = np.median(lap_times_sec)
                    mad = np.median(np.abs(np.array(lap_times_sec) - median))
                    clean_times = [t for t in lap_times_sec if abs(t - median) < 3 * mad]
                    
                    if len(clean_times) >= 3:
                        performance[compound] = {
                            'avg_lap_time': np.mean(clean_times),
                            'best_lap_time': np.min(clean_times),
                            'std_lap_time': np.std(clean_times),
                            'total_laps': len(compound_laps)
                        }
            
            return performance
            
        except Exception as e:
            print(f"Error analyzing compound performance: {e}")
            return {}
    
    def _calculate_average_lap_times(self, laps: pd.DataFrame) -> Dict:
        """Calculate average lap times per driver."""
        try:
            avg_times = {}
            
            for driver in laps['Driver'].unique():
                driver_laps = laps[laps['Driver'] == driver]
                lap_times = driver_laps['LapTime'].dropna()
                lap_times_sec = [lt.total_seconds() for lt in lap_times if lt.total_seconds() > 0]
                
                if len(lap_times_sec) >= 3:
                    avg_times[driver] = {
                        'avg': np.mean(lap_times_sec),
                        'best': np.min(lap_times_sec),
                        'std': np.std(lap_times_sec)
                    }
            
            return avg_times
            
        except Exception as e:
            print(f"Error calculating average lap times: {e}")
            return {}
    
    def _analyze_long_run_pace(self, laps: pd.DataFrame) -> Dict:
        """Analyze long run pace (stints of 10+ laps)."""
        try:
            long_runs = {}
            
            for driver in laps['Driver'].unique():
                driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
                
                # Find long stints (10+ laps on same tire)
                current_stint = []
                prev_compound = None
                
                for idx, lap in driver_laps.iterrows():
                    compound = lap.get('Compound', 'UNKNOWN')
                    
                    if compound != prev_compound:
                        # Analyze previous stint if long enough
                        if len(current_stint) >= 10:
                            lap_times = [s['time'] for s in current_stint]
                            avg_pace = np.mean(lap_times)
                            
                            if prev_compound not in long_runs:
                                long_runs[prev_compound] = []
                            
                            long_runs[prev_compound].append({
                                'driver': driver,
                                'avg_pace': avg_pace,
                                'stint_length': len(current_stint)
                            })
                        
                        current_stint = []
                    
                    lap_time = lap.get('LapTime')
                    if pd.notna(lap_time) and lap_time.total_seconds() > 0:
                        current_stint.append({
                            'time': lap_time.total_seconds(),
                            'compound': compound
                        })
                    
                    prev_compound = compound
            
            return long_runs
            
        except Exception as e:
            print(f"Error analyzing long run pace: {e}")
            return {}
    
    def get_pirelli_tire_allocation(self, year: int, race: str) -> Optional[Dict]:
        """
        Get Pirelli tire compound allocation for the race.
        
        Args:
            year: Season year
            race: Race name
            
        Returns:
            Dictionary with tire allocation information
        """
        try:
            print(f"🛞 Fetching Pirelli tire allocation for {race} {year}...")
            
            # Load any session to get tire info
            session = fastf1.get_session(year, race, 'R')
            session.load()
            
            # Get tire compounds used
            laps = session.laps
            
            if laps is None or len(laps) == 0:
                print("⚠️  No tire data available")
                return None
            
            compounds_used = laps['Compound'].unique()
            compounds_used = [c for c in compounds_used if pd.notna(c) and c != 'UNKNOWN']
            
            tire_allocation = {
                'year': year,
                'race': race,
                'compounds': compounds_used,
                'soft': 'SOFT' in compounds_used,
                'medium': 'MEDIUM' in compounds_used,
                'hard': 'HARD' in compounds_used,
                'intermediate': 'INTERMEDIATE' in compounds_used,
                'wet': 'WET' in compounds_used
            }
            
            # Try to map to C1-C5 designation (this would need Pirelli API or web scraping)
            # For now, just detect what's available
            print(f"✅ Tire allocation: {', '.join(compounds_used)}")
            
            return tire_allocation
            
        except Exception as e:
            print(f"⚠️  Tire allocation data not available: {e}")
            return None
    
    def get_enhanced_weather_forecast(self, race_info: Dict) -> Optional[Dict]:
        """
        Get enhanced weather forecast with race-specific details.
        
        Args:
            race_info: Race information dictionary
            
        Returns:
            Enhanced weather forecast
        """
        try:
            location = race_info.get('location', race_info.get('country'))
            
            # Get coordinates
            coords = TRACK_COORDINATES.get(location)
            
            if not coords:
                print(f"⚠️  No coordinates found for {location}")
                return None
            
            # Get forecast
            race_date = race_info.get('race_date', race_info.get('date'))
            
            weather = self.fetcher.get_weather_forecast(
                coords['lat'], 
                coords['lon'], 
                race_date
            )
            
            if weather:
                # Enhance with race-specific info
                weather['location'] = location
                weather['race_date'] = race_date
                weather['coordinates'] = coords
                
                # Add rain probability assessment
                rain_prob = 0
                if weather.get('rain_3h', 0) > 0:
                    rain_prob = 70
                elif weather.get('weather') == 'Rain':
                    rain_prob = 80
                elif weather.get('weather') == 'Clouds':
                    rain_prob = 30
                
                weather['rain_probability'] = rain_prob
                
                print(f"✅ Weather forecast: {weather.get('temperature')}°C, "
                      f"{weather.get('description')}, Rain: {rain_prob}%")
                
                return weather
            
            return None
            
        except Exception as e:
            print(f"⚠️  Weather forecast error: {e}")
            return None
    
    def get_complete_race_context(self, year: int, race: str, 
                                   race_info: Optional[Dict] = None) -> Dict:
        """
        Get complete race context including all enhanced data.
        
        Args:
            year: Season year
            race: Race name
            race_info: Optional race info (for weather)
            
        Returns:
            Complete race context dictionary
        """
        print(f"\n🔍 Fetching complete race context for {race} {year}...")
        
        context = {
            'year': year,
            'race': race,
            'qualifying': None,
            'practice': None,
            'tire_allocation': None,
            'weather': None,
            'data_completeness': 0.0
        }
        
        # Get qualifying data
        quali = self.get_qualifying_data(year, race)
        if quali:
            context['qualifying'] = quali
            context['data_completeness'] += 0.25
        
        # Get practice data
        practice = self.get_practice_session_data(year, race)
        if practice:
            context['practice'] = practice
            context['data_completeness'] += 0.25
        
        # Get tire allocation
        tires = self.get_pirelli_tire_allocation(year, race)
        if tires:
            context['tire_allocation'] = tires
            context['data_completeness'] += 0.25
        
        # Get weather forecast
        if race_info:
            weather = self.get_enhanced_weather_forecast(race_info)
            if weather:
                context['weather'] = weather
                context['data_completeness'] += 0.25
        
        print(f"\n📊 Data completeness: {context['data_completeness']*100:.0f}%")
        
        return context


if __name__ == "__main__":
    # Test enhanced services
    service = EnhancedF1DataService()
    
    # Test with Bahrain 2023
    context = service.get_complete_race_context(2023, 'Bahrain')
    
    print("\n" + "="*80)
    print("ENHANCED DATA CONTEXT")
    print("="*80)
    print(f"Data completeness: {context['data_completeness']*100:.0f}%")
    
    if context['qualifying']:
        print(f"\n✅ Qualifying: {len(context['qualifying']['grid_positions'])} drivers")
    
    if context['practice']:
        print(f"✅ Practice: {len(context['practice']['sessions_analyzed'])} sessions")
    
    if context['tire_allocation']:
        print(f"✅ Tires: {', '.join(context['tire_allocation']['compounds'])}")
    
    if context['weather']:
        print(f"✅ Weather: {context['weather']['temperature']}°C")
