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
        },
        'Japan': {
            'length_km': 5.807,
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
        # Normalize track name
        for key in cls.TRACK_DATA.keys():
            if key.lower() in track_name.lower() or track_name.lower() in key.lower():
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
