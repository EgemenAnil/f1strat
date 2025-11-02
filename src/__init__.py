"""F1 Strategy Analysis Package"""

__version__ = '2.0.0'
__author__ = 'F1 Strategy Team'

from .data import F1DataFetcher
from .features import F1FeatureEngineer, TrackFeatures
from .models import StrategyOptimizer, CrashPredictor

__all__ = [
    'F1DataFetcher',
    'F1FeatureEngineer', 
    'TrackFeatures',
    'StrategyOptimizer',
    'CrashPredictor',
]
