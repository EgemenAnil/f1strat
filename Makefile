# Makefile for F1 Strategy Prediction System v3.1.0

.PHONY: help install test train validate run docker-build docker-up docker-down clean

# Default target
help:
	@echo "F1 Strategy Prediction System v3.1.0"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make train         - Train ML models"
	@echo "  make validate      - Validate ML accuracy"
	@echo "  make run           - Run prediction"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker container"
	@echo "  make docker-down   - Stop Docker container"
	@echo "  make clean         - Clean cache and temp files"

# Install dependencies
install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Run tests
test:
	python app.py --test
	pytest tests/ -v

# Train models
train:
	python app.py --train

# Validate models
validate:
	python app.py --validate

# Run prediction
run:
	python app.py

# Docker build
docker-build:
	docker build -t f1strat:v3.1.0 .

# Docker up
docker-up:
	docker-compose up -d

# Docker down
docker-down:
	docker-compose down

# Clean cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ 2>/dev/null || true
	@echo "✅ Cleaned cache and temp files"

# Development setup
dev-setup:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 isort
	@echo "✅ Development environment ready"

# Format code
format:
	black src/ tests/
	isort src/ tests/
	@echo "✅ Code formatted"

# Lint code
lint:
	flake8 src/ tests/ --max-line-length=100
	@echo "✅ Code linted"

# Full CI pipeline (local)
ci: clean format lint test
	@echo "✅ CI pipeline completed"
