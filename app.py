#!/usr/bin/env python3
"""
🏎️ F1 Race Prediction System - Main Application
Single-file launcher for easy usage

Usage:
    python app.py                  # Predict next race
    python app.py --test           # Run system tests
    python app.py --setup          # First-time setup wizard
    python app.py --help           # Show help
"""

import sys
import os
import argparse
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print application banner."""
    print(f"""
{Colors.CYAN}{'='*80}
🏎️  F1 RACE PREDICTION SYSTEM v2.0
{'='*80}{Colors.ENDC}
""")

def check_setup():
    """Check if system is properly set up."""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
    
    # Check .env file
    env_file = Path('.env')
    if not env_file.exists():
        issues.append(".env file not found (copy from .env.example)")
    else:
        # Check if API key is set
        with open(env_file) as f:
            content = f.read()
            if 'your_api_key_here' in content or 'OPENWEATHER_API_KEY=' not in content:
                issues.append("OpenWeatherMap API key not configured in .env")
    
    # Check required packages
    try:
        import pandas
        import numpy
        import fastf1
        import sklearn
    except ImportError as e:
        issues.append(f"Missing package: {str(e).split('No module named ')[-1]}")
    
    return issues

def run_setup_wizard():
    """Interactive setup wizard."""
    print(f"{Colors.BOLD}🔧 Setup Wizard{Colors.ENDC}\n")
    
    print("Step 1: Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"{Colors.GREEN}✓ Python {sys.version.split()[0]} detected{Colors.ENDC}")
    else:
        print(f"{Colors.RED}✗ Python 3.8+ required{Colors.ENDC}")
        return False
    
    print("\nStep 2: Installing dependencies...")
    print("Run: pip install -r requirements.txt")
    response = input(f"\n{Colors.YELLOW}Install now? (y/n): {Colors.ENDC}")
    if response.lower() == 'y':
        os.system("pip install -r requirements.txt --quiet")
        print(f"{Colors.GREEN}✓ Dependencies installed{Colors.ENDC}")
    
    print("\nStep 3: Setting up environment...")
    env_path = Path('.env')
    
    # Create .env if doesn't exist
    if not env_path.exists():
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print(f"{Colors.GREEN}✓ Created .env file{Colors.ENDC}")
        else:
            print(f"{Colors.RED}✗ .env.example not found{Colors.ENDC}")
            return False
    else:
        print(f"{Colors.GREEN}✓ .env file exists{Colors.ENDC}")
    
    # Interactive API key setup
    print(f"\n{Colors.BOLD}Step 4: OpenWeatherMap API Key{Colors.ENDC}")
    print("Weather forecasts require a free API key from OpenWeatherMap")
    print(f"{Colors.CYAN}Get your free key: https://openweathermap.org/api{Colors.ENDC}")
    
    # Check if API key already set
    with open(env_path) as f:
        env_content = f.read()
    
    if 'your_api_key_here' in env_content:
        print(f"\n{Colors.YELLOW}Current: API key not set{Colors.ENDC}")
        api_key = input(f"\nEnter your API key (or press Enter to skip): {Colors.ENDC}").strip()
        
        if api_key:
            # Update .env file
            env_content = env_content.replace('OPENWEATHER_API_KEY=your_api_key_here', 
                                             f'OPENWEATHER_API_KEY={api_key}')
            with open(env_path, 'w') as f:
                f.write(env_content)
            print(f"{Colors.GREEN}✓ API key saved to .env{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  Skipped - You can add it later by editing .env file{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}✓ API key already configured{Colors.ENDC}")
        update = input(f"\n{Colors.YELLOW}Update API key? (y/n): {Colors.ENDC}")
        if update.lower() == 'y':
            api_key = input(f"Enter new API key: {Colors.ENDC}").strip()
            if api_key:
                # Find and replace existing API key
                import re
                env_content = re.sub(r'OPENWEATHER_API_KEY=.*', 
                                    f'OPENWEATHER_API_KEY={api_key}', 
                                    env_content)
                with open(env_path, 'w') as f:
                    f.write(env_content)
                print(f"{Colors.GREEN}✓ API key updated{Colors.ENDC}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Setup complete!{Colors.ENDC}")
    print(f"\nNext steps:")
    print(f"1. Run: python app.py --test  {Colors.CYAN}(recommended){Colors.ENDC}")
    print(f"2. Run: python app.py         {Colors.CYAN}(predict next race){Colors.ENDC}")
    
    return True

def run_tests():
    """Run system tests."""
    print(f"{Colors.BOLD}🧪 Running System Tests{Colors.ENDC}\n")
    
    # Check setup first
    issues = check_setup()
    if issues:
        print(f"{Colors.YELLOW}⚠️  Setup issues found:{Colors.ENDC}")
        for issue in issues:
            print(f"   • {issue}")
        print(f"\n{Colors.CYAN}Run: python app.py --setup{Colors.ENDC}")
        return False
    
    try:
        # Import test module
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        print("Testing imports...")
        from src.features.engineering import F1FeatureEngineer
        from src.features.track_features import TrackFeatures
        from src.models.strategy_optimizer import StrategyOptimizer
        from src.models.crash_predictor import CrashPredictor
        print(f"{Colors.GREEN}✓ All modules imported successfully{Colors.ENDC}\n")
        
        print("Testing track features...")
        bahrain = TrackFeatures.get_track_info('Bahrain')
        print(f"{Colors.GREEN}✓ Track database working{Colors.ENDC}")
        
        print("Testing crash predictor...")
        predictor = CrashPredictor()
        risk = predictor.analyze_track_risk('Monaco')
        print(f"{Colors.GREEN}✓ Crash predictor working{Colors.ENDC}")
        
        print("Testing strategy optimizer...")
        optimizer = StrategyOptimizer(total_laps=57)
        strategies = optimizer.generate_strategies({'temperature': 25, 'rain_probability': 0.2})
        print(f"{Colors.GREEN}✓ Strategy optimizer working ({len(strategies)} strategies){Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED{Colors.ENDC}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Test failed: {e}{Colors.ENDC}")
        return False

def run_prediction():
    """Run race prediction."""
    print(f"{Colors.BOLD}🔮 Running Race Prediction{Colors.ENDC}\n")
    
    # Check if API key is missing
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file) as f:
            content = f.read()
            if 'your_api_key_here' in content:
                print(f"{Colors.YELLOW}⚠️  OpenWeatherMap API key not configured{Colors.ENDC}")
                print(f"Weather forecasts will use historical data instead of real-time forecasts.\n")
                
                response = input(f"{Colors.CYAN}Would you like to add your API key now? (y/n): {Colors.ENDC}").strip().lower()
                
                if response == 'y':
                    print(f"\n{Colors.CYAN}Get your free API key: https://openweathermap.org/api{Colors.ENDC}")
                    api_key = input(f"Enter your API key: {Colors.ENDC}").strip()
                    
                    if api_key:
                        # Update .env file
                        content = content.replace('OPENWEATHER_API_KEY=your_api_key_here', 
                                                 f'OPENWEATHER_API_KEY={api_key}')
                        with open(env_file, 'w') as f:
                            f.write(content)
                        print(f"{Colors.GREEN}✓ API key saved!{Colors.ENDC}\n")
                    else:
                        print(f"{Colors.YELLOW}Skipped - continuing with historical data{Colors.ENDC}\n")
                else:
                    print(f"{Colors.YELLOW}Continuing with historical data...{Colors.ENDC}\n")
    
    # Check other setup issues
    issues = check_setup()
    
    # Filter out API key warning (we already handled it)
    critical_issues = [i for i in issues if 'API key' not in i]
    
    if critical_issues:
        print(f"{Colors.YELLOW}⚠️  Setup incomplete:{Colors.ENDC}")
        for issue in critical_issues:
            print(f"   • {issue}")
        print(f"\n{Colors.CYAN}Run: python app.py --setup{Colors.ENDC}")
        return False
    
    try:
        # Import and run prediction
        from predict_upcoming_race import F1RacePredictionPipeline
        
        pipeline = F1RacePredictionPipeline()
        prediction = pipeline.predict_upcoming_race()
        
        if prediction:
            pipeline.print_prediction(prediction)
            
            # Save to file
            race_name = prediction['race_info']['race_name'].replace(' ', '_')
            output_file = f"prediction_{race_name}.json"
            
            import json
            with open(output_file, 'w') as f:
                json_prediction = {
                    k: v for k, v in prediction.items()
                    if k not in ['optimal_strategies']
                }
                json_prediction['strategies'] = {
                    level: {
                        'name': strat.name,
                        'compounds': strat.compounds,
                        'pit_laps': strat.pit_laps,
                        'expected_time': strat.expected_time
                    }
                    for level, strat in prediction['optimal_strategies'].items()
                }
                json.dump(json_prediction, f, indent=2)
            
            print(f"\n{Colors.GREEN}💾 Prediction saved to: {output_file}{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.YELLOW}⚠️  No upcoming race found{Colors.ENDC}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}✗ Prediction failed: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        return False

def show_help():
    """Show help message."""
    print(f"""
{Colors.BOLD}F1 Race Prediction System - Help{Colors.ENDC}

{Colors.CYAN}USAGE:{Colors.ENDC}
    python app.py              Predict next F1 race (default)
    python app.py --test       Run system tests
    python app.py --setup      Run setup wizard
    python app.py --help       Show this help

{Colors.CYAN}EXAMPLES:{Colors.ENDC}
    # First time setup
    python app.py --setup
    
    # Test installation
    python app.py --test
    
    # Predict next race
    python app.py

{Colors.CYAN}REQUIREMENTS:{Colors.ENDC}
    • Python 3.8+
    • OpenWeatherMap API key (free)
    • Internet connection

{Colors.CYAN}SETUP STEPS:{Colors.ENDC}
    1. Run setup wizard:      python app.py --setup
    2. Get API key:           https://openweathermap.org/api
    3. Edit .env file:        Add your API key
    4. Test system:           python app.py --test
    5. Run prediction:        python app.py

{Colors.CYAN}FILES:{Colors.ENDC}
    README.md          Full documentation
    QUICKSTART.md      Quick start guide
    FILE_GUIDE.md      File organization
    
{Colors.CYAN}TROUBLESHOOTING:{Colors.ENDC}
    If prediction fails:
    1. Check .env file has API key
    2. Run: python app.py --test
    3. Check internet connection
    4. See README.md for details

{Colors.CYAN}MORE INFO:{Colors.ENDC}
    GitHub: https://github.com/EgemenAnil/f1strat
    Docs:   See README.md
""")

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='F1 Race Prediction System',
        add_help=False
    )
    parser.add_argument('--setup', action='store_true', help='Run setup wizard')
    parser.add_argument('--test', action='store_true', help='Run system tests')
    parser.add_argument('--help', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.help:
        show_help()
    elif args.setup:
        run_setup_wizard()
    elif args.test:
        run_tests()
    else:
        # Check if first time setup is needed
        issues = check_setup()
        
        if issues:
            print(f"{Colors.YELLOW}⚠️  Setup incomplete:{Colors.ENDC}")
            for issue in issues:
                print(f"   • {issue}")
            
            print(f"\n{Colors.BOLD}Running setup wizard...{Colors.ENDC}\n")
            
            # Auto-run setup wizard
            if run_setup_wizard():
                print(f"\n{Colors.CYAN}Setup complete! Run 'python app.py' again to predict.{Colors.ENDC}")
            else:
                print(f"\n{Colors.RED}Setup failed. Please run 'python app.py --setup' manually.{Colors.ENDC}")
        else:
            # Setup OK, run prediction
            run_prediction()

if __name__ == "__main__":
    main()
