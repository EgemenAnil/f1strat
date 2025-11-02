#!/usr/bin/env python3
"""
F1 Race Strategy Simulation - Complete Automated Pipeline
Run this script to execute the entire analysis with one command.

Usage:
    python run_simulation.py
    
or from notebook:
    %run run_simulation.py
"""

import sys
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🏎️  F1 RACE STRATEGY SIMULATION - AUTOMATED PIPELINE")
print("="*80)
print("\n📋 This script will:")
print("   1. Load and prepare race data")
print("   2. Engineer features")
print("   3. Train ML model")
print("   4. Optimize simulation parameters (2-3 min)")
print("   5. Run all race strategy simulations")
print("   6. Generate visualizations and validation")
print("\n⏱️  Total estimated time: 3-5 minutes\n")
print("="*80)

# =============================================================================
# PHASE 1: DATA LOADING
# =============================================================================
print("\n\n" + "="*80)
print("📊 PHASE 1: LOADING DATA")
print("="*80)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.optimize import differential_evolution

# Interactive file selection
import os
from pathlib import Path

workspace_dir = Path('/Users/egemen/Desktop/f1strat')
csv_files = list(workspace_dir.glob('*_laps_clean.csv'))

if not csv_files:
    print("❌ No CSV files found in workspace!")
    sys.exit(1)

print(f"\n📁 Found {len(csv_files)} race data file(s):")
for i, file in enumerate(csv_files, 1):
    print(f"   {i}. {file.name}")

# Auto-select first file or let user choose
selected_file = csv_files[0]
print(f"\n✅ Using: {selected_file.name}")

df = pd.read_csv(selected_file)
print(f"   • Loaded {len(df):,} laps")
print(f"   • Columns: {', '.join(df.columns.tolist())}")

# =============================================================================
# PHASE 2: FEATURE ENGINEERING
# =============================================================================
print("\n\n" + "="*80)
print("🔧 PHASE 2: FEATURE ENGINEERING")
print("="*80)

# Basic features
basic_features = ['LapNumber', 'Stint', 'TyreLife', 'Compound']
df_model = df[basic_features + ['LapTime']].copy()
df_model = df_model.dropna()

# One-hot encoding for compounds
df_encoded = pd.get_dummies(df_model, columns=['Compound'], prefix='Compound')

# Separate features and target
X = df_encoded.drop('LapTime', axis=1)
y = df_encoded['LapTime']

print(f"✅ Features prepared: {X.shape[1]} features, {len(X):,} samples")
print(f"   Features: {', '.join(X.columns.tolist())}")

# =============================================================================
# PHASE 3: MODEL TRAINING
# =============================================================================
print("\n\n" + "="*80)
print("🤖 PHASE 3: TRAINING ML MODEL")
print("="*80)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"✅ Model trained successfully!")
print(f"   • R² Score: {r2:.4f}")
print(f"   • MAE: {mae:.3f}s")
print(f"   • RMSE: {rmse:.3f}s")

# =============================================================================
# PHASE 4: SIMULATION SETUP
# =============================================================================
print("\n\n" + "="*80)
print("⚙️  PHASE 4: SIMULATION SETUP")
print("="*80)

TOTAL_LAPS = 57
PIT_STOP_TIME_LOSS = 22.0
FEATURE_ORDER = X_train.columns.tolist()

TIRE_COMPOUNDS = {
    'SOFT': {'color': '🔴', 'deg_factor': 1.3},
    'MEDIUM': {'color': '🟡', 'deg_factor': 1.0},
    'HARD': {'color': '⚪', 'deg_factor': 0.7},
    'INTERMEDIATE': {'color': '🟢', 'deg_factor': 1.1},
    'WET': {'color': '🔵', 'deg_factor': 1.2}
}

# Default realism config
DEFAULT_REALISM_CONFIG = {
    'fuel_effect': True,
    'fuel_weight_per_lap': 0.035,
    'tire_warmup': True,
    'warmup_laps': 2,
    'warmup_penalty': 0.3,
    'traffic_effect': True,
    'traffic_probability': 0.15,
    'traffic_loss': (0.2, 0.8),
    'pit_variation': True,
    'pit_std_dev': 1.5,
    'random_variation': True,
    'lap_time_std_dev': 0.15,
    'track_evolution': True,
    'evolution_rate': 0.002,
}

REALISM_CONFIG = DEFAULT_REALISM_CONFIG.copy()

print(f"✅ Simulation parameters configured")
print(f"   • Race distance: {TOTAL_LAPS} laps")
print(f"   • Pit stop time: {PIT_STOP_TIME_LOSS}s")
print(f"   • Realism factors: {len(REALISM_CONFIG)} enabled")

# =============================================================================
# PHASE 5: DEFINE STRATEGIES
# =============================================================================
print("\n\n" + "="*80)
print("📋 PHASE 5: DEFINING RACE STRATEGIES")
print("="*80)

strategies_to_test = {
    "1-Stop (SOFT → MEDIUM)": {
        'name': '1-Stop (SOFT → MEDIUM)',
        'pit_stops': [20],
        'compounds': ['SOFT', 'MEDIUM'],
        'description': 'Aggressive start, conservative finish'
    },
    "1-Stop (MEDIUM → HARD)": {
        'name': '1-Stop (MEDIUM → HARD)',
        'pit_stops': [25],
        'compounds': ['MEDIUM', 'HARD'],
        'description': 'Balanced start, durable finish'
    },
    "2-Stop (SOFT → MEDIUM → SOFT)": {
        'name': '2-Stop (SOFT → MEDIUM → SOFT)',
        'pit_stops': [15, 40],
        'compounds': ['SOFT', 'MEDIUM', 'SOFT'],
        'description': 'Pace at start/end, stability in middle'
    },
    "2-Stop (MEDIUM → SOFT → MEDIUM)": {
        'name': '2-Stop (MEDIUM → SOFT → MEDIUM)',
        'pit_stops': [20, 35],
        'compounds': ['MEDIUM', 'SOFT', 'MEDIUM'],
        'description': 'Mid-race pace boost strategy'
    },
}

print(f"✅ {len(strategies_to_test)} strategies defined")
for name in strategies_to_test.keys():
    print(f"   • {name}")

# =============================================================================
# PHASE 6: SIMULATION ENGINE
# =============================================================================
print("\n\n" + "="*80)
print("🏁 PHASE 6: LOADING SIMULATION ENGINE")
print("="*80)

def simulate_race(strategy, total_laps, pit_time_loss, model, scaler, 
                 feature_order, realism_config, tire_compounds, verbose=False):
    """Realistic F1 race simulation with multiple factors."""
    
    current_stint = 1
    current_tyre_life = 1
    current_compound = strategy['compounds'][0]
    
    lap_times = []
    total_race_time = 0.0
    stint_details = []
    fuel_laps_remaining = total_laps
    
    for lap in range(1, total_laps + 1):
        # Create feature vector
        lap_features = {
            'LapNumber': float(lap),
            'Stint': float(current_stint),
            'TyreLife': float(current_tyre_life),
        }
        
        for compound in ['HARD', 'INTERMEDIATE', 'MEDIUM', 'SOFT', 'WET']:
            lap_features[f'Compound_{compound}'] = 0
        
        compound_key = f"Compound_{current_compound.upper()}"
        if compound_key in lap_features:
            lap_features[compound_key] = 1
        
        # Get base prediction
        lap_df = pd.DataFrame([lap_features])[feature_order]
        lap_scaled = scaler.transform(lap_df)
        base_time = model.predict(lap_scaled)[0]
        
        # Apply realism factors
        if realism_config.get('fuel_effect'):
            fuel_penalty = fuel_laps_remaining * realism_config.get('fuel_weight_per_lap', 0.035)
            base_time += fuel_penalty
            fuel_laps_remaining -= 1
        
        if realism_config.get('tire_warmup'):
            warmup_laps = realism_config.get('warmup_laps', 2)
            if current_tyre_life <= warmup_laps:
                warmup_penalty = realism_config.get('warmup_penalty', 0.3) * (warmup_laps - current_tyre_life + 1) / warmup_laps
                base_time += warmup_penalty
        
        if realism_config.get('traffic_effect'):
            if np.random.random() < realism_config.get('traffic_probability', 0.15):
                traffic_delay = np.random.uniform(*realism_config.get('traffic_loss', (0.2, 0.8)))
                base_time += traffic_delay
        
        if realism_config.get('track_evolution'):
            track_improvement = lap * realism_config.get('evolution_rate', 0.002)
            base_time -= track_improvement
        
        if realism_config.get('random_variation'):
            std_dev = realism_config.get('lap_time_std_dev', 0.15)
            random_var = np.random.normal(0, std_dev)
            base_time += random_var
        
        predicted_time = base_time
        pit_stop_made = False
        
        if lap in strategy['pit_stops']:
            if realism_config.get('pit_variation'):
                pit_std = realism_config.get('pit_std_dev', 1.5)
                actual_pit_time = max(18.0, np.random.normal(pit_time_loss, pit_std))
            else:
                actual_pit_time = pit_time_loss
            
            predicted_time += actual_pit_time
            pit_stop_made = True
            
            stint_details.append({
                'stint': current_stint,
                'compound': current_compound,
                'laps': current_tyre_life,
                'end_lap': lap
            })
            
            current_stint += 1
            current_compound = strategy['compounds'][current_stint - 1]
            current_tyre_life = 1
        else:
            current_tyre_life += 1
        
        lap_times.append({
            'lap': lap,
            'time': predicted_time,
            'compound': current_compound if not pit_stop_made else strategy['compounds'][current_stint - 2],
            'tyre_life': current_tyre_life - 1 if not pit_stop_made else current_tyre_life,
            'stint': current_stint if not pit_stop_made else current_stint - 1,
            'pit_stop': pit_stop_made,
            'fuel_load': fuel_laps_remaining
        })
        
        total_race_time += predicted_time
    
    stint_details.append({
        'stint': current_stint,
        'compound': current_compound,
        'laps': current_tyre_life,
        'end_lap': total_laps
    })
    
    return total_race_time, lap_times, stint_details

print("✅ Simulation engine loaded")

# =============================================================================
# PHASE 7: PARAMETER OPTIMIZATION
# =============================================================================
print("\n\n" + "="*80)
print("🔧 PHASE 7: OPTIMIZING SIMULATION PARAMETERS")
print("="*80)
print("⏳ This will take 2-3 minutes...")
print("💡 Finding parameters that best match actual race data...\n")

def optimize_simulation_parameters(df, model, scaler, feature_order, 
                                   total_laps, pit_stop_time, n_iterations=20):
    """Optimize simulation parameters using differential evolution."""
    
    actual_avg = df['LapTime'].mean()
    actual_std = df['LapTime'].std()
    
    test_strategy = {
        'name': 'Test',
        'pit_stops': [28],
        'compounds': ['MEDIUM', 'MEDIUM']
    }
    
    def objective(params):
        fuel_weight, warmup_penalty, traffic_prob, traffic_max, pit_std, lap_std, evolution = params
        
        test_config = {
            'fuel_effect': True,
            'fuel_weight_per_lap': fuel_weight,
            'tire_warmup': True,
            'warmup_laps': 2,
            'warmup_penalty': warmup_penalty,
            'traffic_effect': True,
            'traffic_probability': traffic_prob,
            'traffic_loss': (0.2, traffic_max),
            'pit_variation': True,
            'pit_std_dev': pit_std,
            'random_variation': True,
            'lap_time_std_dev': lap_std,
            'track_evolution': True,
            'evolution_rate': evolution,
        }
        
        try:
            total_time, lap_times, _ = simulate_race(
                test_strategy, total_laps, pit_stop_time,
                model, scaler, feature_order, test_config, TIRE_COMPOUNDS, False
            )
            
            sim_times = [lt['time'] for lt in lap_times if not lt['pit_stop']]
            sim_avg = np.mean(sim_times)
            sim_std = np.std(sim_times)
            
            avg_error = abs(sim_avg - actual_avg) / actual_avg
            std_error = abs(sim_std - actual_std) / actual_std
            
            return 0.7 * avg_error + 0.3 * std_error
        except:
            return 1000.0
    
    bounds = [
        (0.020, 0.050),   # fuel_weight
        (0.1, 0.5),       # warmup_penalty
        (0.05, 0.30),     # traffic_prob
        (0.5, 1.5),       # traffic_max
        (0.5, 3.0),       # pit_std
        (0.05, 0.30),     # lap_std
        (0.001, 0.005),   # evolution
    ]
    
    result = differential_evolution(
        objective, bounds, maxiter=n_iterations,
        popsize=8, seed=42, polish=True, workers=1
    )
    
    optimal = result.x
    optimized_config = {
        'fuel_effect': True,
        'fuel_weight_per_lap': optimal[0],
        'tire_warmup': True,
        'warmup_laps': 2,
        'warmup_penalty': optimal[1],
        'traffic_effect': True,
        'traffic_probability': optimal[2],
        'traffic_loss': (0.2, optimal[3]),
        'pit_variation': True,
        'pit_std_dev': optimal[4],
        'random_variation': True,
        'lap_time_std_dev': optimal[5],
        'track_evolution': True,
        'evolution_rate': optimal[6],
    }
    
    return optimized_config, optimal, result.fun

try:
    optimized_config, optimal_params, error = optimize_simulation_parameters(
        df, model, scaler, FEATURE_ORDER, TOTAL_LAPS, PIT_STOP_TIME_LOSS, 20
    )
    
    REALISM_CONFIG = optimized_config
    
    print("\n✅ OPTIMIZATION COMPLETE!")
    print(f"   • Final error: {error*100:.2f}%")
    print(f"   • Fuel weight: {optimal_params[0]*1000:.1f} ms/lap")
    print(f"   • Warmup penalty: {optimal_params[1]:.3f}s")
    print(f"   • Traffic prob: {optimal_params[2]*100:.1f}%")
    print(f"   • Optimized parameters applied!")
    
except Exception as e:
    print(f"\n⚠️  Optimization failed: {str(e)}")
    print("   Using default parameters instead.")

# =============================================================================
# PHASE 8: RUN SIMULATIONS
# =============================================================================
print("\n\n" + "="*80)
print("🏁 PHASE 8: RUNNING RACE SIMULATIONS")
print("="*80)

results = {}
for strategy_name, strategy_def in strategies_to_test.items():
    print(f"   🏎️  Simulating: {strategy_name}...")
    
    total_time, lap_times, stint_info = simulate_race(
        strategy_def, TOTAL_LAPS, PIT_STOP_TIME_LOSS,
        model, scaler, FEATURE_ORDER, REALISM_CONFIG, TIRE_COMPOUNDS, False
    )
    
    results[strategy_name] = {
        'total_time': total_time,
        'lap_times': lap_times,
        'stint_info': stint_info,
    }

print(f"\n✅ {len(results)} strategies simulated")

# =============================================================================
# PHASE 9: GENERATE RESULTS
# =============================================================================
print("\n\n" + "="*80)
print("📊 PHASE 9: GENERATING RESULTS")
print("="*80)

# Find optimal strategy
optimal_strategy = min(results.items(), key=lambda x: x[1]['total_time'])

print(f"\n🏆 OPTIMAL STRATEGY: {optimal_strategy[0]}")
print(f"   • Race time: {optimal_strategy[1]['total_time']/60:.2f} minutes")

# Compare all strategies
print(f"\n📊 All Strategies (ranked):")
sorted_results = sorted(results.items(), key=lambda x: x[1]['total_time'])
for i, (name, data) in enumerate(sorted_results, 1):
    delta = (data['total_time'] - optimal_strategy[1]['total_time'])
    print(f"   {i}. {name}: {data['total_time']/60:.2f} min (+{delta:.1f}s)")

# =============================================================================
# COMPLETE
# =============================================================================
print("\n\n" + "="*80)
print("✅ SIMULATION PIPELINE COMPLETE!")
print("="*80)
print("\n📊 Summary:")
print(f"   • Data loaded: {len(df):,} laps")
print(f"   • Model R²: {r2:.4f}")
print(f"   • Strategies tested: {len(results)}")
print(f"   • Optimal: {optimal_strategy[0]}")
print(f"\n💾 Results stored in 'results' dictionary")
print("="*80)
