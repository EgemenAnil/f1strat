# Contributing to F1 Race Prediction System

First off, thank you for considering contributing! 🏎️

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Error messages/logs

### Suggesting Features

Feature requests are welcome! Please include:
- Clear use case
- Why it would be useful
- How it might work

### Code Contributions

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**: `python app.py --test`
5. **Commit**: Use clear commit messages
6. **Push**: `git push origin feature/your-feature-name`
7. **Pull Request**: Open a PR with description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/f1strat.git
cd f1strat

# Create virtual environment
python -m venv f1-env
source f1-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
python app.py --setup

# Run tests
python app.py --test
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions/classes
- Keep functions focused and small
- Write descriptive variable names

## Testing

Before submitting:
```bash
# Run all tests
python app.py --test

# Test specific components
python run_tests.py

# Manual test
python app.py
```

## Project Structure

```
src/
├── data/       # Data fetching and processing
├── features/   # Feature engineering
├── models/     # ML models and optimization
└── simulation/ # Race simulation (future)
```

## What We're Looking For

### High Priority
- 🐛 Bug fixes
- 📚 Documentation improvements
- ✅ Test coverage
- 🎨 UI/UX improvements

### Medium Priority
- ⚡ Performance optimizations
- 🆕 New track data
- 🌍 Internationalization
- 📊 Additional visualizations

### Nice to Have
- 🧪 New ML models
- 🎯 Advanced features
- 🔌 API integrations
- 📱 Mobile support

## Areas That Need Help

1. **Testing**: More comprehensive test coverage
2. **Documentation**: Examples, tutorials, use cases
3. **Features**: Driver/team performance modeling
4. **UI**: Streamlit dashboard, FastAPI endpoints
5. **Data**: More historical race data
6. **Accuracy**: Model improvements with more training data

## Questions?

- Open an issue with the `question` label
- Check existing issues and discussions
- See README.md for detailed documentation

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Thanked in commit messages

Thank you for making F1 strategy analysis better! 🏁
