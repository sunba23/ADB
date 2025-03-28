import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

def get_team_locations():
    match_df = pd.read_csv('../csv/Match.csv')
    team_df = pd.read_csv('../csv/Team.csv')

    home_team_ids = match_df['home_team_api_id'].unique()
    teams = team_df[team_df['team_api_id'].isin(home_team_ids)]

    geolocator = Nominatim(user_agent="football_team_locator")
    team_locations = {}

    for _, row in teams.iterrows():
        team_name = row['team_long_name']
        try:
            location = geolocator.geocode(team_name, timeout=10)
            if location:
                team_locations[row['team_api_id']] = (team_name, location.latitude, location.longitude)
            else:
                team_locations[row['team_api_id']] = (team_name, None, None)
        except Exception as e:
            print(f"Geocoding error {team_name}: {e}")
            team_locations[row['team_api_id']] = (team_name, None, None)

    return team_locations

def get_weather_data(lat, lon, date):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone=UTC"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "daily" in data:
                temp_max = data["daily"]["temperature_2m_max"][0]
                temp_min = data["daily"]["temperature_2m_min"][0]
                wind_speed = data["daily"]["wind_speed_10m_max"][0]
                precipitation = data["daily"]["precipitation_sum"][0]
                conditions = "Rainy" if precipitation > 0 else "Clear"
                return (temp_max + temp_min) / 2, None, wind_speed, conditions
        except Exception as e:
            print(f"Error downloading weather for ({lat}, {lon}) on {date}, attempt {attempt+1}: {e}")
            time.sleep(2) 
    return None, None, None, None

def fetch_weather_for_teams():
    team_locations = get_team_locations()
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2016, 12, 31)

    weather_data = []

    for team_id, (team_name, lat, lon) in team_locations.items():
        if lat is None or lon is None:
            print(f"No coordinates for {team_name}")
            continue

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            temp, humidity, wind_speed, conditions = get_weather_data(lat, lon, date_str)

            weather_data.append([team_id, date_str, temp, humidity, wind_speed, conditions])
            current_date += timedelta(days=1)

    return weather_data

def save_to_csv(data, filename="../csvNew/Weather.csv"):
    df = pd.DataFrame(data, columns=["team_id", "date", "temperature", "humidity", "wind_speed", "conditions"])
    df.to_csv(filename, index=False)
    print(f"Data saved in {filename}")

if __name__ == "__main__":
    weather_data = fetch_weather_for_teams()
    save_to_csv(weather_data)
