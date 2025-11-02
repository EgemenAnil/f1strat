# Archive Folder

This folder contains the **previous version (v1.x)** of the F1 Strategy Analysis project.

## Archived Files

### `analysis.ipynb`
- **Original Jupyter notebook** with 30 sections
- Educational F1 strategy analysis
- Historical race simulation
- Feature engineering examples
- ML model training (Linear Regression)

### `get_data.py`
- **Original data fetcher** script
- FastF1 data acquisition
- Manual race selection
- CSV export functionality

### `run_simulation.py`
- **Standalone simulation** script
- Runs complete pipeline without Jupyter
- Historical race analysis
- Strategy optimization

## Why Archived?

These files have been replaced by the new **v2.0 production system**:

- ✅ **New System**: `predict_upcoming_race.py` - Professional prediction pipeline
- ✅ **New Structure**: Modular `src/` package with separated concerns
- ✅ **New Features**: Weather API, crash prediction, traffic modeling
- ✅ **New Approach**: Predictive (future races) vs Analytical (past races)

## Can I Still Use These?

**Yes!** These files are fully functional for:
- Educational purposes
- Historical race analysis
- Learning F1 strategy concepts
- Understanding the evolution of the project

### To use old notebook:
```bash
jupyter notebook archive/analysis.ipynb
```

### To use old data fetcher:
```bash
python archive/get_data.py
```

### To use old simulation:
```bash
python archive/run_simulation.py
```

## Differences: v1.x vs v2.0

| Feature | v1.x (Archived) | v2.0 (Current) |
|---------|-----------------|----------------|
| **Focus** | Historical analysis | Future prediction |
| **Structure** | Monolithic notebook | Modular package |
| **Weather** | Static historical data | Real-time API |
| **ML Models** | Linear Regression | XGBoost + Neural Networks |
| **Strategy** | Manual optimization | Automatic optimization |
| **Crashes** | Not modeled | Probability prediction |
| **Interface** | Jupyter notebook | CLI + Python API |

---

**For current usage, see main README.md in project root.**
