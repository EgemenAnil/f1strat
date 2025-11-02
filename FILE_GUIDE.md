# 📁 F1 Race Prediction System - File Organization Guide

**Last Updated:** 2 Kasım 2025

---

## 🎯 Main Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| **`app.py`** | 🚀 **MAIN APPLICATION** | `python app.py` |
| **`app.py --setup`** | 🔧 **Setup wizard** | First-time configuration |
| **`app.py --test`** | 🧪 **System tests** | Verify installation |
| **`app.py --help`** | ❓ **Help** | Show all commands |
| | | |
| `predict_upcoming_race.py` | 📦 Core prediction engine | Advanced users only |
| `run_tests.py` | 🧪 Component tests | Alternative to --test |
| **`QUICKSTART.md`** | 📖 **Quick start guide** | Read first! |
| **`README.md`** | 📚 **Full documentation** | Complete guide |

**For normal use, just run:** `python app.py`

---

## 📦 Core Package (`src/`)

```
src/
├── __init__.py              Package root
│
├── data/                    Data acquisition & processing
│   ├── __init__.py
│   └── fetcher.py          F1DataFetcher class
│                            - Auto-detect upcoming races
│                            - Weather API integration
│                            - Historical data fetching
│
├── features/                Feature engineering
│   ├── __init__.py
│   ├── engineering.py      F1FeatureEngineer class
│   │                        - 50+ engineered features
│   │                        - Weather, tire, fuel features
│   └── track_features.py   TrackFeatures class
│                            - 22 F1 circuit database
│
├── models/                  Machine learning models
│   ├── __init__.py
│   ├── race_predictor.py   F1RacePredictor class
│   │                        - XGBoost & Neural Networks
│   ├── strategy_optimizer.py  StrategyOptimizer class
│   │                        - Pit stop optimization
│   └── crash_predictor.py  CrashPredictor class
│                            - Incident predictions
│
└── simulation/             Race simulation (future expansion)
    └── __init__.py
```

---

## ⚙️ Configuration (`config/`)

| File | Contains |
|------|----------|
| **`model_config.yaml`** | ML model hyperparameters, training settings |
| **`simulation_config.yaml`** | Tire compounds, realism factors, optimization |

---

## 📊 Data Directories

### `historical_data/`
Historical race data (CSV files) used for analysis and model training:
- `2020_Turkey_R_laps_clean.csv`
- `2021_Abu_Dhabi_R_laps_clean.csv`
- `2023_Bahrain_R_laps_clean.csv`
- `2025_Italian_Grand_Prix_R_laps_clean.csv`

### `cache/`
FastF1 automatic cache (auto-generated, ignored by git)

---

## 📦 Archive (`archive/`)

**Previous version (v1.x)** - Educational material:
- `analysis.ipynb` - Original 30-section notebook
- `get_data.py` - Old data fetcher
- `run_simulation.py` - Old simulation script
- `README.md` - Archive documentation

**Still usable for:**
- Learning F1 concepts
- Historical analysis
- Educational purposes

---

## 📝 Documentation Files

| File | Description |
|------|-------------|
| **`README.md`** | Complete documentation, API reference, examples |
| **`QUICKSTART.md`** | 5-minute setup guide |
| **`PROJECT_STATUS.md`** | Development status, features, roadmap |
| **`FILE_GUIDE.md`** | This file - project organization |

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| **`.env.example`** | Environment variables template |
| **`.env`** | Your API keys (create from .env.example) |
| **`.gitignore`** | Git ignore rules |
| **`requirements.txt`** | Python dependencies |

---

## 🚫 What NOT to Touch

### Auto-generated (Git Ignored)
- `cache/` - FastF1 cache
- `__pycache__/` - Python bytecode
- `.env` - Your API keys
- `f1-env/` - Virtual environment
- `prediction_*.json` - Output files

### System Files
- `.git/` - Git repository
- `.DS_Store` - Mac system files

---

## 🎯 Quick Reference

### The Easy Way (Recommended for Everyone):
```bash
# First time
python app.py --setup

# Normal use
python app.py

# Test
python app.py --test

# Help
python app.py --help
```

### Advanced Usage:
```bash
# Direct prediction (skip app.py wrapper)
python predict_upcoming_race.py

# Component tests (detailed)
python run_tests.py
```

### To Import Modules:
```python
from src.data.fetcher import F1DataFetcher
from src.features.engineering import F1FeatureEngineer
from src.models.strategy_optimizer import StrategyOptimizer
from src.models.crash_predictor import CrashPredictor
```

### To Access Track Data:
```python
from src.features.track_features import TrackFeatures
track_info = TrackFeatures.get_track_info('Monaco')
```

---

## 📊 File Stats

### Current Project Size:
- **Python files**: 8 main modules
- **Config files**: 2 YAML files
- **Documentation**: 4 markdown files
- **Historical data**: 4 CSV files
- **Total lines of code**: ~2,500+ lines

### Archived (v1.x):
- **Notebook**: 1 file (30 sections)
- **Scripts**: 2 Python files
- **Still functional**: ✅ Yes

---

## 🗂️ Recommended Workflow

1. **First Time Setup**:
   - Read `QUICKSTART.md`
   - Set up `.env` file
   - Run `python run_tests.py`

2. **Regular Use**:
   - Run `python predict_upcoming_race.py`
   - Check output JSON files
   - Customize configs if needed

3. **Development**:
   - Edit files in `src/`
   - Update configs in `config/`
   - Run tests after changes

4. **Learning**:
   - Explore `archive/` for v1.x
   - Read module docstrings
   - Check `PROJECT_STATUS.md`

---

## 🎓 File Naming Convention

✅ **Clear Action-Based Names:**
- `predict_upcoming_race.py` - Does what it says
- `run_tests.py` - Runs tests
- `QUICKSTART.md` - Quick start guide

✅ **Organized Directories:**
- `src/` - Source code
- `config/` - Configuration
- `archive/` - Old versions
- `historical_data/` - Data files

✅ **Descriptive Module Names:**
- `fetcher.py` - Fetches data
- `engineering.py` - Engineers features
- `strategy_optimizer.py` - Optimizes strategies

---

**Everything is organized, nothing is wasted!** 🎯
