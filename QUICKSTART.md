# 🏎️ F1 Strategy System v3.1.0 - Quick Start Guide

Get started with F1 race predictions in 3 minutes!

---

## ⚡ Fast Track (3 Commands)

```bash
# 1. Setup & install dependencies
python app.py --setup

# 2. Train ML models
python app.py --train

# 3. Predict next race
python app.py
```

Done! You now have AI-powered F1 race predictions 🎉

## Prerequisites

- ✅ Python 3.8 or higher
- ✅ Internet connection
- ✅ That's it! (Dependencies auto-install)

## Super Quick Start ⚡

### ONE COMMAND - That's All! 🎉

```bash
# Just run this - it does everything automatically!
python app.py
```

**Yes, really!** The system will:
1. ✅ Check for required packages
2. ✅ Auto-install missing dependencies (first time only)
3. ✅ Download F1 data
4. ✅ Show predictions

**First run:** ~2-5 minutes (one-time setup)  
**Subsequent runs:** ~30 seconds

---

## What Happens Behind the Scenes

### First Time Running:
```bash
python app.py
```

Output:
```
================================================================================
🔧 FIRST-TIME SETUP: Installing required dependencies...
================================================================================

Missing packages: 6
This is a one-time setup that will take 2-5 minutes.

📦 Installing pandas>=2.0.0...
   ✅ pandas>=2.0.0 installed
📦 Installing numpy>=1.24.0...
   ✅ numpy>=1.24.0 installed
📦 Installing fastf1>=3.6.0...
   ✅ fastf1>=3.6.0 installed
...

✅ All dependencies installed successfully!
================================================================================

🏎️ F1 RACE PREDICTION SYSTEM v2.3
... (continues with predictions)
```

### Every Other Time:
```bash
python app.py
```

Instantly starts (dependencies already installed)!

---

## Old Way vs New Way

### ❌ Old Way (Manual):
```bash
git clone https://github.com/EgemenAnil/f1strat.git
cd f1strat
pip install -r requirements.txt  # ← User has to know this
python app.py
```

### ✅ New Way (Automatic):
```bash
git clone https://github.com/EgemenAnil/f1strat.git
cd f1strat
python app.py  # ← That's it!
```

**50% fewer steps! 🎉**

---

## Detailed Installation

### 1️⃣ Install Dependencies

```bash
# Activate virtual environment
source f1-env/bin/activate

# Install all required packages
pip install -r requirements.txt
```

### 2️⃣ Setup with Wizard

```bash
# Interactive setup
python app.py --setup
```

The wizard will:
- ✅ Check Python version
- ✅ Install dependencies
- ✅ Create .env file
- ✅ Guide you through API key setup

### 3️⃣ Get API Key

1. Go to: https://openweathermap.org/api
2. Sign up for **free account**
3. Get your **API key** from dashboard
4. Edit `.env` and add your key:
   ```
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

### 4️⃣ Test Installation

```bash
python app.py --test
```

Expected output:
```
✓ All modules imported successfully
✓ Track database working
✓ Crash predictor working
✓ Strategy optimizer working
✓ ALL TESTS PASSED
```

## Usage

### The Easy Way: Single Command! 🎯

```bash
python app.py
```

That's it! The app will:
1. 🔍 Auto-detect the next F1 race
2. 🌤️ Fetch weather forecast
3. 🏁 Analyze track characteristics
4. 📊 Calculate crash probabilities
5. 🎯 Optimize pit stop strategies
6. 💾 Save prediction to JSON file

### All Available Commands

```bash
# Predict next race (default)
python app.py

# Run system tests
python app.py --test

# Setup wizard (first time)
python app.py --setup

# Show help
python app.py --help
```

### Example Output

```
================================================================================
RACE PREDICTION SUMMARY
================================================================================

📍 Belgian Grand Prix
   Spa-Francorchamps
   2024-07-28

🌤 Weather Forecast:
   Temperature: 18°C
   Rain Probability: 65%

⚠️  Risk Assessment:
   Track Risk: Medium
   Safety Car Probability: 50%

🏁 RECOMMENDED STRATEGY:
   OPTIMAL STRATEGY: 1-Stop: M18S
   Compounds: MEDIUM → SOFT
   Pit on laps: 18
   ⚠ HIGH RAIN RISK (65%): Have intermediates ready

💾 Prediction saved to: prediction_Belgian_Grand_Prix.json
```

## Python API Usage

```python
# Option 1: Use the app (recommended for beginners)
# Just run: python app.py

# Option 2: Use as Python library (advanced)
from predict_upcoming_race import F1RacePredictionPipeline

# Initialize
pipeline = F1RacePredictionPipeline()

# Predict next race
prediction = pipeline.predict_upcoming_race()

# Print results
pipeline.print_prediction(prediction)

# Access data
strategy = prediction['optimal_strategies']['balanced']
print(f"Best strategy: {strategy.name}")
print(f"Pit laps: {strategy.pit_laps}")
```

## Project Structure

```
f1strat/
├── app.py                       ⭐ MAIN APP (use this!)
├── run_tests.py                 🧪 Test components
├── predict_upcoming_race.py     📦 Core prediction engine
├── requirements.txt             📦 Dependencies
├── .env.example                🔧 Config template
│
├── src/                        📁 Core package
│   ├── data/                      - Data fetching
│   ├── features/                  - Feature engineering
│   └── models/                    - ML models
│
├── config/                     ⚙️ Configuration files
├── historical_data/            📊 CSV files (past races)
├── archive/                    📦 Old version (v1.x)
└── README.md                   📖 Full documentation
```

## Common Commands

```bash
# Quick prediction (most common use)
python app.py

# First time setup
python app.py --setup

# Test everything is working
python app.py --test

# Get help
python app.py --help

# Advanced: Run specific modules
python run_tests.py              # Component tests
python predict_upcoming_race.py  # Direct prediction
```

## Troubleshooting

### Problem: "No module named 'sklearn'"
**Solution:**
```bash
source f1-env/bin/activate
pip install -r requirements.txt
```

### Problem: "API key not found"
**Solution:**
```bash
# Run setup wizard
python app.py --setup

# Or manually check .env file
cat .env | grep OPENWEATHER_API_KEY
# Should output: OPENWEATHER_API_KEY=your_key_here
```

### Problem: "No upcoming race found"
**Explanation:**
- System checks current + next calendar year
- If season ended, it will notify you
- You can still analyze historical data

### Problem: Prediction fails
**Solution:**
```bash
# Step 1: Run diagnostics
python app.py --test

# Step 2: Check setup
python app.py --setup

# Step 3: Verify internet connection
ping openweathermap.org
```

## Next Steps

After first successful prediction:

1. 📚 Read full docs: `README.md`
2. 🎓 Check project status: `PROJECT_STATUS.md`
3. � Understand file structure: `FILE_GUIDE.md`
4. �🔧 Customize configs: `config/*.yaml`
5. 🧪 Explore old version: `archive/`
6. 📊 Analyze historical data: `historical_data/`

## Getting Help

- **Quick Help**: `python app.py --help`
- **Documentation**: See `README.md`
- **Examples**: Check `src/models/` module docstrings
- **Tests**: Run `python app.py --test` to verify setup
- **Old version**: Educational material in `archive/`

## Features

✅ **Single command execution** - Just run `python app.py`!
✅ Automatic upcoming race detection
✅ Real-time weather forecasts
✅ Optimal pit stop strategies
✅ Crash/Safety car predictions
✅ 22 F1 circuits database
✅ Multiple risk profiles
✅ JSON export
✅ Monte Carlo simulation
✅ Interactive setup wizard
✅ Built-in testing

---

**Ready to race?** Just run: `python app.py` 🏎️💨
