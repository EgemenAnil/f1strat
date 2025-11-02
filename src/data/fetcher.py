"""
F1 Enhanced Data Fetcher
Fetches comprehensive race data including weather, track conditions, and driver performance.
"""

import fastf1
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
import os
from pathlib import Path


class F1DataFetcher:
    """Enhanced F1 data fetcher with weather and track data integration."""
    
    def __init__(self, cache_dir: str = "./cache"):
        """
        Initialize the data fetcher.
        
        Args:
            cache_dir: Directory for caching FastF1 data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        fastf1.Cache.enable_cache(str(self.cache_dir))
        
        # Weather API keys (set via environment variables)
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.weather_api_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    def get_upcoming_race(self) -> Optional[Dict]:
        """
        Get information about the next upcoming F1 race (including today).
        
        Returns:
            Dictionary with race details or None if no upcoming race
        """
        try:
            current_year = datetime.now().year
            schedule = fastf1.get_event_schedule(current_year)
            
            # Get today's date at midnight (start of day)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today = pd.Timestamp(today)
            
            # Find races from today onwards
            upcoming_races = []
            for idx, race in schedule.iterrows():
                race_date = pd.Timestamp(race['Session5Date'])
                
                # Skip if date is NaT (Not a Time)
                if pd.isna(race_date):
                    continue
                    
                # Remove timezone info for comparison
                if race_date.tz is not None:
                    race_date = race_date.tz_localize(None)
                if today.tz is not None:
                    today = today.tz_localize(None)
                    
                # Compare dates only
                if race_date.date() >= today.date():
                    upcoming_races.append(race)
            
            if len(upcoming_races) == 0:
                # Try next year
                schedule = fastf1.get_event_schedule(current_year + 1)
                for idx, race in schedule.iterrows():
                    race_date = pd.Timestamp(race['Session5Date'])
                    
                    # Skip if date is NaT
                    if pd.isna(race_date):
                        continue
                        
                    if race_date.tz is not None:
                        race_date = race_date.tz_localize(None)
                    if race_date.date() >= today.date():
                        upcoming_races.append(race)
            
            if len(upcoming_races) > 0:
                next_race = upcoming_races[0]
                return {
                    'year': pd.Timestamp(next_race['EventDate']).year,
                    'round': next_race['RoundNumber'],
                    'country': next_race['Country'],
                    'location': next_race['Location'],
                    'event_name': next_race['EventName'],
                    'race_name': next_race['EventName'],  # For compatibility
                    'circuit': next_race['Location'],  # For compatibility
                    'date': next_race['Session5Date'],  # For compatibility
                    'race_date': next_race['Session5Date'],
                    'quali_date': next_race['Session4Date'],
                    'fp1_date': next_race['Session1Date'],
                    'fp2_date': next_race['Session2Date'],
                    'fp3_date': next_race['Session3Date'],
                    'total_laps': 57,  # Default, will be updated with actual data
                }
            return None
            
        except Exception as e:
            print(f"Error fetching upcoming race: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_historical_race_data(self, year: int, race: str, 
                                 session: str = 'R') -> pd.DataFrame:
        """
        Fetch comprehensive historical race data.
        
        Args:
            year: Season year
            race: Race name or round number
            session: Session type ('FP1', 'FP2', 'FP3', 'Q', 'R', 'S', 'SS')
        
        Returns:
            DataFrame with enhanced lap data
        """
        try:
            # Load session
            session_data = fastf1.get_session(year, race, session)
            session_data.load()
            
            # Get laps
            laps = session_data.laps
            
            # Add weather data
            weather = session_data.weather_data
            if weather is not None and len(weather) > 0:
                # Merge weather data with laps based on time
                laps = self._merge_weather_data(laps, weather)
            
            # Add track status
            track_status = session_data.track_status
            if track_status is not None and len(track_status) > 0:
                laps = self._merge_track_status(laps, track_status)
            
            # Add session info
            laps['Session'] = session
            laps['Year'] = year
            laps['EventName'] = session_data.event['EventName']
            laps['CircuitKey'] = session_data.event.get('Circuit', 'Unknown')
            
            return laps
            
        except Exception as e:
            print(f"Error fetching race data: {e}")
            return pd.DataFrame()
    
    def _merge_weather_data(self, laps: pd.DataFrame, 
                           weather: pd.DataFrame) -> pd.DataFrame:
        """Merge weather data with lap data."""
        try:
            # Convert time columns to datetime if needed
            if 'Time' in laps.columns and 'Time' in weather.columns:
                # Merge based on nearest time
                weather_cols = ['AirTemp', 'Humidity', 'Pressure', 'Rainfall', 
                               'TrackTemp', 'WindDirection', 'WindSpeed']
                
                available_cols = [col for col in weather_cols if col in weather.columns]
                
                if available_cols:
                    # Simple merge by session time (can be improved)
                    for col in available_cols:
                        if col in weather.columns:
                            # Use mean values for now
                            laps[col] = weather[col].mean()
            
            return laps
        except Exception as e:
            print(f"Error merging weather data: {e}")
            return laps
    
    def _merge_track_status(self, laps: pd.DataFrame, 
                           track_status: pd.DataFrame) -> pd.DataFrame:
        """Merge track status data with lap data."""
        try:
            if 'Time' in laps.columns and 'Time' in track_status.columns:
                # Add track status indicators
                # 1 = Track clear, 2 = Yellow flag, 4 = Safety Car, 5 = Red Flag, 6 = VSC, 7 = VSC Ending
                laps['TrackStatus'] = 1  # Default: clear track
                
                # This can be enhanced with proper time-based merging
                
            return laps
        except Exception as e:
            print(f"Error merging track status: {e}")
            return laps
    
    def get_weather_forecast(self, lat: float, lon: float, 
                            race_date: datetime) -> Optional[Dict]:
        """
        Get weather forecast for race day.
        
        Args:
            lat: Latitude of circuit
            lon: Longitude of circuit
            race_date: Date of the race
        
        Returns:
            Weather forecast data
        """
        if not self.weather_api_key:
            print("Warning: OPENWEATHER_API_KEY not set. Cannot fetch weather forecast.")
            return None
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.weather_api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Find forecast closest to race time
            forecasts = data.get('list', [])
            race_forecast = None
            min_time_diff = float('inf')
            
            for forecast in forecasts:
                forecast_time = datetime.fromtimestamp(forecast['dt'])
                time_diff = abs((forecast_time - race_date).total_seconds())
                
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    race_forecast = forecast
            
            if race_forecast:
                return {
                    'temperature': race_forecast['main']['temp'],
                    'humidity': race_forecast['main']['humidity'],
                    'pressure': race_forecast['main']['pressure'],
                    'weather': race_forecast['weather'][0]['main'],
                    'description': race_forecast['weather'][0]['description'],
                    'wind_speed': forecast.get('wind', {}).get('speed', 0),
                    'wind_deg': forecast.get('wind', {}).get('deg', 0),
                    'rain_3h': forecast.get('rain', {}).get('3h', 0),
                    'clouds': forecast['clouds']['all'],
                }
            
            return None
            
        except Exception as e:
            print(f"Error fetching weather forecast: {e}")
            return None
    
    def get_driver_standings(self, year: int) -> pd.DataFrame:
        """Get current driver championship standings."""
        try:
            # This would require additional API or web scraping
            # For now, returning placeholder
            print(f"Driver standings for {year} - requires implementation")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching driver standings: {e}")
            return pd.DataFrame()
    
    def get_constructor_standings(self, year: int) -> pd.DataFrame:
        """Get current constructor championship standings."""
        try:
            # Placeholder - requires implementation
            print(f"Constructor standings for {year} - requires implementation")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching constructor standings: {e}")
            return pd.DataFrame()


# Track coordinates database (for weather forecasting)
TRACK_COORDINATES = {
    'Bahrain': {'lat': 26.0325, 'lon': 50.5106},
    'Saudi Arabia': {'lat': 21.6319, 'lon': 39.1044},
    'Australia': {'lat': -37.8497, 'lon': 144.9680},
    'Azerbaijan': {'lat': 40.3725, 'lon': 49.8533},
    'Miami': {'lat': 25.9581, 'lon': -80.2389},
    'Monaco': {'lat': 43.7347, 'lon': 7.4206},
    'Spain': {'lat': 41.5700, 'lon': 2.2611},
    'Canada': {'lat': 45.5000, 'lon': -73.5228},
    'Austria': {'lat': 47.2197, 'lon': 14.7647},
    'Great Britain': {'lat': 52.0786, 'lon': -1.0169},
    'Hungary': {'lat': 47.5789, 'lon': 19.2486},
    'Belgium': {'lat': 50.4372, 'lon': 5.9714},
    'Netherlands': {'lat': 52.3888, 'lon': 4.5409},
    'Italy': {'lat': 45.6156, 'lon': 9.2811},
    'Singapore': {'lat': 1.2914, 'lon': 103.8640},
    'Japan': {'lat': 34.8431, 'lon': 136.5408},
    'Qatar': {'lat': 25.4900, 'lon': 51.4542},
    'United States': {'lat': 30.1328, 'lon': -97.6411},
    'Mexico': {'lat': 19.4042, 'lon': -99.0907},
    'Brazil': {'lat': -23.7036, 'lon': -46.6997},
    'São Paulo': {'lat': -23.7036, 'lon': -46.6997},  # Interlagos
    'Las Vegas': {'lat': 36.1147, 'lon': -115.1728},
    'Abu Dhabi': {'lat': 24.4672, 'lon': 54.6031},
}


if __name__ == "__main__":
    # Test the fetcher
    fetcher = F1DataFetcher()
    
    # Get upcoming race
    upcoming = fetcher.get_upcoming_race()
    if upcoming:
        print(f"Next race: {upcoming['event_name']} on {upcoming['race_date']}")
    
    # Get historical data example
    laps = fetcher.get_historical_race_data(2023, 'Bahrain', 'R')
    if not laps.empty:
        print(f"Loaded {len(laps)} laps from 2023 Bahrain GP")
        print(laps.head())
