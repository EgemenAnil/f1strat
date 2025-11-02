# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-02

### 🎉 Major Release - Complete System Transformation

This release represents a complete rewrite of the F1 strategy analysis system, transforming it from an educational notebook into a production-ready race prediction platform.

### Added

#### Core Features
- **Single-command application** (`app.py`) with interactive setup wizard
- **Automatic upcoming race detection** - no manual input needed
- **Real-time weather integration** via OpenWeatherMap API
- **Professional ML models** - XGBoost and PyTorch Neural Networks
- **Crash probability prediction** with safety car forecasting
- **Traffic simulation** with position-based modeling
- **22 F1 circuit database** with detailed track characteristics
- **Monte Carlo simulation** for statistical confidence
- **Multiple risk profiles** (conservative, balanced, aggressive)

#### Technical Improvements
- Modular package structure (`src/` with proper separation)
- Configuration management via YAML files
- Comprehensive feature engineering (50+ derived features)
- Weather impact modeling (temperature, rain, wind, humidity)
- Tire degradation modeling (compound-specific)
- Fuel weight effect simulation
- Track evolution modeling (rubber buildup)
- Pit stop variation and timing optimization

#### User Experience
- **Interactive setup wizard** (`python app.py --setup`)
- **Built-in testing** (`python app.py --test`)
- **Colorful terminal output** with clear status messages
- **Automatic setup verification** before prediction
- **JSON export** for further analysis
- **Comprehensive documentation** (5 guides: USAGE, QUICKSTART, README, FILE_GUIDE, PROJECT_STATUS)

#### Documentation
- `USAGE.md` - Ultra-simple user guide
- `QUICKSTART.md` - 5-minute setup guide
- `FILE_GUIDE.md` - Project structure reference
- `PROJECT_STATUS.md` - Technical details and roadmap
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - This file

### Changed

- **Renamed files for clarity**:
  - `predict_race.py` → `predict_upcoming_race.py`
  - `test_system.py` → `run_tests.py`
  - `requirements_new.txt` → `requirements.txt`
  - `README_NEW.md` → `README.md`

- **Reorganized project structure**:
  - Old files moved to `archive/` folder
  - CSV files moved to `historical_data/` folder
  - Source code organized into `src/` package
  - Configuration files in `config/` folder

- **Enhanced dependencies**:
  - Added XGBoost for gradient boosting
  - Added PyTorch for neural networks
  - Added LightGBM as alternative ML framework
  - Added Optuna for hyperparameter optimization
  - Added FastAPI and Streamlit for future web interface

### Improved

- **Strategy optimization**: Now generates 194 viable FIA-compliant strategies
- **Feature engineering**: Expanded from ~20 to 50+ features
- **Model accuracy**: Multiple ML models with ensemble capability
- **Error handling**: Comprehensive error messages with solutions
- **Code quality**: Type hints, docstrings, and proper documentation

### Fixed

- FastF1 auto-correction issue with track name validation
- Jupyter notebook cell ordering complexity
- Manual parameter tuning inefficiency
- Missing weather impact in simulations
- No-stop strategies violating FIA regulations

### Deprecated

- Jupyter notebook interface (moved to `archive/`)
- Manual data fetcher script (moved to `archive/`)
- Standalone simulation script (moved to `archive/`)

### Removed

- Turkish language strings (fully English now)
- Hardcoded parameters (now in config files)
- Duplicate requirements files
- Scattered CSV files (organized into folder)

## [1.0.0] - 2024-10-29

### Initial Release (Archived)

- Educational Jupyter notebook with 30 sections
- Historical race analysis
- Basic strategy simulation
- Linear regression model
- Manual data fetching
- Turkish/English mixed codebase

---

## Migration Guide from v1.x to v2.0

### For Users

**Old way:**
```bash
jupyter notebook analysis.ipynb
# Navigate through 30 cells, run each manually
```

**New way:**
```bash
python app.py
# That's it!
```

### For Developers

**Old structure:**
```
- analysis.ipynb (monolithic)
- get_data.py
- run_simulation.py
```

**New structure:**
```
- app.py (main entry)
- src/data/fetcher.py
- src/features/engineering.py
- src/models/race_predictor.py
- src/models/strategy_optimizer.py
- src/models/crash_predictor.py
```

### Breaking Changes

1. **API Changes**: Module imports changed (see FILE_GUIDE.md)
2. **Configuration**: Now uses YAML files instead of hardcoded values
3. **Data Location**: CSV files moved to `historical_data/`
4. **Entry Point**: Use `app.py` instead of notebook

### Upgrade Steps

1. Install new dependencies: `pip install -r requirements.txt`
2. Get OpenWeatherMap API key
3. Run setup: `python app.py --setup`
4. Test: `python app.py --test`
5. Use: `python app.py`

Old notebook still available in `archive/` folder for reference.

---

## Future Roadmap

### v2.1.0 (Planned)
- FastAPI REST endpoints
- Streamlit dashboard
- Database integration
- Historical prediction tracking

### v2.2.0 (Planned)
- Driver/team performance modeling
- Qualifying simulation
- Grid position optimization
- Real-time race monitoring

### v3.0.0 (Future)
- Live race updates
- Telemetry streaming
- Advanced ML models
- Mobile app

---

**Legend:**
- 🎉 Major features
- ✨ Minor features
- 🐛 Bug fixes
- 📚 Documentation
- ⚠️ Breaking changes
- 🗑️ Deprecations
