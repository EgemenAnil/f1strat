import fastf1
import pandas as pd
import os

# --- 1. Script'in Kendi Konumunu Bulma (En Önemli Kısım) ---
# __file__ -> bu script dosyasının yolunu verir (örn: f1strat/get_data.py)
# os.path.abspath(__file__) -> bu yolun tam, mutlak halini verir (örn: /Users/egemen/Desktop/f1strat/get_data.py)
# os.path.dirname(...) -> bir dosya yolundan, o dosyanın içinde bulunduğu klasörün yolunu çıkarır.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Artık tüm dosya yollarımızı bu 'script_dir' değişkenini referans alarak oluşturacağız.
cache_path = os.path.join(script_dir, 'cache')


# --- Kullanıcıdan Girdileri Alma (Aynı kod) ---
try:
    year_input = int(input("Please enter the year you want to fetch data for (e.g.: 2023): "))
    track_input = input("Please enter the track name (e.g.: Bahrain, Monza, Miami): ")
    print("Session Types: 'R' (Race), 'Q' (Qualifying), 'FP1', 'FP2', 'FP3'")
    session_input = input("Please enter the session type: ")
except ValueError:
    print("Error: Please enter a valid year. Program is terminating.")
    exit()

# --- FastF1 Önbellek Ayarı (Düzeltilmiş Yol ile) ---
if not os.path.exists(cache_path):
    os.makedirs(cache_path)
    print(f"Cache directory created at: {cache_path}")
fastf1.Cache.enable_cache(cache_path)


# --- Hata Yönetimi ve Dinamik Veri Çekme ---
try:
    print(f"\nLoading {year_input} {track_input} GP - '{session_input}' session data...")
    session = fastf1.get_session(year_input, track_input, session_input)
    session.load()
    laps = session.laps

    # --- Veri Temizleme ve İşleme ---
    df_laps = laps.loc[:, ['Driver', 'LapNumber', 'LapTime', 'Compound', 'Stint', 'TyreLife']]
    df_laps['LapTime'] = df_laps['LapTime'].dt.total_seconds()
    df_laps = df_laps.dropna(subset=['TyreLife', 'LapTime'])
    df_laps['TyreLife'] = df_laps['TyreLife'].astype(int)

    # --- Dinamik Dosya Adı Oluşturma ve Doğru Yola Kaydetme ---
    safe_track_name = track_input.replace(' ', '_')
    file_name = f"{year_input}_{safe_track_name}_{session_input}_laps_clean.csv"
    
    # Dosya yolunu 'script_dir' ile birleştirerek tam yolu oluşturuyoruz.
    output_path = os.path.join(script_dir, file_name)
    
    # Veriyi tam ve doğru yola kaydediyoruz.
    df_laps.to_csv(output_path, index=False)

    print(f"\nSuccess! Data has been saved to: {output_path}")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please make sure the information you entered (year, track, session type) is correct.")