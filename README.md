# 🏎️ F1 Strategy Analysis

A comprehensive Formula 1 race data analysis tool that fetches, processes, and visualizes race data using the FastF1 API.

## 📋 Overview

This project provides tools to:
- Fetch Formula 1 race data from any season
- Clean and process lap time data
- Analyze tire performance and degradation
- Compare driver performance
- Generate detailed statistical insights

## 🚀 Getting Started

### Prerequisites

Install required packages:
```bash
pip install -r requirements.txt
```

### Usage

#### 1. Fetch Race Data

Run the data fetcher script:
```bash
python get_data.py
```

You'll be prompted to enter:
- **Year**: Race season (e.g., 2023)
- **Track**: Circuit name (e.g., Bahrain, Monza, Miami)
- **Session**: Session type (R=Race, Q=Qualifying, FP1/FP2/FP3=Practice)

The script will:
- Download race data from FastF1
- Process and clean the data
- Save it as a CSV file (e.g., `2023_Bahrain_R_laps_clean.csv`)

#### 2. Analyze Data

Open and run `analysis.ipynb` in Jupyter:
```bash
jupyter notebook analysis.ipynb
```

**Two ways to select data file:**

**Option A - Interactive Selection:**
1. Run the "Option A" cell
2. You'll see a list of all available CSV files
3. Enter the number of the file you want to analyze
4. The analysis will run on your selected file

**Option B - Auto Selection:**
1. Run the "Option B" cell
2. The most recently created file will be automatically selected
3. Or uncomment the line and specify a file directly

The notebook includes:
- 📊 Data loading and exploration
- 🛞 Tire performance analysis
- 👨‍✈️ Driver performance comparison
- 🔥 Heatmaps and visualizations
- 📈 Statistical insights

## 📁 Project Structure

```
f1strat/
│
├── get_data.py              # Data fetching script
├── analysis.ipynb           # Analysis notebook
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
│
├── cache/                  # FastF1 cache directory
│   └── [year]/
│       └── [race]/
│
└── *.csv                   # Generated data files
```

## 📊 Analysis Features

### 1. Tire Performance Analysis
- Tire degradation curves
- Compound comparison (Soft/Medium/Hard)
- Distribution analysis
- Performance statistics

### 2. Driver Performance
- Average lap times with consistency metrics
- Best lap comparisons
- Lap count analysis
- Performance rankings

### 3. Combined Analysis
- Driver vs tire performance heatmaps
- Lap time progression
- Top performers by compound

### 4. Statistical Insights
- Correlation analysis
- Key performance indicators
- Race summary statistics

## 🛠️ Technical Details

### Data Processing Pipeline

1. **Fetch**: Download session data via FastF1 API
2. **Extract**: Select relevant columns (Driver, LapTime, Compound, etc.)
3. **Clean**: Remove invalid laps and convert time formats
4. **Save**: Export as CSV for analysis

### Key Metrics

- **Lap Time**: Race lap duration in seconds
- **Tire Life**: Number of laps on current tire set
- **Compound**: Tire type (SOFT/MEDIUM/HARD)
- **Stint**: Current tire stint number

## 📈 Visualizations

The analysis notebook generates:
- Scatter plots with trend lines
- Box plots for distribution
- Violin plots for density
- Bar charts for comparisons
- Heatmaps for multi-dimensional analysis

## 🎯 Use Cases

- **Race Strategy**: Understand optimal tire strategies
- **Driver Analysis**: Compare driver performance
- **Tire Degradation**: Study how tires wear over a race
- **Performance Prediction**: Identify performance patterns

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to:
- Add new analysis methods
- Improve visualizations
- Enhance data processing
- Add new metrics

## 📝 Notes

- Data is cached locally to improve performance
- First run may take longer while downloading data
- Ensure stable internet connection for data fetching
- Some races may have limited data availability

## 🔗 Resources

- [FastF1 Documentation](https://docs.fastf1.dev/)
- [Formula 1 Official](https://www.formula1.com/)

---

**Happy Analyzing! 🏁**
