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
    
    def __init__(self, race_predictor=None, total_laps: int = 57):
        """
        Initialize optimizer.
        
        Args:
            race_predictor: Trained race prediction model
            total_laps: Total race laps
        """
        self.race_predictor = race_predictor
        self.total_laps = total_laps
        
        # Compound performance characteristics
        self.compound_params = {
            'SOFT': {
                'base_pace': 0.0,  # Fastest (reference)
                'degradation_rate': 0.08,
                'optimal_stint': 18,
                'max_stint': 25
            },
            'MEDIUM': {
                'base_pace': 0.3,  # 0.3s slower than soft
                'degradation_rate': 0.05,
                'optimal_stint': 28,
                'max_stint': 40
            },
            'HARD': {
                'base_pace': 0.6,  # 0.6s slower than soft
                'degradation_rate': 0.03,
                'optimal_stint': 40,
                'max_stint': 57
            },
            'INTERMEDIATE': {
                'base_pace': 2.0,  # Much slower in dry
                'degradation_rate': 0.06,
                'optimal_stint': 25,
                'max_stint': 35
            }
        }
        
        # Strategy constraints (FIA regulations)
        self.min_pit_stops = 1
        self.min_compounds = 2  # Must use at least 2 different compounds
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
        
        # Generate 1-stop strategies
        for start_compound, end_compound in product(compounds, repeat=2):
            if start_compound == end_compound:
                continue  # Must use 2 different compounds
            
            # Optimal pit window based on compound characteristics
            start_optimal = self.compound_params[start_compound]['optimal_stint']
            
            for pit_lap in range(
                max(10, start_optimal - 5),
                min(self.total_laps - 10, start_optimal + 5)
            ):
                strategies.append(Strategy(
                    name=f"1-Stop: {start_compound[:1]}{pit_lap}{end_compound[:1]}",
                    compounds=[start_compound, end_compound],
                    pit_laps=[pit_lap]
                ))
        
        # Generate 2-stop strategies
        for c1, c2, c3 in product(compounds, repeat=3):
            # Must have at least 2 different compounds
            if len(set([c1, c2, c3])) < 2:
                continue
            
            opt1 = self.compound_params[c1]['optimal_stint']
            opt2 = self.compound_params[c2]['optimal_stint']
            
            for pit1 in range(max(8, opt1 - 3), min(opt1 + 3, self.total_laps // 3)):
                for pit2 in range(
                    pit1 + max(8, opt2 - 3),
                    min(pit1 + opt2 + 3, self.total_laps - 8)
                ):
                    strategies.append(Strategy(
                        name=f"2-Stop: {c1[:1]}{pit1}{c2[:1]}{pit2}{c3[:1]}",
                        compounds=[c1, c2, c3],
                        pit_laps=[pit1, pit2]
                    ))
        
        # Generate 3-stop strategies (aggressive)
        for compounds_combo in product(['SOFT', 'MEDIUM'], repeat=4):
            if len(set(compounds_combo)) < 2:
                continue
            
            interval = self.total_laps // 4
            pit_laps = [interval, interval * 2, interval * 3]
            
            strategies.append(Strategy(
                name=f"3-Stop: {'-'.join([c[:1] for c in compounds_combo])}",
                compounds=list(compounds_combo),
                pit_laps=pit_laps
            ))
        
        return strategies
    
    def simulate_strategy(self, strategy: Strategy, 
                         weather_forecast: Optional[Dict] = None,
                         track_name: str = "Unknown") -> Tuple[float, Dict]:
        """
        Simulate a specific strategy.
        
        Args:
            strategy: Strategy to simulate
            weather_forecast: Weather conditions
            track_name: Circuit name
        
        Returns:
            Tuple of (total_race_time, detailed_results)
        """
        total_time = 0.0
        lap_times = []
        current_lap = 1
        
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
                    weather=weather_forecast
                )
                
                lap_times.append(lap_time)
                total_time += lap_time
                current_lap += 1
            
            # Add pit stop time (except after last stint)
            if stint_idx < len(strategy.pit_laps):
                pit_variation = np.random.normal(0, 1.5)  # ±1.5s variation
                total_time += self.pit_stop_time + pit_variation
        
        results = {
            'total_time': total_time,
            'avg_lap_time': np.mean(lap_times),
            'fastest_lap': np.min(lap_times),
            'slowest_lap': np.max(lap_times),
            'lap_times': lap_times
        }
        
        return total_time, results
    
    def _calculate_lap_time(self, lap_number: int, compound: str,
                           tire_age: int, weather: Optional[Dict] = None) -> float:
        """
        Calculate lap time for given conditions.
        
        Args:
            lap_number: Current lap number
            compound: Tire compound
            tire_age: Age of current tires
            weather: Weather conditions
        
        Returns:
            Lap time in seconds
        """
        # Base lap time (typical for mid-field car)
        base_time = 90.0  # 1:30.000
        
        # Compound effect
        compound_delta = self.compound_params[compound]['base_pace']
        
        # Tire degradation
        deg_rate = self.compound_params[compound]['degradation_rate']
        tire_deg = tire_age * deg_rate
        
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
        
        lap_time = (base_time + compound_delta + tire_deg + fuel_effect + 
                   track_evolution + weather_effect + random_variation)
        
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
        print(f"Optimizing strategies for {track_name} ({self.total_laps} laps)...")
        
        # Generate all viable strategies
        strategies = self.generate_strategies(weather_forecast)
        print(f"Generated {len(strategies)} viable strategies")
        
        # Simulate each strategy multiple times
        results = []
        
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
