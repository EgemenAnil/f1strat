"""
Crash and incident probability prediction for F1 races.
Models safety car, VSC, and red flag probabilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib


class CrashPredictor:
    """Predict crash and incident probabilities during F1 races."""
    
    def __init__(self):
        """Initialize crash predictor."""
        self.model = None
        self.scaler = StandardScaler()
        
        # Historical incident rates by circuit
        self.circuit_incident_rates = {
            'Monaco': 0.85,
            'Singapore': 0.75,
            'Azerbaijan': 0.70,
            'Saudi Arabia': 0.65,
            'Miami': 0.60,
            'Canada': 0.60,
            'Australia': 0.55,
            'Bahrain': 0.45,
            'Las Vegas': 0.50,
            'Brazil': 0.55,
            'Belgium': 0.50,
            'Great Britain': 0.40,
            'Italy': 0.35,
            'Austria': 0.35,
        }
    
    def calculate_lap_incident_probability(self, lap_number: int,
                                          total_laps: int,
                                          weather: Optional[Dict] = None,
                                          track_name: str = "Unknown") -> Dict[str, float]:
        """
        Calculate incident probability for a specific lap.
        
        Args:
            lap_number: Current lap number
            total_laps: Total race laps
            weather: Weather conditions
            track_name: Circuit name
        
        Returns:
            Dictionary with incident probabilities
        """
        # Base incident rate
        base_rate = 0.01  # 1% per lap base
        
        # Track-specific multiplier
        track_multiplier = self.circuit_incident_rates.get(track_name, 0.5)
        
        # Lap-specific factors
        lap_factor = 1.0
        
        # First lap is most dangerous
        if lap_number == 1:
            lap_factor = 5.0
        # First 3 laps have elevated risk
        elif lap_number <= 3:
            lap_factor = 2.5
        # Restarts after safety car
        elif lap_number > 1:  # Check if previous lap had incident (simplified)
            lap_factor = 1.0
        
        # End of race (more desperate moves)
        if lap_number > total_laps - 5:
            lap_factor *= 1.5
        
        # Weather factors
        weather_factor = 1.0
        if weather:
            # Rain significantly increases incidents
            rain_prob = weather.get('rain_probability', 0)
            if rain_prob > 0.7:
                weather_factor = 3.0
            elif rain_prob > 0.3:
                weather_factor = 2.0
            
            # Mixed conditions (most dangerous)
            if 0.3 < rain_prob < 0.7:
                weather_factor = 3.5
            
            # Wind
            wind_speed = weather.get('wind_speed', 0)
            if wind_speed > 30:
                weather_factor *= 1.3
        
        # Calculate total probability
        total_incident_prob = base_rate * track_multiplier * lap_factor * weather_factor
        
        # Cap at reasonable maximum
        total_incident_prob = min(total_incident_prob, 0.5)
        
        # Break down by incident type
        return {
            'total': total_incident_prob,
            'crash': total_incident_prob * 0.4,  # 40% result in crash
            'safety_car': total_incident_prob * 0.25,  # 25% need SC
            'vsc': total_incident_prob * 0.20,  # 20% need VSC
            'red_flag': total_incident_prob * 0.05,  # 5% red flag
            'minor': total_incident_prob * 0.10,  # 10% minor incidents
        }
    
    def simulate_race_incidents(self, total_laps: int,
                               weather_forecast: Optional[List[Dict]] = None,
                               track_name: str = "Unknown") -> List[Dict]:
        """
        Simulate incidents throughout entire race.
        
        Args:
            total_laps: Total race laps
            weather_forecast: Weather conditions per lap (or overall)
            track_name: Circuit name
        
        Returns:
            List of incidents with lap number and type
        """
        incidents = []
        
        for lap in range(1, total_laps + 1):
            # Get weather for this lap
            if weather_forecast and isinstance(weather_forecast, list):
                weather = weather_forecast[min(lap - 1, len(weather_forecast) - 1)]
            elif weather_forecast:
                weather = weather_forecast
            else:
                weather = None
            
            # Calculate incident probability
            probs = self.calculate_lap_incident_probability(
                lap, total_laps, weather, track_name
            )
            
            # Monte Carlo: does incident occur?
            if np.random.random() < probs['total']:
                # Determine incident type
                rand = np.random.random()
                
                if rand < 0.05:  # 5% red flag
                    incident_type = 'red_flag'
                    duration = np.random.randint(15, 45)  # 15-45 min delay
                elif rand < 0.30:  # 25% safety car
                    incident_type = 'safety_car'
                    duration = np.random.randint(3, 8)  # 3-8 laps
                elif rand < 0.50:  # 20% VSC
                    incident_type = 'vsc'
                    duration = np.random.randint(2, 5)  # 2-5 laps
                elif rand < 0.90:  # 40% crash (no SC)
                    incident_type = 'crash'
                    duration = 0
                else:  # 10% minor
                    incident_type = 'minor'
                    duration = 0
                
                incidents.append({
                    'lap': lap,
                    'type': incident_type,
                    'duration': duration,
                    'probability': probs['total']
                })
        
        return incidents
    
    def calculate_safety_car_probability(self, total_laps: int,
                                        weather: Optional[Dict] = None,
                                        track_name: str = "Unknown") -> float:
        """
        Calculate probability of at least one safety car in race.
        
        Args:
            total_laps: Total race laps
            weather: Weather conditions
            track_name: Circuit name
        
        Returns:
            Probability (0-1)
        """
        # Simulate many races
        num_simulations = 1000
        safety_car_count = 0
        
        for _ in range(num_simulations):
            incidents = self.simulate_race_incidents(total_laps, weather, track_name)
            
            # Check if any safety car or red flag
            has_sc = any(
                inc['type'] in ['safety_car', 'red_flag'] 
                for inc in incidents
            )
            
            if has_sc:
                safety_car_count += 1
        
        return safety_car_count / num_simulations
    
    def get_optimal_pit_windows(self, total_laps: int,
                               weather: Optional[Dict] = None,
                               track_name: str = "Unknown") -> List[Tuple[int, int, float]]:
        """
        Identify laps with higher incident probability (good for pit stops).
        
        Args:
            total_laps: Total race laps
            weather: Weather conditions
            track_name: Circuit name
        
        Returns:
            List of (start_lap, end_lap, incident_probability)
        """
        windows = []
        
        # First few laps (high crash risk)
        first_lap_prob = self.calculate_lap_incident_probability(
            1, total_laps, weather, track_name
        )
        windows.append((1, 3, first_lap_prob['total']))
        
        # Mid-race windows
        for lap in range(15, total_laps - 10, 10):
            prob = self.calculate_lap_incident_probability(
                lap, total_laps, weather, track_name
            )
            windows.append((lap, lap + 2, prob['total']))
        
        # End of race
        late_lap_prob = self.calculate_lap_incident_probability(
            total_laps - 3, total_laps, weather, track_name
        )
        windows.append((total_laps - 5, total_laps - 2, late_lap_prob['total']))
        
        # Sort by probability (descending)
        windows.sort(key=lambda x: x[2], reverse=True)
        
        return windows
    
    def analyze_track_risk(self, track_name: str) -> Dict[str, any]:
        """
        Get comprehensive risk analysis for a track.
        
        Args:
            track_name: Circuit name
        
        Returns:
            Dictionary with risk metrics
        """
        base_rate = self.circuit_incident_rates.get(track_name, 0.5)
        
        # Categorize risk
        if base_rate > 0.7:
            risk_category = "Very High"
        elif base_rate > 0.5:
            risk_category = "High"
        elif base_rate > 0.3:
            risk_category = "Medium"
        else:
            risk_category = "Low"
        
        # Expected incidents
        expected_incidents = base_rate
        expected_safety_cars = base_rate * 0.4
        expected_red_flags = base_rate * 0.08
        
        return {
            'track': track_name,
            'risk_category': risk_category,
            'incident_rate': base_rate,
            'expected_incidents_per_race': expected_incidents,
            'expected_safety_cars': expected_safety_cars,
            'expected_red_flags': expected_red_flags,
            'recommendations': self._get_risk_recommendations(risk_category)
        }
    
    def _get_risk_recommendations(self, risk_category: str) -> List[str]:
        """Get strategy recommendations based on risk."""
        if risk_category == "Very High":
            return [
                "Consider conservative pit strategy with early stops",
                "Be prepared for multiple safety car periods",
                "Save tire life for potential safety car restarts",
                "Avoid risky overtaking maneuvers"
            ]
        elif risk_category == "High":
            return [
                "Plan for at least one safety car period",
                "Have flexible pit strategy ready",
                "Monitor track conditions closely"
            ]
        elif risk_category == "Medium":
            return [
                "Standard strategy should work well",
                "Be ready to adapt if safety car appears",
                "Focus on tire management"
            ]
        else:
            return [
                "Clean race expected",
                "Execute planned strategy",
                "Maximize tire performance"
            ]


if __name__ == "__main__":
    # Test crash predictor
    print("Testing Crash Predictor...")
    
    predictor = CrashPredictor()
    
    # Analyze Monaco (high risk)
    monaco_risk = predictor.analyze_track_risk("Monaco")
    print(f"\n{monaco_risk['track']} Risk Analysis:")
    print(f"  Category: {monaco_risk['risk_category']}")
    print(f"  Incident Rate: {monaco_risk['incident_rate']:.0%}")
    print(f"  Expected Safety Cars: {monaco_risk['expected_safety_cars']:.2f}")
    print(f"  Recommendations: {monaco_risk['recommendations'][0]}")
    
    # Calculate safety car probability
    sc_prob = predictor.calculate_safety_car_probability(
        total_laps=78,
        track_name="Monaco"
    )
    print(f"\n  Safety Car Probability: {sc_prob:.0%}")
    
    # Simulate race
    weather = {'temperature': 22, 'rain_probability': 0.1}
    incidents = predictor.simulate_race_incidents(
        total_laps=57,
        weather_forecast=weather,
        track_name="Bahrain"
    )
    print(f"\nSimulated {len(incidents)} incidents in Bahrain GP")
