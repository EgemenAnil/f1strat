# Contributing to F1 Strategy Prediction System# Contributing to F1 Race Prediction System



Thank you for your interest in contributing to the F1 Strategy Prediction System! 🏎️First off, thank you for considering contributing! 🏎️



This document provides guidelines for contributing to the project.## How to Contribute



---### Reporting Bugs



## 🎯 How Can You Contribute?If you find a bug, please open an issue with:

- Clear description of the problem

### 1. Report Bugs 🐛- Steps to reproduce

- Expected vs actual behavior

Found a bug? Please create an issue with:- Your environment (OS, Python version)

- Error messages/logs

- **Clear title** describing the bug

- **Steps to reproduce** the issue### Suggesting Features

- **Expected behavior** vs **actual behavior**

- **Environment details** (OS, Python version, etc.)Feature requests are welcome! Please include:

- **Error messages** or screenshots- Clear use case

- Why it would be useful

**Template:**- How it might work

```markdown

**Bug Description:**### Code Contributions

Brief description of the bug

1. **Fork the repository**

**Steps to Reproduce:**2. **Create a branch**: `git checkout -b feature/your-feature-name`

1. Run `python app.py`3. **Make your changes**

2. ...4. **Test thoroughly**: `python app.py --test`

5. **Commit**: Use clear commit messages

**Expected Behavior:**6. **Push**: `git push origin feature/your-feature-name`

What should happen7. **Pull Request**: Open a PR with description



**Actual Behavior:**## Development Setup

What actually happens

```bash

**Environment:**# Clone your fork

- OS: macOS 14.0git clone https://github.com/YOUR_USERNAME/f1strat.git

- Python: 3.14.0cd f1strat

- Version: v3.1.0

# Create virtual environment

**Error Log:**python -m venv f1-env

```source f1-env/bin/activate

[paste error here]

```# Install dependencies

```pip install -r requirements.txt



### 2. Suggest Features 💡# Setup environment

python app.py --setup

Have an idea? Create a feature request with:

# Run tests

- **Feature description** - What you wantpython app.py --test

- **Use case** - Why it's useful```

- **Implementation ideas** (optional)

- **Examples** from other projects (optional)## Code Style



### 3. Improve Documentation 📝- Follow PEP 8

- Use type hints where possible

Documentation improvements are always welcome:- Add docstrings to functions/classes

- Keep functions focused and small

- Fix typos or unclear sections- Write descriptive variable names

- Add examples or tutorials

- Translate to other languages## Testing

- Improve code comments

Before submitting:

### 4. Submit Code 💻```bash

# Run all tests

See "Development Workflow" below.python app.py --test



---# Test specific components

python run_tests.py

## 🛠️ Development Setup

# Manual test

### 1. Fork & Clonepython app.py

```

```bash

# Fork the repository on GitHub## Project Structure

# Then clone your fork

git clone https://github.com/YOUR_USERNAME/f1strat.git```

cd f1stratsrc/

```├── data/       # Data fetching and processing

├── features/   # Feature engineering

### 2. Set Up Environment├── models/     # ML models and optimization

└── simulation/ # Race simulation (future)

```bash```

# Create virtual environment

python -m venv f1-env## What We're Looking For



# Activate it### High Priority

source f1-env/bin/activate  # macOS/Linux- 🐛 Bug fixes

# or- 📚 Documentation improvements

f1-env\Scripts\activate     # Windows- ✅ Test coverage

- 🎨 UI/UX improvements

# Install dependencies

pip install -r requirements.txt### Medium Priority

- ⚡ Performance optimizations

# Install development dependencies- 🆕 New track data

pip install pytest pytest-cov black flake8- 🌍 Internationalization

```- 📊 Additional visualizations



### 3. Create Branch### Nice to Have

- 🧪 New ML models

```bash- 🎯 Advanced features

# Create feature branch- 🔌 API integrations

git checkout -b feature/your-feature-name- 📱 Mobile support



# or for bug fixes## Areas That Need Help

git checkout -b fix/bug-description

```1. **Testing**: More comprehensive test coverage

2. **Documentation**: Examples, tutorials, use cases

### 4. Make Changes3. **Features**: Driver/team performance modeling

4. **UI**: Streamlit dashboard, FastAPI endpoints

- Follow the coding style (see below)5. **Data**: More historical race data

- Add tests for new features6. **Accuracy**: Model improvements with more training data

- Update documentation

- Test your changes## Questions?



### 5. Run Tests- Open an issue with the `question` label

- Check existing issues and discussions

```bash- See README.md for detailed documentation

# Run system tests

python app.py --test## Code of Conduct



# Run validation- Be respectful and inclusive

python app.py --validate- Provide constructive feedback

- Focus on the code, not the person

# Run specific test- Help others learn and grow

python test_system_v3_1.py

```## Recognition



### 6. Commit ChangesContributors will be:

- Listed in README.md

```bash- Credited in release notes

# Stage changes- Thanked in commit messages

git add .

Thank you for making F1 strategy analysis better! 🏁

# Commit with clear message
git commit -m "feat: add new feature X"
# or
git commit -m "fix: resolve issue #123"
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

### 7. Push & Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Fill in the PR template
```

---

## 📏 Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

```python
# Good ✅
def predict_strategy(race_data: dict, weather: dict) -> dict:
    """
    Predict optimal race strategy.
    
    Args:
        race_data: Dictionary containing race information
        weather: Dictionary containing weather data
    
    Returns:
        Dictionary with strategy prediction
    """
    # Use descriptive variable names
    optimal_strategy = calculate_optimal_pit_stops(race_data)
    
    # Add type hints
    confidence: float = model.predict_proba(features)
    
    return {
        'strategy': optimal_strategy,
        'confidence': confidence
    }

# Bad ❌
def ps(d, w):
    s = calc(d)
    c = m.p(f)
    return {'s': s, 'c': c}
```

### Code Organization

```python
# 1. Imports (grouped and sorted)
import os
import sys
from typing import Dict, List

import numpy as np
import pandas as pd

from src.models.strategy_optimizer import StrategyOptimizer

# 2. Constants
DEFAULT_PIT_STOP_TIME = 24.0
MAX_STRATEGIES = 100

# 3. Classes
class StrategyPredictor:
    """Strategy prediction class."""
    pass

# 4. Functions
def main():
    """Main entry point."""
    pass
```

### Documentation

```python
def predict_pit_lap(
    race_data: dict,
    tire_compound: str,
    weather_temp: float
) -> int:
    """
    Predict optimal pit stop lap.
    
    Uses ML ensemble (RF + GB + AdaBoost) to predict the best lap
    to pit based on race conditions and tire degradation.
    
    Args:
        race_data: Dictionary containing:
            - track_name (str): Circuit name
            - total_laps (int): Race distance
            - starting_compound (str): Starting tire
        tire_compound: Target compound (SOFT, MEDIUM, HARD)
        weather_temp: Track temperature in Celsius
    
    Returns:
        Predicted pit lap number (1-indexed)
    
    Raises:
        ValueError: If tire_compound is invalid
    
    Example:
        >>> predict_pit_lap(
        ...     {'track_name': 'Monaco', 'total_laps': 78},
        ...     'MEDIUM',
        ...     25.5
        ... )
        42
    """
    pass
```

### Testing

```python
import pytest

def test_strategy_prediction():
    """Test strategy prediction accuracy."""
    # Arrange
    race_data = {
        'track_name': 'Bahrain',
        'total_laps': 57
    }
    
    # Act
    result = predict_strategy(race_data)
    
    # Assert
    assert result['strategy_type'] in ['1-stop', '2-stop', '3-stop']
    assert 0 <= result['confidence'] <= 1
    assert len(result['pit_laps']) > 0
```

---

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority ⭐⭐⭐

1. **More Training Data**
   - Add 2024 race results
   - Add 2026 races as they complete
   - Improve model accuracy

2. **Sprint Race Support**
   - Implement sprint-specific strategies
   - Shorter race predictions
   - Different tire allocations

3. **Wet Weather Predictions**
   - Rain probability integration
   - Intermediate/Wet tire strategies
   - Dynamic strategy changes

### Medium Priority ⭐⭐

4. **Web Interface**
   - Flask/FastAPI backend
   - React/Vue frontend
   - Real-time predictions

5. **Docker Support**
   - Dockerfile creation
   - Docker Compose setup
   - Easy deployment

6. **CI/CD Pipeline**
   - GitHub Actions workflow
   - Automated testing
   - Code quality checks

### Low Priority ⭐

7. **Additional Features**
   - Historical race analysis
   - Driver comparison tools
   - Team performance analytics

---

## 🔍 Code Review Process

All contributions go through code review:

1. **Automated Checks**
   - Tests must pass
   - Code style must comply
   - No merge conflicts

2. **Manual Review**
   - Code quality
   - Documentation
   - Test coverage
   - Performance impact

3. **Feedback**
   - We'll provide constructive feedback
   - Address comments
   - Iterate if needed

4. **Merge**
   - Approved PRs are merged
   - Contributions credited in changelog

---

## 📋 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All tests pass (`python app.py --test`)
- [ ] Added tests for new features
- [ ] Validated ML accuracy (`python app.py --validate`)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Changelog updated

## Related Issues
Fixes #123
Related to #456
```

---

## 🎓 Learning Resources

New to F1 data analysis? Check these out:

- **FastF1 Docs:** https://docs.fastf1.dev/
- **scikit-learn Guide:** https://scikit-learn.org/stable/user_guide.html
- **F1 Technical:** https://www.formula1.com/en/latest/article.what-is-an-f1-pit-stop.html
- **Tire Strategy:** https://www.pirelli.com/global/en-ww/motorsport/f1

---

## 💬 Communication

- **Questions:** Open a [Discussion](https://github.com/EgemenAnil/f1strat/discussions)
- **Bugs:** Create an [Issue](https://github.com/EgemenAnil/f1strat/issues)
- **Ideas:** Start a [Discussion](https://github.com/EgemenAnil/f1strat/discussions)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution, no matter how small, is valued and appreciated!

**Top Contributors:**
- @EgemenAnil - Creator & Maintainer
- [Your name could be here!]

---

*Happy coding! 🏎️💨*
