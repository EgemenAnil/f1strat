# 🏎️ F1 Strategy Prediction System v3.1.0

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-3.1.0-green.svg)](https://github.com/EgemenAnil/f1strat)
[![FastF1](https://img.shields.io/badge/FastF1-3.6+-red.svg)](https://github.com/theOehrly/Fast-F1)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Accuracy](https://img.shields.io/badge/accuracy-83.3%25-brightgreen.svg)](VALIDATION_SUMMARY.md)

**Professional Formula 1 race strategy prediction system powered by Enhanced ML Ensemble**

> **83.3% strategy accuracy** • **100% pit lap accuracy** • **One-command setup** • **Real 2025 data**

Predict optimal F1 pit stop strategies using **machine learning ensemble** (RandomForest + GradientBoosting + AdaBoost), **real-time weather**, and **2025 season data**. Ready in **90 seconds**.

---

## ⚡ Quick Start

**No installation needed - just run:**

```bash
# Clone repository
git clone https://github.com/EgemenAnil/f1strat.git
cd f1strat

# Run (auto-installs everything)
python app.py
```

First run will:
- ✅ Auto-install all dependencies (100+ packages)
- ✅ Set up environment (.env file)
- ✅ Train ML models (83.3% accuracy)
- ✅ Predict next race

**Setup time:** ~90 seconds

---

## 🎯 What This Does

Predicts optimal F1 pit stop strategies with ML confidence:

```
🏆 OPTIMAL STRATEGY:
   Strategy Type: 1-stop
   Compounds: SOFT → MEDIUM
   Pit Lap: Lap 24
   Confidence: 94.0%
   Model: Enhanced Ensemble (RF+GB+AdaBoost)
```

**Accuracy:**
- ✅ **83.3%** strategy type (1-stop, 2-stop, 3-stop)
- ✅ **100%** pit lap (±2 laps)
- ✅ **79.2%** cross-validation
- ✅ **<50ms** prediction speed

---

## 🚀 Features

### 🤖 Enhanced ML Ensemble (v3.1.0)

**Three-model voting system:**
- RandomForestClassifier (150 estimators)
- GradientBoostingClassifier (150 estimators)
- AdaBoostClassifier (100 estimators)

**Training:**
- 72 real races (2023-2025)
- 12 enhanced features
- <1 second training
- No overfitting

### 🌐 Real-Time Data

- Live weather forecasts
- 2025 tire degradation model
- Practice session data
- Qualifying results
- Driver ratings (21 drivers)
- Team profiles (10 teams)

### 📊 Analytics

- 54 strategies evaluated
- Crash probability
- Safety car likelihood
- Track optimization
- Weather impact

---

## 🛠️ Usage

### Standard Usage

```bash
# Predict next race
python app.py

# Test system
python app.py --test

# Train models
python app.py --train

# Validate accuracy
python app.py --validate

# Show version
python app.py --version

# Setup wizard
python app.py --setup
```

### 🐳 Docker Usage

```bash
# Quick start with Docker Compose
docker-compose up -d

# Run prediction
docker-compose exec f1strat python app.py

# Run tests
docker-compose exec f1strat python app.py --test
```

See [DOCKER.md](DOCKER.md) for full Docker guide

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Strategy Accuracy | **83.3%** |
| Pit Lap Accuracy | **100%** |
| Cross-Validation | 79.2% |
| Training Time | <1 second |
| Prediction Time | <50ms |

**Tested on:** Bahrain, Saudi Arabia, Australia, Azerbaijan, Miami, Monaco (2023-2025)

---

## 📚 Documentation

- [DEPENDENCIES.md](DEPENDENCIES.md) - Dependency guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start
- [DOCKER.md](DOCKER.md) - Docker deployment
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [CHANGELOG.md](CHANGELOG.md) - Version history

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Priority areas:**
- More training data (2026 season)
- Sprint race strategies
- Wet weather predictions
- Web interface
- ✅ Docker support (implemented!)

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- [FastF1](https://github.com/theOehrly/Fast-F1) - F1 data API
- [scikit-learn](https://scikit-learn.org/) - ML framework
- [OpenWeatherMap](https://openweathermap.org/) - Weather API

---

**Made with ❤️ for F1 fans**

*Last updated: November 2, 2025*
