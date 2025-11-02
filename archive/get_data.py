import fastf1
import pandas as pd
import os
from typing import Tuple
import datetime

def setup_paths() -> Tuple[str, str]:
    """
    Set up the necessary paths for the script.
    Returns:
        Tuple containing script directory and cache path
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(script_dir, 'cache')
    return script_dir, cache_path

def setup_cache(cache_path: str) -> None:
    """
    Set up the FastF1 cache directory
    """
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
        print(f"Cache directory created at: {cache_path}")
    fastf1.Cache.enable_cache(cache_path)


def get_user_input() -> Tuple[int, str, str]:
    """
    Get and validate user input for year, track, and session type
    Returns:
        Tuple containing year, track name, and session type
    """
    valid_sessions = ['R', 'Q', 'FP1', 'FP2', 'FP3']
    current_year = datetime.datetime.now().year
    
    try:
        year_input = int(input("Please enter the year you want to fetch data for (e.g.: 2023): "))
        if not (1950 <= year_input <= current_year):
            raise ValueError(f"Year must be between 1950 and {current_year}")
        
        track_input = input("Please enter the track name (e.g.: Bahrain, Monza, Miami): ")
        if not track_input.strip():
            raise ValueError("Track name cannot be empty")
        
        print("Session Types: 'R' (Race), 'Q' (Qualifying), 'FP1', 'FP2', 'FP3'")
        session_input = input("Please enter the session type: ").upper()
        if session_input not in valid_sessions:
            raise ValueError(f"Session type must be one of: {', '.join(valid_sessions)}")
        
        return year_input, track_input, session_input
    
    except ValueError as e:
        print(f"Error: {str(e)}")
        exit(1)


def process_session_data(year: int, track: str, session_type: str, script_dir: str) -> str:
    """
    Fetch and process F1 session data
    
    Args:
        year: Race year
        track: Track name
        session_type: Session type (R/Q/FP1/FP2/FP3)
        script_dir: Script directory path for saving output
    
    Returns:
        Path to the saved CSV file
    
    Raises:
        Exception: If there's an error in fetching or processing data
    """
    try:
        print(f"\nSearching for {year} {track} GP - '{session_type}' session...")
        session = fastf1.get_session(year, track, session_type)
        
        # Validate BEFORE loading: check if FastF1 found the correct event
        event_name = session.event.get('EventName', 'Unknown')
        event_location = session.event.get('Location', 'Unknown')
        event_country = session.event.get('Country', 'Unknown')
        
        print(f"\n⚠️ found: {event_name}")
        print(f"   Location: {event_location}, {event_country}")
        print(f"   Round: {session.event.get('RoundNumber', 'N/A')}")
        
        # Check if the found event matches user's request
        user_track_lower = track.lower().replace(' ', '')
        found_event_text = f"{event_name} {event_location} {event_country}".lower().replace(' ', '')
        
        # Simple check: is the user's track name somewhere in the event info?
        if user_track_lower not in found_event_text:
            print(f"\n❌ WARNING: The track you requested ('{track}') does not match the found event!")
            confirm = input(f"\nDo you want to continue with '{event_name}' instead? (yes/no): ").lower()
            if confirm not in ['yes', 'y']:
                print("Operation cancelled by user.")
                raise Exception("User cancelled - event mismatch")
        
        print(f"\n✅ Confirmed: Loading {event_name}...")
        session.load()
        
        # Extract and clean lap data
        df_laps = session.laps.loc[:, [
            'Driver', 'LapNumber', 'LapTime', 
            'Compound', 'Stint', 'TyreLife'
        ]]
        
        # Convert lap times to seconds and clean data
        df_laps['LapTime'] = df_laps['LapTime'].dt.total_seconds()
        df_laps = df_laps.dropna(subset=['TyreLife', 'LapTime'])
        df_laps['TyreLife'] = df_laps['TyreLife'].astype(int)
        
        # Create output file path using the ACTUAL event name (not user input)
        actual_event_name = session.event.get('EventName', track).replace(' ', '_')
        file_name = f"{year}_{actual_event_name}_{session_type}_laps_clean.csv"
        output_path = os.path.join(script_dir, file_name)
        
        # Save processed data
        df_laps.to_csv(output_path, index=False)
        
        # Display success message with file info
        print(f"\n{'='*70}")
        print("✅ SUCCESS!")
        print(f"{'='*70}")
        print(f"📁 File saved: {file_name}")
        print(f"📂 Full path: {output_path}")
        print(f"📊 Total laps saved: {len(df_laps):,}")
        print(f"{'='*70}")
        print(f"\n💡 To analyze this data:")
        print(f"   1. Open 'analysis.ipynb'")
        print(f"   2. Run the cells and select: {file_name}")
        print(f"{'='*70}\n")
        
        return output_path
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please make sure the information you entered (year, track, session type) is correct.")
        raise

def main():
    """
    Main execution function
    """
    try:
        # Setup
        script_dir, cache_path = setup_paths()
        setup_cache(cache_path)
        
        # Get user input
        year, track, session_type = get_user_input()
        
        # Process data
        process_session_data(year, track, session_type, script_dir)
        
    except Exception as e:
        print(f"\nProgram terminated due to an error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()