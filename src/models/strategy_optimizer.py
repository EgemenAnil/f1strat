"""
Optimal pit stop strategy optimizer for F1 races.
Uses predictive models and simulation to find best strategy.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from itertools import product
import warnings
warnings.filterwarnings('ignore')

from ..features.track_features import TrackFeatures
from ..features.driver_ratings import DriverRatings, TeamPerformance


@dataclass
class Strategy:
    """Pit stop strategy definition."""
    name: str
    compounds: List[str]
    pit_laps: List[int]
    expected_time: float = 0.0
    finish_position: int = 0
    confidence: float = 0.0


class StrategyOptimizer:
    """Optimize pit stop strategies for upcoming races."""
    
    def __init__(self, race_predictor=None, total_laps: int = 57, track_name: str = "Unknown"):
        """
        Initialize optimizer.
        
        Args:
            race_predictor: Trained race prediction model
            total_laps: Total race laps
            track_name: Circuit name for track-specific base times
        """
        self.race_predictor = race_predictor
        self.total_laps = total_laps
        self.track_name = track_name
        
        # Get track-specific base lap time
        track_info = TrackFeatures.get_track_info(track_name)
        if track_info and 'base_lap_time' in track_info:
            self.base_lap_time = track_info['base_lap_time']
        else:
            self.base_lap_time = 90.0  # Fallback to generic time
        
        # Track-specific characteristics
        self.is_monaco = 'Monaco' in track_name
        self.is_street_circuit = track_name in ['Monaco', 'Singapore', 'Jeddah', 'Baku', 'Azerbaijan']
        
        # Safety Car probabilities by track type
        self.safety_car_probability = self._get_safety_car_probability()
        
        # Compound performance characteristics
        # Updated for 2025 season (more durable tires vs 2023)
        self.compound_params = {
            'SOFT': {
                'base_pace': 0.0,  # Fastest (reference)
                'degradation_rate': 0.04,  # 2025: 50% lower than 2023 (was 0.08)
                'optimal_stint': 25,  # 2025: +39% longer (was 18)
                'max_stint': 35  # 2025: +40% longer (was 25)
            },
            'MEDIUM': {
                'base_pace': 0.3,  # 0.3s slower than soft
                'degradation_rate': 0.025,  # 2025: 50% lower (was 0.05)
                'optimal_stint': 35,  # 2025: +25% longer (was 28)
                'max_stint': 45  # 2025: +18% longer (was 38)
            },
            'HARD': {
                'base_pace': 0.5,  # 0.5s slower than soft
                'degradation_rate': 0.015,  # 2025: 50% lower (was 0.03)
                'optimal_stint': 45,  # 2025: +29% longer (was 35)
                'max_stint': 55  # 2025: +10% longer (was 50)
            }
        }
        
        # Strategy constraints (FIA regulations)
        self.min_pit_stops = 1
        self.min_compounds = 2  # Must use at least 2 different compounds
        
    def _get_safety_car_probability(self) -> float:
        """
        Get Safety Car probability based on track characteristics.
        
        NOTE: SC simulation is DISABLED in current version.
        These probabilities are kept for future reference and analysis.
        Predicting SC is nearly impossible - better to optimize for clean race.
        """
        sc_probabilities = {
            'Monaco': 0.30,      # Historical: ~30% Monaco races have SC
            'Singapore': 0.40,   # Historical: ~40% (long, demanding)
            'Jeddah': 0.35,      # Street circuit, high speed
            'Azerbaijan': 0.30,  # Baku street circuit
            'Baku': 0.30,
            'Saudi Arabia': 0.35,
        }
        
        # Check if exact match
        for track, prob in sc_probabilities.items():
            if track in self.track_name:
                return prob
        
        # Default probabilities
        if self.is_street_circuit:
            return 0.25  # Generic street circuit
        return 0.15  # Normal circuits    def generate_strategies(self, weather_forecast: Optional[Dict] = None) -> List[Strategy]:
        self.pit_stop_time = 22.0  # Average pit stop duration
    
    def generate_strategies(self, weather_forecast: Optional[Dict] = None) -> List[Strategy]:
        """
        Generate all viable pit stop strategies.
        
        Args:
            weather_forecast: Expected weather conditions
        
        Returns:
            List of viable strategies
        """
        strategies = []
        
        # Available compounds (exclude intermediates unless rain expected)
        compounds = ['SOFT', 'MEDIUM', 'HARD']
        if weather_forecast and weather_forecast.get('rain_probability', 0) > 0.3:
            compounds.append('INTERMEDIATE')
        
        # NOTE: 0-stop is ILLEGAL in F1!
        # F1 regulations require using at least 2 different tire compounds
        # in dry races. No 0-stop strategies generated.
        
        # Monaco-specific strategy generation
        # Monaco has more strategy variance due to:
        # - Zero overtaking (track position crucial)
        # - Undercut power (fresh tires gain 2-3s in traffic)
        # - Result: 2-stop viable but not always optimal
        if self.is_monaco:
            one_stop_multiplier = 1.0  # Keep 1-stop generation normal
            two_stop_multiplier = 1.2  # Slightly more 2-stops (not 1.5x)
        else:
            one_stop_multiplier = 1.0
            two_stop_multiplier = 1.0
        
        # Generate 1-stop strategies
        one_stop_step = int(1 / one_stop_multiplier) if one_stop_multiplier < 1 else 1
        for start_compound, end_compound in product(compounds, repeat=2):
            if start_compound == end_compound:
                continue  # Must use 2 different compounds
            
            # Optimal pit window based on compound characteristics
            start_optimal = self.compound_params[start_compound]['optimal_stint']
            
            for pit_lap in range(
                max(10, start_optimal - 5),
                min(self.total_laps - 10, start_optimal + 5),
                one_stop_step
            ):
                strategies.append(Strategy(
                    name=f"1-Stop: {start_compound[:1]}{pit_lap}{end_compound[:1]}",
                    compounds=[start_compound, end_compound],
                    pit_laps=[pit_lap]
                ))
        
        # Generate 2-stop strategies
        two_stop_step = max(1, int(1 / two_stop_multiplier))
        for c1, c2, c3 in product(compounds, repeat=3):
            # Must have at least 2 different compounds
            if len(set([c1, c2, c3])) < 2:
                continue
            
            opt1 = self.compound_params[c1]['optimal_stint']
            opt2 = self.compound_params[c2]['optimal_stint']
            
            for pit1 in range(
                max(8, opt1 - 3), 
                min(opt1 + 3, self.total_laps // 3),
                two_stop_step
            ):
                for pit2 in range(
                    pit1 + max(8, opt2 - 3),
                    min(pit1 + opt2 + 3, self.total_laps - 8),
                    two_stop_step
                ):
                    strategies.append(Strategy(
                        name=f"2-Stop: {c1[:1]}{pit1}{c2[:1]}{pit2}{c3[:1]}",
                        compounds=[c1, c2, c3],
                        pit_laps=[pit1, pit2]
                    ))
        
        # NOTE: 3-stop strategies removed - extremely rare in modern F1
        # Only viable in exceptional circumstances:
        # - Multiple safety cars
        # - Extreme tire degradation (40+°C track temp)
        # - Rain interruptions
        # Modern F1 races are 95%+ won with 1-stop or 2-stop strategies
        
        return strategies
    
    def simulate_strategy(self, strategy: Strategy, 
                         weather_forecast: Optional[Dict] = None,
                         track_name: str = "Unknown",
                         driver_code: str = "AVG",
                         team_name: str = "Unknown") -> Tuple[float, Dict]:
        """
        Simulate a specific strategy.
        
        Args:
            strategy: Strategy to simulate
            weather_forecast: Weather conditions
            track_name: Circuit name
            driver_code: 3-letter driver code for skill adjustment
            team_name: Team name for car/pit performance
        
        Returns:
            Tuple of (total_race_time, detailed_results)
        """
        total_time = 0.0
        lap_times = []
        current_lap = 1
        
        # Get driver skill and team performance
        driver_delta = DriverRatings.get_driver_rating(driver_code)
        team_data = TeamPerformance.get_team_performance(team_name)
        car_delta = team_data['car_performance'] if team_data else 0.0
        
        # Safety Car simulation disabled for now - creates too much variance
        # Real races: SC happens ~20-40% of time, but predicting WHICH race is impossible
        # Better to optimize for normal conditions and handle SC as special case
        
        # Iterate through stints
        for stint_idx, compound in enumerate(strategy.compounds):
            # Determine stint length
            if stint_idx < len(strategy.pit_laps):
                stint_end = strategy.pit_laps[stint_idx]
            else:
                stint_end = self.total_laps
            
            stint_length = stint_end - current_lap + 1
            
            # Simulate each lap in stint
            for lap_in_stint in range(1, stint_length + 1):
                lap_time = self._calculate_lap_time(
                    lap_number=current_lap,
                    compound=compound,
                    tire_age=lap_in_stint - 1,
                    weather=weather_forecast,
                    driver_delta=driver_delta,
                    car_delta=car_delta
                )
                
                lap_times.append(lap_time)
                total_time += lap_time
                current_lap += 1
            
            # Add pit stop time (except after last stint)
            if stint_idx < len(strategy.pit_laps):
                # Use team-specific pit stop time with variation
                pit_time = TeamPerformance.get_pit_stop_time(team_name, add_variation=True)
                
                # Monaco: Undercut is valuable due to zero overtaking
                # Small bonus makes 2-stop competitive (as seen in real races)
                if self.is_monaco and len(strategy.pit_laps) >= 2:
                    # Monaco 2023: 45% 2-stop, 40% 1-stop (nearly equal split)
                    # This bonus reflects track position value
                    pit_time -= 1.5  # Moderate undercut bonus
                
                total_time += pit_time
        
        results = {
            'total_time': total_time,
            'avg_lap_time': np.mean(lap_times),
            'fastest_lap': np.min(lap_times),
            'slowest_lap': np.max(lap_times),
            'lap_times': lap_times
        }
        
        return total_time, results
    
    def _calculate_lap_time(self, lap_number: int, compound: str,
                           tire_age: int, weather: Optional[Dict] = None,
                           driver_delta: float = 0.0, car_delta: float = 0.0) -> float:
        """
        Calculate lap time for given conditions.
        
        Args:
            lap_number: Current lap number
            compound: Tire compound
            tire_age: Age of current tires
            weather: Weather conditions
            driver_delta: Driver skill adjustment (seconds)
            car_delta: Car performance adjustment (seconds)
        
        Returns:
            Lap time in seconds
        """
        # Base lap time (track-specific, not hardcoded!)
        base_time = self.base_lap_time
        
        # Monaco-specific adjustments
        if self.is_monaco:
            # Tire degradation matters less at Monaco (slow corners, gentle on tires)
            # But traffic/position matters MORE (no overtaking)
            tire_deg_multiplier = 0.6  # 40% less deg impact
        else:
            tire_deg_multiplier = 1.0
        
        # Driver skill effect
        driver_effect = driver_delta
        
        # Car performance effect
        car_effect = car_delta
        
        # Compound effect
        compound_delta = self.compound_params[compound]['base_pace']
        
        # Tire degradation
        deg_rate = self.compound_params[compound]['degradation_rate']
        tire_deg = tire_age * deg_rate * tire_deg_multiplier
        
        # Fuel effect (car gets lighter)
        fuel_effect = (self.total_laps - lap_number) * 0.035
        
        # Track evolution (rubber buildup)
        track_evolution = -lap_number * 0.002
        
        # Weather effects
        weather_effect = 0.0
        if weather:
            # Rain penalty
            if weather.get('rain_probability', 0) > 0.5:
                if compound != 'INTERMEDIATE':
                    weather_effect += 5.0  # Huge penalty for wrong tires
                else:
                    weather_effect += 1.0  # Inters slower than slicks in dry
            
            # Temperature effect
            temp = weather.get('temperature', 20)
            if temp > 35:  # Very hot
                weather_effect += 0.3
            elif temp < 10:  # Very cold
                weather_effect += 0.5
        
        # Random variation
        random_variation = np.random.normal(0, 0.15)
        
        lap_time = (base_time + driver_effect + car_effect + compound_delta + 
                   tire_deg + fuel_effect + track_evolution + weather_effect + 
                   random_variation)
        
        return max(lap_time, 60.0)  # Minimum 1:00.000
    
    def optimize(self, weather_forecast: Optional[Dict] = None,
                track_name: str = "Unknown", 
                num_simulations: int = 100) -> List[Strategy]:
        """
        Find optimal strategies through simulation.
        
        Args:
            weather_forecast: Expected weather
            track_name: Circuit name
            num_simulations: Number of Monte Carlo simulations per strategy
        
        Returns:
            List of strategies sorted by expected performance
        """
        print(f"\n🏎️  Optimizing strategies for {track_name} ({self.total_laps} laps)...")
        
        # Track characteristics info
        if self.is_monaco:
            print(f"   🏙️  Monaco: Higher 2-stop viability (undercut value)")
        
        # Generate all viable strategies
        strategies = self.generate_strategies(weather_forecast)
        print(f"   📊 Generated {len(strategies)} strategies")
        
        # Simulate each strategy multiple times
        results = []
        
        print(f"   🎲 Running Monte Carlo simulation ({num_simulations} iterations per strategy)...")
        for strategy in strategies:
            times = []
            for _ in range(num_simulations):
                total_time, _ = self.simulate_strategy(
                    strategy, weather_forecast, track_name
                )
                times.append(total_time)
            
            # Calculate statistics
            strategy.expected_time = np.mean(times)
            strategy.confidence = 1.0 - (np.std(times) / np.mean(times))
            
            results.append(strategy)
        
        # Sort by expected time
        results.sort(key=lambda s: s.expected_time)
        
        # Assign estimated finish positions
        for idx, strategy in enumerate(results):
            strategy.finish_position = idx + 1
        
        print(f"   ✅ Optimization complete! Best: {results[0].name}")
        return results
    
    def get_optimal_strategy(self, weather_forecast: Optional[Dict] = None,
                           track_name: str = "Unknown",
                           risk_tolerance: str = 'medium') -> Strategy:
        """
        Get single best strategy recommendation.
        
        Args:
            weather_forecast: Expected weather
            track_name: Circuit name
            risk_tolerance: 'conservative', 'medium', or 'aggressive'
        
        Returns:
            Recommended strategy
        """
        strategies = self.optimize(weather_forecast, track_name)
        
        if risk_tolerance == 'conservative':
            # Prefer fewer stops
            one_stoppers = [s for s in strategies if len(s.pit_laps) == 1]
            return one_stoppers[0] if one_stoppers else strategies[0]
        
        elif risk_tolerance == 'aggressive':
            # Prefer strategies with softer compounds
            soft_strats = [s for s in strategies[:10] if 'SOFT' in s.compounds]
            return soft_strats[0] if soft_strats else strategies[0]
        
        else:  # medium
            return strategies[0]


if __name__ == "__main__":
    # Test strategy optimizer
    print("Testing Strategy Optimizer...")
    
    optimizer = StrategyOptimizer(total_laps=57)
    
    # Test weather
    weather = {
        'temperature': 25,
        'rain_probability': 0.2,
        'humidity': 60
    }
    
    # Find optimal strategy
    best_strategy = optimizer.get_optimal_strategy(
        weather_forecast=weather,
        track_name="Bahrain",
        risk_tolerance='medium'
    )
    
    print(f"\nOptimal Strategy: {best_strategy.name}")
    print(f"Compounds: {' → '.join(best_strategy.compounds)}")
    print(f"Pit Laps: {best_strategy.pit_laps}")
    print(f"Expected Time: {best_strategy.expected_time:.1f}s")
    print(f"Confidence: {best_strategy.confidence:.2%}")
