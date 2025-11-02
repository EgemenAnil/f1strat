# F1 Race Prediction System v2.0

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/EgemenAnil/f1strat/graphs/commit-activity)

🏎️ **Professional Formula 1 race prediction system using machine learning and advanced simulation.**

**Key Features:** Single-command operation • Real-time weather • AI-powered strategies • 22 F1 circuits • Safety car prediction

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Setup (first time only)
python app.py --setup

# 2. Add API key to .env file
# Get free key: https://openweathermap.org/api

# 3. Run prediction
python app.py
```

**That's it!** See [QUICKSTART.md](QUICKSTART.md) for details.

---

## Features

### 🎯 Core Capabilities
- **Single Command Operation**: Just run `python app.py` - everything else is automatic!
- **Upcoming Race Prediction**: Automatically detects and predicts the next F1 race
- **Weather Integration**: Real-time weather forecasts via OpenWeatherMap API
- **Optimal Strategy**: AI-powered pit stop strategy optimization
- **Crash Prediction**: Statistical modeling of safety car and incident probabilities
- **Traffic Simulation**: Realistic modeling of race traffic and overtaking
- **Track-Specific Analysis**: Detailed characteristics for all 22+ F1 circuits
- **Interactive Setup**: Built-in wizard guides you through first-time setup

### 🧠 Machine Learning Models
- **XGBoost**: Fast and accurate lap time prediction
- **Neural Networks**: Deep learning for complex pattern recognition
- **Ensemble Methods**: Combining multiple models for better accuracy
- **Monte Carlo Simulation**: Statistical race outcome prediction

### 📊 Advanced Features
- Real-time weather impact on tire performance
- Fuel weight effect simulation (car gets lighter → faster)
- Tire warm-up penalties and degradation modeling
- Track evolution (rubber buildup)
- Position-based traffic probability
- Safety car and red flag prediction
- Multiple risk profiles (conservative, balanced, aggressive)

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Quick Setup

```bash
# Clone repository
cd f1strat

# Create virtual environment
python -m venv f1-env

# Activate environment
source f1-env/bin/activate  # macOS/Linux
# or
f1-env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements_new.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key
```

### Get OpenWeatherMap API Key
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` file

## Usage

### Quick Start: Predict Next Race

```bash
# Predict the upcoming F1 race
python predict_race.py
```

This will:
1. ✅ Auto-detect next F1 race
2. ✅ Fetch weather forecast
3. ✅ Analyze track characteristics
4. ✅ Calculate crash/incident probabilities
5. ✅ Optimize pit stop strategies
6. ✅ Generate comprehensive race prediction
7. ✅ Save results to JSON file

### Example Output

```
===============================================================================
F1 RACE PREDICTION SYSTEM
===============================================================================

[1/7] Fetching upcoming race information...
✓ Next Race: Belgian Grand Prix
  Date: 2024-07-28
  Circuit: Spa-Francorchamps

[2/7] Fetching weather forecast...
✓ Weather Forecast:
  Temperature: 18°C
  Rain Probability: 65%
  Humidity: 78%

[3/7] Analyzing track characteristics...
✓ Track Analysis:
  Length: 7.004 km
  Corners: 19
  Overtaking Difficulty: 40.0%
  Typical Pit Loss: 25.0s

[4/7] Calculating incident probabilities...
✓ Risk Analysis:
  Risk Level: Medium
  Safety Car Probability: 50%
  Expected Incidents: 0.50

[5/7] Preparing race prediction model...
[6/7] Optimizing pit stop strategies...
✓ Strategy Optimization Complete

[7/7] Compiling predictions...
✓ Prediction Complete!

===============================================================================
RACE PREDICTION SUMMARY
===============================================================================

🏁 RECOMMENDED STRATEGY:
   OPTIMAL STRATEGY: 1-Stop: M18S
   Compounds: MEDIUM → SOFT
   Pit on laps: 18
   ⚠ HIGH RAIN RISK (65%): Have intermediates ready, consider early pit stop
```

### Python API Usage

```python
from predict_race import F1RacePredictionPipeline

# Initialize pipeline
pipeline = F1RacePredictionPipeline()

# Predict next race
prediction = pipeline.predict_upcoming_race()

# Print results
pipeline.print_prediction(prediction)

# Access specific data
optimal_strategy = prediction['optimal_strategies']['balanced']
print(f"Best strategy: {optimal_strategy.name}")
print(f"Pit laps: {optimal_strategy.pit_laps}")
print(f"Expected time: {optimal_strategy.expected_time:.1f}s")
```

### Custom Predictions

```python
from src.models.strategy_optimizer import StrategyOptimizer
from src.models.crash_predictor import CrashPredictor

# Create custom strategy optimizer
optimizer = StrategyOptimizer(total_laps=58)

# Define weather conditions
weather = {
    'temperature': 25,
    'rain_probability': 0.3,
    'humidity': 60
}

# Get optimal strategy
strategy = optimizer.get_optimal_strategy(
    weather_forecast=weather,
    track_name="Monza",
    risk_tolerance='aggressive'
)

print(f"Optimal: {strategy.name}")
print(f"Compounds: {strategy.compounds}")
print(f"Pit laps: {strategy.pit_laps}")
```

## Project Structure

```
f1strat/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── fetcher.py          # F1 data fetching + weather API
│   ├── features/
│   │   ├── __init__.py
│   │   ├── engineering.py       # Feature engineering
│   │   └── track_features.py    # Track characteristics
│   ├── models/
│   │   ├── __init__.py
│   │   ├── race_predictor.py    # ML models (XGBoost, NN)
│   │   ├── strategy_optimizer.py # Strategy optimization
│   │   └── crash_predictor.py   # Incident prediction
│   └── simulation/              # Race simulation (future)
├── config/
│   ├── model_config.yaml        # ML hyperparameters
│   └── simulation_config.yaml   # Simulation settings
├── predict_race.py              # Main prediction script
├── requirements_new.txt         # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Configuration

### Model Configuration (`config/model_config.yaml`)
- XGBoost hyperparameters
- Neural network architecture
- Feature engineering settings
- Training configuration

### Simulation Configuration (`config/simulation_config.yaml`)
- Tire compound parameters
- Realism factors (fuel, traffic, weather)
- Strategy constraints
- Risk profiles

## Advanced Usage

### Training Custom Models

```python
from src.models.race_predictor import F1RacePredictor
import pandas as pd

# Load historical data
df = pd.read_csv('historical_race_data.csv')

# Initialize and train model
predictor = F1RacePredictor(model_type='xgboost')
metrics = predictor.train(df, target_col='LapTimeSeconds')

# Save model
predictor.save('my_model.pkl')
```

### Track Risk Analysis

```python
from src.models.crash_predictor import CrashPredictor

predictor = CrashPredictor()

# Analyze track risk
risk = predictor.analyze_track_risk("Monaco")
print(f"Risk: {risk['risk_category']}")
print(f"Safety Car Prob: {risk['expected_safety_cars']:.0%}")

# Get optimal pit windows (high incident probability)
windows = predictor.get_optimal_pit_windows(
    total_laps=78,
    track_name="Monaco"
)
```

## API Reference

### Main Classes

#### `F1RacePredictionPipeline`
Complete prediction pipeline integrating all components.

**Methods:**
- `predict_upcoming_race()` - Predict next F1 race
- `print_prediction(prediction)` - Pretty print results
- `train_model_from_historical_data(years)` - Train ML model

#### `StrategyOptimizer`
Optimize pit stop strategies.

**Methods:**
- `generate_strategies(weather)` - Generate viable strategies
- `simulate_strategy(strategy, weather)` - Simulate one strategy
- `optimize(weather, track_name)` - Find optimal strategies
- `get_optimal_strategy(weather, track, risk)` - Get best strategy

#### `CrashPredictor`
Predict incidents and safety cars.

**Methods:**
- `calculate_lap_incident_probability(lap, weather)` - Per-lap risk
- `simulate_race_incidents(total_laps, weather)` - Full race simulation
- `calculate_safety_car_probability(laps, weather)` - SC probability
- `analyze_track_risk(track_name)` - Track risk profile

#### `F1FeatureEngineer`
Create ML features from raw data.

**Methods:**
- `create_all_features(df)` - Create all features
- `create_weather_features(df)` - Weather-based features
- `create_tire_degradation_features(df)` - Tire features
- `create_crash_risk_features(df)` - Risk features

## Dependencies

### Core
- `fastf1>=3.6.0` - F1 data access
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing

### Machine Learning
- `xgboost>=2.0.0` - Gradient boosting
- `torch>=2.0.0` - Neural networks
- `lightgbm>=4.0.0` - Additional ML models
- `scikit-learn>=1.3.0` - ML utilities

### Web & APIs
- `requests>=2.31.0` - API calls
- `python-dotenv>=1.0.0` - Environment variables

### Visualization (Optional)
- `matplotlib>=3.7.0`
- `seaborn>=0.12.0`

## Troubleshooting

### Import Errors
```bash
# If you get import errors, ensure you're in the project root
cd /path/to/f1strat
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Weather API Issues
```bash
# Verify API key is set
cat .env | grep OPENWEATHER_API_KEY

# Test API manually
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENWEATHER_API_KEY'))"
```

### FastF1 Cache Issues
```bash
# Clear cache if data seems outdated
rm -rf cache/*
```

## Future Enhancements

See [CHANGELOG.md](CHANGELOG.md) for version history and roadmap.

### Planned Features

**v2.1.0:**
- [ ] FastAPI web service
- [ ] Streamlit dashboard UI
- [ ] Database integration for prediction history
- [ ] Historical prediction accuracy tracking

**v2.2.0:**
- [ ] Real-time race monitoring
- [ ] Driver/team performance modeling
- [ ] Qualifying simulation
- [ ] Grid position optimization

**v3.0.0:**
- [ ] Live telemetry streaming
- [ ] Mobile app
- [ ] Advanced neural networks
- [ ] Multi-language support

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📚 Improve documentation
- 🧪 Add tests
- 🎨 Enhance UI/UX
- 🚀 Submit pull requests

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Egemen Anil

## Credits & Acknowledgments

### Technologies
- **[FastF1](https://github.com/theOehrly/Fast-F1)** - F1 telemetry data library by theOehrly
- **[OpenWeatherMap](https://openweathermap.org/)** - Weather forecast API
- **[XGBoost](https://xgboost.readthedocs.io/)** - Gradient boosting framework
- **[PyTorch](https://pytorch.org/)** - Deep learning library
- **[scikit-learn](https://scikit-learn.org/)** - Machine learning toolkit
- **[pandas](https://pandas.pydata.org/)** - Data manipulation library

### Inspiration
This project was inspired by the fascinating world of F1 strategy and the desire to make data-driven race predictions accessible to everyone.

### Data Sources
- Formula 1 telemetry data via FastF1
- Historical weather data
- FIA sporting regulations
- Track characteristics from official F1 sources

## Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

## Contact

- **GitHub**: [@EgemenAnil](https://github.com/EgemenAnil)
- **Project**: [f1strat](https://github.com/EgemenAnil/f1strat)
- **Issues**: [Report a bug](https://github.com/EgemenAnil/f1strat/issues)

## Disclaimer

This is a **prediction tool** for educational and analytical purposes. Race outcomes depend on many unpredictable factors including driver skill, team decisions, mechanical failures, and weather changes. Use predictions as insights, not certainties.

**Not affiliated with Formula 1, FIA, or any F1 teams.**

---

**Made with ❤️ for F1 strategy analysis**

🏁 *May your strategies be optimal and your tires never blister!* 🏎️💨

- **FastF1**: F1 telemetry data library
- **OpenWeatherMap**: Weather forecast API
- **XGBoost**: Machine learning library
- **PyTorch**: Deep learning framework

---

Made with ❤️ for F1 strategy nerds
