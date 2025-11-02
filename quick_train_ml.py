#!/usr/bin/env python3
"""Quick ML model training script - uses only 2025 data for speed."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.ml_strategy_predictor import MLStrategyPredictor
import warnings
warnings.filterwarnings('ignore')

print('🤖 Quick ML Model Training (2025 Data Only)')
print('='*80)
print('\nThis uses only completed 2025 races for faster training.')
print('For production, train on [2023, 2024, 2025] for better accuracy.\n')

# Initialize predictor
predictor = MLStrategyPredictor()

# Train on 2025 only (faster, ~10-15 races)
try:
    predictor.train(years=[2025], save_model=True)
    
    print('\n' + '='*80)
    print('✅ Quick training complete!')
    print('\nModel saved and ready to use.')
    
except Exception as e:
    print(f'\n❌ Training error: {e}')
    import traceback
    traceback.print_exc()
