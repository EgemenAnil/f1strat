"""
Test Data Integration (Weather, Calendar, etc.)
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.race_calendar import RaceCalendar
from src.data.weather import WeatherAPI


class TestRaceCalendar:
    """Test race calendar functionality."""
    
    @pytest.fixture
    def calendar(self):
        """Create calendar instance."""
        return RaceCalendar()
    
    def test_get_next_race(self, calendar):
        """Test getting next race."""
        next_race = calendar.get_next_race()
        
        assert next_race is not None
        assert 'name' in next_race
        assert 'location' in next_race
        assert 'date' in next_race
    
    def test_get_race_by_name(self, calendar):
        """Test getting race by name."""
        race = calendar.get_race_by_name('Monaco')
        
        if race:  # Monaco might not be in current calendar
            assert 'name' in race
            assert 'location' in race


class TestWeatherAPI:
    """Test weather API integration."""
    
    @pytest.fixture
    def weather_api(self):
        """Create weather API instance."""
        return WeatherAPI()
    
    def test_get_weather_forecast(self, weather_api):
        """Test weather forecast retrieval."""
        # Test with known location
        forecast = weather_api.get_forecast(
            location='Bahrain',
            date='2025-03-01'
        )
        
        # Should return forecast or None (if API key not set)
        if forecast:
            assert 'temperature' in forecast or 'temp' in forecast
    
    def test_api_key_optional(self, weather_api):
        """Test that system works without API key."""
        # Should not raise error even without API key
        forecast = weather_api.get_forecast(
            location='Monaco',
            date='2025-05-01'
        )
        
        # Might be None without API key, but shouldn't crash
        assert forecast is None or isinstance(forecast, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
