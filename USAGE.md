# 🎯 ONE-FILE USER GUIDE

**The simplest way to use F1 Race Prediction System**

---

## For Absolute Beginners

### Step 1: First Time Setup
```bash
python app.py --setup
```

Follow the wizard. It will:
- ✅ Check your Python version
- ✅ Install required packages
- ✅ Create configuration file
- ✅ Tell you where to get API key

### Step 2: Get API Key
1. Go to: https://openweathermap.org/api
2. Sign up (it's free!)
3. Copy your API key
4. Open `.env` file
5. Paste your key after `OPENWEATHER_API_KEY=`

### Step 3: Test
```bash
python app.py --test
```

Should see:
```
✓ All modules imported successfully
✓ Track database working
✓ Crash predictor working
✓ Strategy optimizer working
✓ ALL TESTS PASSED
```

### Step 4: Predict!
```bash
python app.py
```

Done! 🎉

---

## All You Need to Know

### Main Command (99% of the time)
```bash
python app.py
```

### Other Commands (rarely needed)
```bash
python app.py --setup    # First time only
python app.py --test     # If something breaks
python app.py --help     # Forgot the commands
```

---

## What It Does

When you run `python app.py`, it:

1. 🔍 Finds the next F1 race automatically
2. 🌤️ Gets weather forecast for race day
3. 🏁 Analyzes the track (Monaco vs Monza = different!)
4. 📊 Calculates crash probability
5. 🎯 Finds optimal pit stop strategy
6. 💾 Saves everything to a file

### Example Output:
```
📍 Belgian Grand Prix - Spa-Francorchamps
🌤 Temperature: 18°C, Rain: 65%
⚠️  Safety Car Probability: 50%
🏁 BEST STRATEGY: 1-Stop
   - Start on MEDIUM tires
   - Pit on lap 18
   - Switch to SOFT tires
   - ⚠️ Keep INTERMEDIATES ready for rain!
💾 Saved to: prediction_Belgian_Grand_Prix.json
```

---

## Troubleshooting

### "No module named..."
```bash
python app.py --setup
```
Then type `y` when asked to install packages.

### "API key not found"
Did you:
1. Get API key from openweathermap.org? ✓
2. Paste it in `.env` file? ✓
3. Save the file? ✓

### "No upcoming race found"
- Season might have ended
- Check F1 calendar
- System looks ahead 1 year

### Still not working?
```bash
python app.py --help
```

---

## Files You Should Know

| File | What It Is |
|------|------------|
| **`app.py`** | **The main app - this is all you need** |
| `.env` | Your API key (edit this once) |
| `QUICKSTART.md` | If you want more details |
| `README.md` | If you want ALL the details |

---

## Advanced Stuff (Optional)

### Want to customize?
Edit files in `config/` folder:
- `model_config.yaml` - ML settings
- `simulation_config.yaml` - Race simulation settings

### Want to understand the code?
- `src/data/` - How data is fetched
- `src/features/` - How features are created
- `src/models/` - The AI models

### Want the old version?
Check `archive/` folder - has educational Jupyter notebook

---

## FAQ

**Q: Do I need to code?**
A: No! Just run `python app.py`

**Q: Is it free?**
A: Yes! API is free too (up to 1000 calls/day)

**Q: Which races can it predict?**
A: Any upcoming F1 race (auto-detected)

**Q: Does it work offline?**
A: No, needs internet for weather data

**Q: Can I predict past races?**
A: Use the old notebook in `archive/` for that

**Q: How accurate is it?**
A: It's a prediction tool, not a crystal ball! 
   Weather changes, crashes happen, life is unpredictable.
   But it gives you data-driven strategy insights!

**Q: Can I customize strategies?**
A: Yes! Edit `config/simulation_config.yaml`

**Q: Where's the output saved?**
A: `prediction_[RACE_NAME].json` in current folder

---

## One More Time (TL;DR)

```bash
# First time
python app.py --setup
# Edit .env, add API key

# Every race weekend
python app.py
```

**That's literally it.** 🏎️💨

---

Need help? Check:
1. `python app.py --help`
2. `QUICKSTART.md`
3. `README.md`
