import pandas as pd
from datetime import datetime
import os

team_df = pd.read_csv("../csv/Team.csv")
attributes_df = pd.read_csv("../csv/Team_Attributes.csv")

attributes_df['date'] = pd.to_datetime(attributes_df['date'])
latest_attributes = attributes_df.sort_values('date').groupby('team_api_id').last().reset_index()

merged_df = pd.merge(team_df, latest_attributes, on=['team_api_id', 'team_fifa_api_id'], how='left')

logo_base_url = "https://example.com/logos/"
merged_df["logo"] = logo_base_url + merged_df["team_api_id"].astype(str) + ".png"

final_df = merged_df[["team_api_id", "team_long_name", "team_short_name", "logo", 
                       "buildUpPlaySpeedClass", "buildUpPlayDribblingClass", "buildUpPlayPassingClass", "date"]]
final_df.columns = ["id", "name", "abbrev", "logo", "build_up_play_speed", "build_up_play_dribble", "build_up_play_passing", "creation_date"]

speed_map = {"Balanced": "Balanced", "Fast": "Fast", "Slow": "Slow"}
dribble_map = {"Lots": "Lots", "Little": "Little", "Normal": "Normal"}
passing_map = {"Mixed": "Mixed", "Short": "Short", "Long": "Long"}

final_df["build_up_play_speed"] = final_df["build_up_play_speed"].map(speed_map)
final_df["build_up_play_dribble"] = final_df["build_up_play_dribble"].map(dribble_map)
final_df["build_up_play_passing"] = final_df["build_up_play_passing"].map(passing_map)

output_dir = "../csvNew"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "Formatted_Team.csv")
final_df.to_csv(output_path, index=False)

print(f"File saved as {output_path}")
