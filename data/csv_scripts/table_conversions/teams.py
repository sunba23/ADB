import os
from datetime import datetime

import pandas as pd


class TeamsEnricher:
    def __init__(self, in_teams_file: str, in_team_attributes_file: str, out_file: str) -> None:
        self.in_teams_file = in_teams_file
        self.in_team_attributes_file = in_team_attributes_file
        self.out_file = out_file

    def run(self):
        team_df = pd.read_csv(self.in_teams_file)
        attributes_df = pd.read_csv(self.in_team_attributes_file)

        attributes_df["date"] = pd.to_datetime(attributes_df["date"])
        latest_attributes = (
            attributes_df.sort_values("date")
            .groupby("team_api_id")
            .last()
            .reset_index()
        )

        merged_df = pd.merge(
            team_df,
            latest_attributes,
            on=["team_api_id", "team_fifa_api_id"],
            how="left",
        )

        logo_base_url = "https://example.com/logos/"
        merged_df["logo"] = (
            logo_base_url + merged_df["team_api_id"].astype(str) + ".png"
        )

        final_df = merged_df[
            [
                "team_api_id",
                "team_long_name",
                "team_short_name",
                "logo",
                "buildUpPlaySpeedClass",
                "buildUpPlayDribblingClass",
                "buildUpPlayPassingClass",
                "date",
            ]
        ]
        final_df.columns = [
            "id",
            "name",
            "abbrev",
            "logo",
            "build_up_play_speed",
            "build_up_play_dribble",
            "build_up_play_passing",
            "creation_date",
        ]

        speed_map = {"Balanced": "Balanced", "Fast": "Fast", "Slow": "Slow"}
        dribble_map = {"Lots": "Lots", "Little": "Little", "Normal": "Normal"}
        passing_map = {"Mixed": "Mixed", "Short": "Short", "Long": "Long"}

        final_df["build_up_play_speed"] = final_df["build_up_play_speed"].map(speed_map)
        final_df["build_up_play_dribble"] = final_df["build_up_play_dribble"].map(
            dribble_map
        )
        final_df["build_up_play_passing"] = final_df["build_up_play_passing"].map(
            passing_map
        )

        final_df.to_csv(self.out_file, index=False)

        print(f"Done: {self.out_file}")
