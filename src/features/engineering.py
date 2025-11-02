"""
Advanced Feature Engineering for F1 Race Prediction
Creates comprehensive features including weather impact, tire degradation, 
fuel effects, and traffic modeling.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder


class F1FeatureEngineer:
    """Advanced feature engineering for F1 race prediction."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
    
    def create_basic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create basic racing features.
        
        Args:
            df: DataFrame with lap data
        
        Returns:
            DataFrame with basic features
        """
        df = df.copy()
        
        # Lap-based features
        if 'LapNumber' in df.columns:
            df['LapProgress'] = df['LapNumber'] / df['LapNumber'].max()
            df['LapsRemaining'] = df['LapNumber'].max() - df['LapNumber']
        
        # Stint features
        if 'Stint' in df.columns:
            df['StintNumber'] = df['Stint']
        
        # Tire features
        if 'TyreLife' in df.columns:
            df['TyreAge'] = df['TyreLife']
            df['TyreAgeSq'] = df['TyreLife'] ** 2  # Non-linear degradation
            df['TyreAgeLog'] = np.log1p(df['TyreLife'])
        
        # Compound encoding
        if 'Compound' in df.columns:
            # One-hot encoding
            compound_dummies = pd.get_dummies(df['Compound'], prefix='Compound')
            df = pd.concat([df, compound_dummies], axis=1)
        
        return df
    
    def create_weather_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create weather-related features.
        
        Args:
            df: DataFrame with weather data
        
        Returns:
            DataFrame with weather features
        """
        df = df.copy()
        
        # Temperature features
        if 'AirTemp' in df.columns:
            df['AirTempNorm'] = (df['AirTemp'] - df['AirTemp'].mean()) / df['AirTemp'].std()
            df['AirTempHigh'] = (df['AirTemp'] > 30).astype(int)  # Hot conditions
            df['AirTempLow'] = (df['AirTemp'] < 15).astype(int)   # Cold conditions
        
        if 'TrackTemp' in df.columns:
            df['TrackTempNorm'] = (df['TrackTemp'] - df['TrackTemp'].mean()) / df['TrackTemp'].std()
            df['TrackTempHigh'] = (df['TrackTemp'] > 40).astype(int)
            
            # Track vs Air temp difference
            if 'AirTemp' in df.columns:
                df['TempDifference'] = df['TrackTemp'] - df['AirTemp']
        
        # Humidity
        if 'Humidity' in df.columns:
            df['HumidityNorm'] = df['Humidity'] / 100.0
            df['HighHumidity'] = (df['Humidity'] > 70).astype(int)
        
        # Wind
        if 'WindSpeed' in df.columns:
            df['WindSpeedNorm'] = df['WindSpeed'] / 50.0  # Normalize to max ~50 km/h
            df['HighWind'] = (df['WindSpeed'] > 30).astype(int)
        
        # Rain
        if 'Rainfall' in df.columns:
            df['IsRaining'] = (df['Rainfall'] > 0).astype(int)
            df['RainIntensity'] = pd.cut(df['Rainfall'], 
                                         bins=[-0.1, 0, 1, 5, 100],
                                         labels=[0, 1, 2, 3]).astype(int)
        
        return df
    
    def create_fuel_features(self, df: pd.DataFrame, 
                            total_laps: Optional[int] = None) -> pd.DataFrame:
        """
        Create fuel load features.
        
        Args:
            df: DataFrame with lap data
            total_laps: Total number of laps in race
        
        Returns:
            DataFrame with fuel features
        """
        df = df.copy()
        
        if total_laps is None and 'LapNumber' in df.columns:
            total_laps = df['LapNumber'].max()
        
        if 'LapNumber' in df.columns and total_laps:
            # Fuel load proxy (decreases linearly with laps)
            df['FuelLoadProxy'] = (total_laps - df['LapNumber']) / total_laps
            df['FuelLoadProxySq'] = df['FuelLoadProxy'] ** 2
            
            # Fuel weight impact (kg -> seconds)
            # Approximate: 1kg fuel = ~0.03s per lap
            df['FuelWeightImpact'] = df['FuelLoadProxy'] * 0.035
        
        return df
    
    def create_tire_degradation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create advanced tire degradation features.
        
        Args:
            df: DataFrame with tire data
        
        Returns:
            DataFrame with degradation features
        """
        df = df.copy()
        
        if 'TyreLife' in df.columns and 'Compound' in df.columns:
            # Compound-specific degradation rates
            deg_rates = {
                'SOFT': 1.3,
                'MEDIUM': 1.0,
                'HARD': 0.7,
                'INTERMEDIATE': 1.1,
                'WET': 1.2
            }
            
            df['DegradationRate'] = df['Compound'].map(deg_rates).fillna(1.0)
            
            # Degradation impact
            df['TireDegradation'] = df['TyreLife'] * df['DegradationRate'] * 0.005
            
            # Critical tire age (compound-dependent)
            critical_ages = {
                'SOFT': 20,
                'MEDIUM': 30,
                'HARD': 40,
                'INTERMEDIATE': 25,
                'WET': 20
            }
            
            df['CriticalAge'] = df['Compound'].map(critical_ages).fillna(30)
            df['BeyondCritical'] = (df['TyreLife'] > df['CriticalAge']).astype(int)
            df['TireLifeRatio'] = df['TyreLife'] / df['CriticalAge']
        
        return df
    
    def create_track_evolution_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create track evolution features (rubber buildup).
        
        Args:
            df: DataFrame with session data
        
        Returns:
            DataFrame with track evolution features
        """
        df = df.copy()
        
        if 'LapNumber' in df.columns:
            total_laps = df['LapNumber'].max()
            
            # Track evolution (gets faster as race progresses)
            df['TrackEvolution'] = df['LapNumber'] * 0.002  # ~2ms per lap
            
            # Track evolution percentage
            df['TrackEvolutionPct'] = df['LapNumber'] / total_laps
        
        return df
    
    def create_traffic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create traffic-related features.
        
        Args:
            df: DataFrame with position data
        
        Returns:
            DataFrame with traffic features
        """
        df = df.copy()
        
        # Position-based traffic probability
        if 'Position' in df.columns:
            # Mid-field has more traffic
            df['TrafficProbability'] = 0.15  # Base probability
            
            # Increase for mid-field (positions 5-15)
            midfield_mask = (df['Position'] >= 5) & (df['Position'] <= 15)
            df.loc[midfield_mask, 'TrafficProbability'] = 0.25
            
            # Lower for leaders
            leader_mask = df['Position'] <= 3
            df.loc[leader_mask, 'TrafficProbability'] = 0.05
        
        # Track status
        if 'TrackStatus' in df.columns:
            df['YellowFlag'] = (df['TrackStatus'] == 2).astype(int)
            df['SafetyCar'] = (df['TrackStatus'] == 4).astype(int)
            df['VirtualSafetyCar'] = (df['TrackStatus'] == 6).astype(int)
            df['RedFlag'] = (df['TrackStatus'] == 5).astype(int)
        
        return df
    
    def create_crash_risk_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create crash/incident risk features.
        
        Args:
            df: DataFrame with race data
        
        Returns:
            DataFrame with crash risk features
        """
        df = df.copy()
        
        # Base crash probability
        df['CrashRiskBase'] = 0.01  # 1% per lap base
        
        # First lap risk
        if 'LapNumber' in df.columns:
            df['FirstLapRisk'] = (df['LapNumber'] == 1).astype(float) * 0.05
        
        # Weather-related risk
        if 'Rainfall' in df.columns:
            df['WeatherRisk'] = (df['Rainfall'] > 0).astype(float) * 0.03
        
        # Tire age risk
        if 'TyreLife' in df.columns and 'Compound' in df.columns:
            # Old tires = higher risk
            df['TireRisk'] = np.where(df['TyreLife'] > 30, 0.02, 0.0)
        
        # Total crash risk
        risk_columns = [col for col in df.columns if 'Risk' in col]
        if risk_columns:
            df['TotalCrashRisk'] = df[risk_columns].sum(axis=1)
        
        return df
    
    def create_all_features(self, df: pd.DataFrame, 
                           total_laps: Optional[int] = None) -> pd.DataFrame:
        """
        Create all features.
        
        Args:
            df: Input DataFrame
            total_laps: Total race laps
        
        Returns:
            DataFrame with all features
        """
        df = self.create_basic_features(df)
        df = self.create_weather_features(df)
        df = self.create_fuel_features(df, total_laps)
        df = self.create_tire_degradation_features(df)
        df = self.create_track_evolution_features(df)
        df = self.create_traffic_features(df)
        df = self.create_crash_risk_features(df)
        
        return df
    
    def get_feature_importance_groups(self) -> Dict[str, List[str]]:
        """Get feature groups for analysis."""
        return {
            'basic': ['LapNumber', 'LapProgress', 'LapsRemaining', 'Stint', 'TyreAge'],
            'weather': ['AirTemp', 'TrackTemp', 'Humidity', 'WindSpeed', 'Rainfall'],
            'tire': ['TyreDegradation', 'BeyondCritical', 'TireLifeRatio'],
            'fuel': ['FuelLoadProxy', 'FuelWeightImpact'],
            'track': ['TrackEvolution', 'TrackEvolutionPct'],
            'traffic': ['TrafficProbability', 'SafetyCar', 'YellowFlag'],
            'risk': ['TotalCrashRisk', 'FirstLapRisk', 'WeatherRisk']
        }


if __name__ == "__main__":
    # Test feature engineering
    engineer = F1FeatureEngineer()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'LapNumber': range(1, 58),
        'Stint': [1]*20 + [2]*37,
        'TyreLife': list(range(1, 21)) + list(range(1, 38)),
        'Compound': ['SOFT']*20 + ['MEDIUM']*37,
        'AirTemp': [25] * 57,
        'TrackTemp': [35] * 57,
        'Rainfall': [0] * 57,
    })
    
    features = engineer.create_all_features(sample_data, total_laps=57)
    print(f"Created {len(features.columns)} features")
    print(features.columns.tolist())
