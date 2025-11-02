# 🐳 Docker Deployment Guide

Quick guide to run F1 Strategy Prediction System in Docker.

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 2: Docker CLI

```bash
# Build image
docker build -t f1strat:v3.1.0 .

# Run container
docker run -it --rm \
  -v $(pwd)/cache:/app/cache \
  -v $(pwd)/models:/app/models \
  -e OPENWEATHER_API_KEY=your_key_here \
  f1strat:v3.1.0

# Run with specific command
docker run -it --rm f1strat:v3.1.0 python app.py --test
```

---

## 📋 Container Commands

```bash
# Test system
docker-compose exec f1strat python app.py --test

# Train models
docker-compose exec f1strat python app.py --train

# Validate models
docker-compose exec f1strat python app.py --validate

# Run prediction
docker-compose exec f1strat python app.py

# Shell access
docker-compose exec f1strat /bin/bash
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
OPENWEATHER_API_KEY=your_api_key_here
```

Or pass directly:

```bash
docker run -e OPENWEATHER_API_KEY=abc123 f1strat:v3.1.0
```

### Volumes

**Persistent data:**
- `./cache` - FastF1 cache (auto-created)
- `./models` - Trained ML models
- `./config` - Configuration files

**Example:**
```bash
docker run -v ./models:/app/models f1strat:v3.1.0
```

---

## 📊 Resource Limits

Default limits (adjust in `docker-compose.yml`):

```yaml
resources:
  limits:
    cpus: '2.0'      # 2 CPU cores max
    memory: 2G       # 2GB RAM max
  reservations:
    cpus: '1.0'      # 1 CPU core minimum
    memory: 1G       # 1GB RAM minimum
```

---

## 🔍 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Check container status
docker-compose ps
```

### Out of memory

Increase memory limit in `docker-compose.yml`:
```yaml
memory: 4G  # Increase to 4GB
```

### Permission errors

```bash
# Fix permissions
chmod -R 755 cache/ models/
```

### Models not persisting

Ensure volume is mounted:
```bash
docker-compose down
docker-compose up -d
```

---

## 🧪 Testing in Docker

```bash
# Run all tests
docker-compose exec f1strat pytest tests/ -v

# Run specific test
docker-compose exec f1strat pytest tests/test_ml_models.py -v

# With coverage
docker-compose exec f1strat pytest tests/ --cov=src
```

---

## 🏗️ Building

### Development Build

```bash
docker build -t f1strat:dev .
```

### Production Build

```bash
docker build -t f1strat:v3.1.0 --no-cache .
```

### Multi-platform Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t f1strat:v3.1.0 .
```

---

## 📦 Image Size

**Optimizations:**
- Base image: `python:3.11-slim` (~150MB)
- Dependencies: ~800MB
- **Total:** ~950MB

**To reduce size:**
1. Use Alpine Linux (not recommended - compilation issues)
2. Multi-stage build (for production)
3. Remove dev dependencies

---

## 🚢 Deployment

### Push to Docker Hub

```bash
docker tag f1strat:v3.1.0 yourusername/f1strat:v3.1.0
docker push yourusername/f1strat:v3.1.0
```

### Pull and Run

```bash
docker pull yourusername/f1strat:v3.1.0
docker run -it yourusername/f1strat:v3.1.0
```

---

## 🔐 Security

**Best practices:**
- Don't include API keys in image
- Use `.env` file for secrets
- Run as non-root user (TODO)
- Scan for vulnerabilities:

```bash
docker scan f1strat:v3.1.0
```

---

## 📝 Notes

- First run takes longer (downloads F1 data)
- Cache persists between runs
- Models trained once, reused
- Internet required for FastF1 API

---

**Questions?** See [README.md](../README.md) or [CONTRIBUTING.md](../CONTRIBUTING.md)
