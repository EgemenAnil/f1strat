"""
Track-specific features for F1 race prediction.
Contains characteristics for all 22+ F1 circuits.
"""

from typing import Dict, Optional
import pandas as pd


class TrackFeatures:
    """Track-specific feature engineering."""
    
    # Complete track database
    TRACK_DATA = {
        'Bahrain': {
            'length_km': 5.412,
            'base_lap_time': 93.0,  # 1:33.0 (2024 race pace)
            'qualifying_lap_time': 90.5,  # 1:30.5 (pole position)
            'drs_gain': 0.35,  # Time gain with DRS
            'corners': 15,
            'drs_zones': 3,
            'elevation_change_m': 7,
            'avg_speed_kmh': 205,
            'overtaking_difficulty': 0.4,  # 0=easy, 1=very hard
            'tire_stress': 0.7,  # 0=low, 1=extreme
            'brake_severity': 0.8,
            'fuel_consumption': 0.7,
            'pit_loss_seconds': 22.0,
            'typical_safety_cars': 0.3,  # probability per race
            'weather_variability': 0.2,  # 0=stable, 1=very variable
        },
        'Saudi Arabia': {
            'length_km': 6.174,
            'base_lap_time': 91.5,  # 1:31.5 (fast street circuit)
            'qualifying_lap_time': 89.8,  # 1:29.8
            'drs_gain': 0.4,  # Multiple DRS zones
            'corners': 27,
            'drs_zones': 3,
            'elevation_change_m': 18,
            'avg_speed_kmh': 252,
            'overtaking_difficulty': 0.7,
            'tire_stress': 0.5,
            'brake_severity': 0.6,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 24.0,
            'typical_safety_cars': 0.6,
            'weather_variability': 0.1,
        },
        'Australia': {
            'length_km': 5.278,
            'corners': 14,
            'drs_zones': 3,
            'elevation_change_m': 15,
            'avg_speed_kmh': 235,
            'overtaking_difficulty': 0.5,
            'tire_stress': 0.6,
            'brake_severity': 0.7,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 23.0,
            'typical_safety_cars': 0.5,
            'weather_variability': 0.4,
            'base_lap_time': 81.2,  # 1:21.2 (2024 race pace)
            'qualifying_lap_time': 78.5,  # 1:18.5 (pole position)
            'drs_gain': 0.4,
        },
        'Azerbaijan': {
            'length_km': 6.003,
            'corners': 20,
            'drs_zones': 2,
            'elevation_change_m': 17,
            'avg_speed_kmh': 215,
            'overtaking_difficulty': 0.4,
            'tire_stress': 0.4,
            'brake_severity': 0.8,
            'fuel_consumption': 0.55,
            'pit_loss_seconds': 25.0,
            'typical_safety_cars': 0.7,
            'weather_variability': 0.3,
            'base_lap_time': 103.8,  # 1:43.8 (long circuit)
            'qualifying_lap_time': 101.5,  # 1:41.5
            'drs_gain': 0.5,  # Long straight
        },
        'Miami': {
            'length_km': 5.412,
            'corners': 19,
            'drs_zones': 3,
            'elevation_change_m': 5,
            'avg_speed_kmh': 223,
            'overtaking_difficulty': 0.5,
            'tire_stress': 0.6,
            'brake_severity': 0.7,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 22.0,
            'typical_safety_cars': 0.5,
            'weather_variability': 0.5,
            'base_lap_time': 90.0,  # 1:30.0
            'qualifying_lap_time': 87.5,  # 1:27.5
            'drs_gain': 0.4,
        },
        'Monaco': {
            'length_km': 3.337,
            'corners': 19,
            'drs_zones': 1,
            'elevation_change_m': 42,
            'avg_speed_kmh': 160,
            'overtaking_difficulty': 0.95,  # Extremely difficult
            'tire_stress': 0.3,
            'brake_severity': 0.9,
            'fuel_consumption': 0.45,
            'pit_loss_seconds': 26.0,
            'typical_safety_cars': 0.8,
            'weather_variability': 0.2,
            'base_lap_time': 73.5,  # 1:13.5 (slow but short)
            'qualifying_lap_time': 71.0,  # 1:11.0
            'drs_gain': 0.15,  # Minimal effect
        },
        'Spain': {
            'length_km': 4.657,
            'corners': 16,
            'drs_zones': 2,
            'elevation_change_m': 35,
            'avg_speed_kmh': 200,
            'overtaking_difficulty': 0.6,
            'tire_stress': 0.8,
            'brake_severity': 0.6,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 21.0,
            'typical_safety_cars': 0.2,
            'weather_variability': 0.2,
            'base_lap_time': 78.5,  # 1:18.5
            'qualifying_lap_time': 76.0,
            'drs_gain': 0.35,
        },
        'Canada': {
            'length_km': 4.361,
            'corners': 14,
            'drs_zones': 3,
            'elevation_change_m': 13,
            'avg_speed_kmh': 220,
            'overtaking_difficulty': 0.4,
            'tire_stress': 0.5,
            'brake_severity': 0.8,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 20.0,
            'typical_safety_cars': 0.6,
            'weather_variability': 0.5,
            'base_lap_time': 74.0,  # 1:14.0
            'qualifying_lap_time': 71.8,
            'drs_gain': 0.4,
        },
        'Austria': {
            'length_km': 4.318,
            'corners': 10,
            'drs_zones': 3,
            'elevation_change_m': 65,
            'avg_speed_kmh': 237,
            'overtaking_difficulty': 0.3,
            'tire_stress': 0.6,
            'brake_severity': 0.5,
            'fuel_consumption': 0.55,
            'pit_loss_seconds': 19.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.6,
            'base_lap_time': 67.5,  # 1:07.5 (short, fast)
            'qualifying_lap_time': 65.0,
            'drs_gain': 0.45,
        },
        'Great Britain': {
            'length_km': 5.891,
            'corners': 18,
            'drs_zones': 2,
            'elevation_change_m': 18,
            'avg_speed_kmh': 240,
            'overtaking_difficulty': 0.5,
            'tire_stress': 0.7,
            'brake_severity': 0.6,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 23.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.8,
            'base_lap_time': 88.0,  # 1:28.0 (Silverstone)
            'qualifying_lap_time': 85.5,
            'drs_gain': 0.35,
        },
        'Hungary': {
            'length_km': 4.381,
            'corners': 14,
            'drs_zones': 2,
            'elevation_change_m': 17,
            'avg_speed_kmh': 195,
            'overtaking_difficulty': 0.8,
            'tire_stress': 0.6,
            'brake_severity': 0.6,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 20.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.5,
            'base_lap_time': 79.5,  # 1:19.5 (twisty)
            'qualifying_lap_time': 77.0,
            'drs_gain': 0.25,
        },
        'Belgium': {
            'length_km': 7.004,
            'corners': 19,
            'drs_zones': 2,
            'elevation_change_m': 101,
            'avg_speed_kmh': 237,
            'overtaking_difficulty': 0.4,
            'tire_stress': 0.6,
            'brake_severity': 0.7,
            'fuel_consumption': 0.7,
            'pit_loss_seconds': 25.0,
            'typical_safety_cars': 0.5,
            'weather_variability': 0.9,
            'base_lap_time': 108.0,  # 1:48.0 (Spa - longest)
            'qualifying_lap_time': 105.0,
            'drs_gain': 0.5,  # Kemmel straight
        },
        'Netherlands': {
            'length_km': 4.259,
            'corners': 14,
            'drs_zones': 2,
            'elevation_change_m': 4,
            'avg_speed_kmh': 228,
            'overtaking_difficulty': 0.5,
            'tire_stress': 0.5,
            'brake_severity': 0.6,
            'fuel_consumption': 0.55,
            'pit_loss_seconds': 19.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.6,
            'base_lap_time': 72.5,  # 1:12.5 (Zandvoort)
            'qualifying_lap_time': 70.0,
            'drs_gain': 0.3,
        },
        'Italy': {
            'length_km': 5.793,
            'corners': 11,
            'drs_zones': 2,
            'elevation_change_m': 23,
            'avg_speed_kmh': 264,
            'overtaking_difficulty': 0.3,
            'tire_stress': 0.5,
            'brake_severity': 0.8,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 21.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.3,
            'base_lap_time': 82.0,  # 1:22.0 (Monza - fastest)
            'qualifying_lap_time': 79.5,
            'drs_gain': 0.5,
        },
        'Singapore': {
            'length_km': 4.940,
            'corners': 19,
            'drs_zones': 3,
            'elevation_change_m': 15,
            'avg_speed_kmh': 172,
            'overtaking_difficulty': 0.7,
            'tire_stress': 0.4,
            'brake_severity': 0.9,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 24.0,
            'typical_safety_cars': 0.7,
            'weather_variability': 0.5,
            'base_lap_time': 102.0,  # 1:42.0 (bumpy street circuit)
            'qualifying_lap_time': 99.0,
            'drs_gain': 0.3,
        },
        'Japan': {
            'length_km': 5.807,
            'base_lap_time': 91.0,  # 1:31.0 (Suzuka - flowing corners)
            'qualifying_lap_time': 88.5,  # 1:28.5
            'drs_gain': 0.35,
            'corners': 18,
            'drs_zones': 2,
            'elevation_change_m': 45,
            'avg_speed_kmh': 218,
            'overtaking_difficulty': 0.6,
            'tire_stress': 0.7,
            'brake_severity': 0.6,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 23.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.6,
        },
        'Qatar': {
            'length_km': 5.380,
            'base_lap_time': 84.5,  # 1:24.5 (Losail - fast but technical)
            'qualifying_lap_time': 82.0,  # 1:22.0
            'drs_gain': 0.35,
            'corners': 16,
            'drs_zones': 2,
            'elevation_change_m': 11,
            'avg_speed_kmh': 239,
            'overtaking_difficulty': 0.5,
            'tire_stress': 0.6,
            'brake_severity': 0.7,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 22.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.1,
        },
        'United States': {
            'length_km': 5.513,
            'base_lap_time': 96.5,  # 1:36.5 (COTA - technical with long straight)
            'qualifying_lap_time': 94.0,  # 1:34.0
            'drs_gain': 0.45,  # Long back straight
            'corners': 20,
            'drs_zones': 2,
            'elevation_change_m': 41,
            'avg_speed_kmh': 209,
            'overtaking_difficulty': 0.4,
            'tire_stress': 0.7,
            'brake_severity': 0.7,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 22.0,
            'typical_safety_cars': 0.4,
            'weather_variability': 0.4,
        },
        'Mexico': {
            'length_km': 4.304,
            'base_lap_time': 78.5,  # 1:18.5 (high altitude = less drag = faster)
            'qualifying_lap_time': 76.0,  # 1:16.0
            'drs_gain': 0.3,
            'corners': 17,
            'drs_zones': 3,
            'elevation_change_m': 12,
            'avg_speed_kmh': 202,
            'overtaking_difficulty': 0.4,
            'tire_stress': 0.5,
            'brake_severity': 0.7,
            'fuel_consumption': 0.55,
            'pit_loss_seconds': 20.0,
            'typical_safety_cars': 0.4,
            'weather_variability': 0.3,
        },
        'Brazil': {
            'length_km': 4.309,
            'base_lap_time': 71.5,  # 1:11.5 (Interlagos - short, technical)
            'qualifying_lap_time': 69.0,  # 1:09.0
            'drs_gain': 0.4,
            'corners': 15,
            'drs_zones': 2,
            'elevation_change_m': 41,
            'avg_speed_kmh': 215,
            'overtaking_difficulty': 0.5,
            'tire_stress': 0.6,
            'brake_severity': 0.7,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 20.0,
            'typical_safety_cars': 0.5,
            'weather_variability': 0.8,
        },
        'Las Vegas': {
            'length_km': 6.201,
            'base_lap_time': 96.0,  # 1:36.0 (new street circuit, long straights)
            'qualifying_lap_time': 93.5,  # 1:33.5
            'drs_gain': 0.5,  # Very long straights (350+ km/h)
            'corners': 17,
            'drs_zones': 2,
            'elevation_change_m': 12,
            'avg_speed_kmh': 240,
            'overtaking_difficulty': 0.4,
            'tire_stress': 0.5,
            'brake_severity': 0.7,
            'fuel_consumption': 0.65,
            'pit_loss_seconds': 24.0,
            'typical_safety_cars': 0.4,
            'weather_variability': 0.2,
        },
        'Abu Dhabi': {
            'length_km': 5.281,
            'base_lap_time': 87.0,  # 1:27.0 (Yas Marina - redesigned, faster)
            'qualifying_lap_time': 84.5,  # 1:24.5
            'drs_gain': 0.35,
            'corners': 16,
            'drs_zones': 2,
            'elevation_change_m': 11,
            'avg_speed_kmh': 195,
            'overtaking_difficulty': 0.6,
            'tire_stress': 0.6,
            'brake_severity': 0.7,
            'fuel_consumption': 0.6,
            'pit_loss_seconds': 22.0,
            'typical_safety_cars': 0.3,
            'weather_variability': 0.1,
        },
    }
    
    @classmethod
    def get_track_info(cls, track_name: str) -> Optional[Dict]:
        """
        Get track characteristics.
        
        Args:
            track_name: Name of the track
        
        Returns:
            Dictionary with track characteristics or None
        """
        # Track name aliases for better matching
        track_aliases = {
            'sao paulo': 'Brazil',
            'são paulo': 'Brazil',
            'interlagos': 'Brazil',
            'jeddah': 'Saudi Arabia',
            'silverstone': 'Great Britain',
            'spa': 'Belgium',
            'monza': 'Italy',
            'suzuka': 'Japan',
            'cota': 'United States',
            'austin': 'United States',
            'mexico city': 'Mexico',
            'yas marina': 'Abu Dhabi',
            'losail': 'Qatar',
            'zandvoort': 'Netherlands',
        }
        
        # Normalize track name
        track_lower = track_name.lower().strip()
        
        # Check aliases first
        normalized_name = track_aliases.get(track_lower, track_name)
        
        # Try exact match or partial match (case-insensitive)
        for key in cls.TRACK_DATA.keys():
            if key.lower() == normalized_name.lower():
                return cls.TRACK_DATA[key]
            if key.lower() in normalized_name.lower() or normalized_name.lower() in key.lower():
                return cls.TRACK_DATA[key]
        
        return None
    
    @classmethod
    def add_track_features(cls, df: pd.DataFrame, track_name: str) -> pd.DataFrame:
        """
        Add track-specific features to DataFrame.
        
        Args:
            df: Input DataFrame
            track_name: Name of the track
        
        Returns:
            DataFrame with track features
        """
        df = df.copy()
        track_info = cls.get_track_info(track_name)
        
        if track_info is None:
            print(f"Warning: Track '{track_name}' not found in database. Using defaults.")
            track_info = {
                'length_km': 5.0,
                'corners': 15,
                'drs_zones': 2,
                'elevation_change_m': 20,
                'avg_speed_kmh': 200,
                'overtaking_difficulty': 0.5,
                'tire_stress': 0.6,
                'brake_severity': 0.6,
                'fuel_consumption': 0.6,
                'pit_loss_seconds': 22.0,
                'typical_safety_cars': 0.4,
                'weather_variability': 0.4,
            }
        
        # Add all track characteristics as features
        for key, value in track_info.items():
            df[f'Track_{key}'] = value
        
        # Derived features
        df['Track_corners_per_km'] = track_info['corners'] / track_info['length_km']
        df['Track_speed_category'] = pd.cut([track_info['avg_speed_kmh']], 
                                            bins=[0, 180, 220, 300],
                                            labels=['low', 'medium', 'high'])[0]
        
        return df
    
    @classmethod
    def get_optimal_compounds(cls, track_name: str) -> Dict[str, float]:
        """
        Get optimal tire compound distribution for track.
        
        Args:
            track_name: Name of the track
        
        Returns:
            Dictionary with compound preferences (0-1 scale)
        """
        track_info = cls.get_track_info(track_name)
        
        if track_info is None:
            return {'SOFT': 0.33, 'MEDIUM': 0.34, 'HARD': 0.33}
        
        tire_stress = track_info['tire_stress']
        
        if tire_stress > 0.7:
            # High degradation tracks prefer harder compounds
            return {'SOFT': 0.2, 'MEDIUM': 0.3, 'HARD': 0.5}
        elif tire_stress < 0.5:
            # Low degradation tracks can use softer compounds
            return {'SOFT': 0.5, 'MEDIUM': 0.3, 'HARD': 0.2}
        else:
            # Medium degradation - balanced
            return {'SOFT': 0.3, 'MEDIUM': 0.4, 'HARD': 0.3}


if __name__ == "__main__":
    # Test track features
    print("Testing track features...")
    
    # Test track info retrieval
    bahrain_info = TrackFeatures.get_track_info('Bahrain')
    print(f"\nBahrain GP Info:")
    for key, value in bahrain_info.items():
        print(f"  {key}: {value}")
    
    # Test optimal compounds
    monaco_compounds = TrackFeatures.get_optimal_compounds('Monaco')
    print(f"\nMonaco optimal compounds: {monaco_compounds}")
    
    # Test adding features to DataFrame
    sample_df = pd.DataFrame({'LapNumber': [1, 2, 3]})
    enhanced_df = TrackFeatures.add_track_features(sample_df, 'Spa')
    print(f"\nAdded {len(enhanced_df.columns) - 1} track features")
    print(enhanced_df.columns.tolist())
