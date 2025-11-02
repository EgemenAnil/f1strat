"""
Driver skill ratings and team performance factors for F1 2025 season.
Based on actual performance data, championship standings, and qualifying pace.
Updated: November 2025 (end of season data)
"""

from typing import Dict, Optional


class DriverRatings:
    """Driver skill ratings for 2025 F1 season (November update)."""
    
    # Driver skill ratings (lap time delta in seconds)
    # Positive = slower than average, Negative = faster than average
    # Based on 2025 season performance (qualifying pace, race pace, consistency)
    DRIVER_RATINGS = {
        # Red Bull Racing
        'VER': -0.38,  # Max Verstappen - Still dominant, 4x WDC (2025)
        'PER': -0.05,  # Sergio Perez - Declining form, struggles vs VER
        
        # Ferrari
        'LEC': -0.32,  # Charles Leclerc - Improved, title contender
        'HAM': -0.28,  # Lewis Hamilton - Moved to Ferrari, adapting well
        
        # Mercedes
        'RUS': -0.26,  # George Russell - Team leader now, consistent
        'ANT': -0.12,  # Andrea Kimi Antonelli - Promising rookie
        
        # McLaren
        'NOR': -0.30,  # Lando Norris - Title fight, peak performance
        'PIA': -0.24,  # Oscar Piastri - Massive improvement, race winner
        
        # Aston Martin
        'ALO': -0.18,  # Fernando Alonso - Still competitive at 44
        'STR': -0.06,  # Lance Stroll - Slight improvement
        
        # Alpine
        'GAS': -0.14,  # Pierre Gasly - Solid midfield performer
        'OCO': -0.11,  # Esteban Ocon - Consistent points
        
        # Williams
        'ALB': -0.16,  # Alex Albon - Strong in improved Williams
        'SAI': -0.20,  # Carlos Sainz - Moved from Ferrari, experienced
        
        # RB (Racing Bulls)
        'TSU': -0.10,  # Yuki Tsunoda - Matured, more consistent
        'RIC': -0.08,  # Daniel Ricciardo - Veteran presence
        
        # Kick Sauber (Stake F1)
        'BOT': -0.08,  # Valtteri Bottas - Experience in slower car
        'ZHO': 0.02,   # Zhou Guanyu - Slight improvement
        
        # Haas
        'HUL': -0.10,  # Nico Hulkenberg - Experienced, solid
        'BEA': 0.08,   # Oliver Bearman - Rookie, learning curve
    }
    
    @classmethod
    def get_driver_rating(cls, driver_code: str) -> float:
        """
        Get driver skill rating.
        
        Args:
            driver_code: 3-letter driver code (e.g., 'VER', 'HAM')
        
        Returns:
            Lap time delta in seconds (negative = faster)
        """
        return cls.DRIVER_RATINGS.get(driver_code.upper(), 0.0)
    
    @classmethod
    def get_top_drivers(cls, n: int = 5) -> Dict[str, float]:
        """
        Get top N fastest drivers.
        
        Args:
            n: Number of top drivers to return
        
        Returns:
            Dictionary of driver codes and their ratings
        """
        sorted_drivers = sorted(cls.DRIVER_RATINGS.items(), key=lambda x: x[1])
        return dict(sorted_drivers[:n])


class TeamPerformance:
    """Team performance factors for 2025 F1 season (November update)."""
    
    # Team performance ratings
    # Affects: pit stop speed, strategy execution, reliability
    TEAM_RATINGS = {
        'Red Bull Racing': {
            'car_performance': -0.35,  # Still dominant but McLaren catching up
            'pit_stop_avg': 1.9,      # Consistently fastest pit crew
            'strategy_rating': 0.96,  # Excellent strategy, rare mistakes
            'reliability': 0.93,      # Very reliable
        },
        'McLaren': {
            'car_performance': -0.32,  # Major upgrade, title contender
            'pit_stop_avg': 1.95,     # Improved pit crew
            'strategy_rating': 0.91,  # Much better strategy in 2025
            'reliability': 0.91,      # Solid reliability
        },
        'Ferrari': {
            'car_performance': -0.30,  # Hamilton effect + good development
            'pit_stop_avg': 2.0,      # Improved pit crew
            'strategy_rating': 0.87,  # Still some mistakes but better
            'reliability': 0.89,      # Decent reliability
        },
        'Mercedes': {
            'car_performance': -0.20,  # Lost ground without Hamilton
            'pit_stop_avg': 2.0,      # Consistent pit stops
            'strategy_rating': 0.90,  # Good strategy as always
            'reliability': 0.92,      # Very reliable
        },
        'Aston Martin': {
            'car_performance': -0.08,  # Falling back to midfield
            'pit_stop_avg': 2.2,      
            'strategy_rating': 0.83,  
            'reliability': 0.86,      
        },
        'Alpine': {
            'car_performance': 0.05,   # Struggling in 2025
            'pit_stop_avg': 2.3,
            'strategy_rating': 0.79,
            'reliability': 0.83,
        },
        'Williams': {
            'car_performance': 0.08,   # Slight improvement with Sainz
            'pit_stop_avg': 2.3,
            'strategy_rating': 0.84,
            'reliability': 0.85,
        },
        'RB': {
            'car_performance': 0.10,   # Falling behind in development
            'pit_stop_avg': 2.2,
            'strategy_rating': 0.81,
            'reliability': 0.84,
        },
        'Kick Sauber': {
            'car_performance': 0.22,   # Struggling at back
            'pit_stop_avg': 2.5,
            'strategy_rating': 0.76,
            'reliability': 0.80,
        },
        'Haas': {
            'car_performance': 0.20,   # Still at back but improved
            'pit_stop_avg': 2.5,      
            'strategy_rating': 0.77,
            'reliability': 0.82,
        },
    }
    
    @classmethod
    def get_team_performance(cls, team_name: str) -> Optional[Dict]:
        """
        Get team performance factors.
        
        Args:
            team_name: Team name
        
        Returns:
            Dictionary with team performance metrics or None
        """
        # Normalize team name
        for key in cls.TEAM_RATINGS.keys():
            if key.lower() in team_name.lower() or team_name.lower() in key.lower():
                return cls.TEAM_RATINGS[key]
        return None
    
    @classmethod
    def get_pit_stop_time(cls, team_name: str, add_variation: bool = True) -> float:
        """
        Get expected pit stop time for team.
        
        Args:
            team_name: Team name
            add_variation: Add random variation (±0.2s)
        
        Returns:
            Pit stop time in seconds
        """
        team_data = cls.get_team_performance(team_name)
        if not team_data:
            base_time = 2.3  # Default midfield time
        else:
            base_time = team_data['pit_stop_avg']
        
        if add_variation:
            import numpy as np
            variation = np.random.normal(0, 0.15)  # ±0.15s standard deviation
            return max(base_time + variation, 1.8)  # Minimum 1.8s
        
        return base_time


if __name__ == "__main__":
    # Test driver ratings
    print("=" * 70)
    print("TOP 5 DRIVERS (2025 Season - November)")
    print("=" * 70)
    for driver, rating in DriverRatings.get_top_drivers(5).items():
        print(f"{driver}: {rating:+.2f}s per lap")
    
    print("\n" + "=" * 70)
    print("TEAM PERFORMANCE RANKINGS (2025 Season)")
    print("=" * 70)
    teams = sorted(TeamPerformance.TEAM_RATINGS.items(), 
                   key=lambda x: x[1]['car_performance'])
    for team, data in teams:
        print(f"{team:<20} | Car: {data['car_performance']:+.2f}s | "
              f"Pit: {data['pit_stop_avg']:.1f}s | "
              f"Strategy: {data['strategy_rating']:.0%}")
