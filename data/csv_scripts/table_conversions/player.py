from datetime import datetime

import pandas as pd


class PlayerEnricher:
    def __init__(self, in_name: str, in_attributes_name: str, out_name: str) -> None:
        self.in_name = in_name
        self.in_attributes_name = in_attributes_name
        self.out_name = out_name

    def run(self) -> None:
        players_df = pd.read_csv(self.in_name)
        attributes_df = pd.read_csv(self.in_attributes_name)

        players_df = players_df.rename(
            columns={"player_name": "name", "player_fifa_api_id": "fifa_api_id"}
        )

        players_df["weight"] = players_df["weight"] * 0.453592

        attributes_df["date"] = pd.to_datetime(attributes_df["date"])
        latest_attributes = (
            attributes_df.sort_values("date")
            .groupby("player_fifa_api_id")
            .last()
            .reset_index()
        )

        attributes_to_merge = latest_attributes[
            [
                "player_fifa_api_id",
                "overall_rating",
                "potential",
                "preferred_foot",
                "attacking_work_rate",
                "defensive_work_rate",
                "crossing",
            ]
        ]

        merged_df = pd.merge(
            players_df,
            attributes_to_merge,
            left_on="fifa_api_id",
            right_on="player_fifa_api_id",
            how="left",
        )

        final_df = merged_df[
            [
                "id",
                "name",
                "birthday",
                "height",
                "weight",
                "overall_rating",
                "potential",
                "preferred_foot",
                "attacking_work_rate",
                "defensive_work_rate",
                "crossing",
            ]
        ].copy()

        final_df["preferred_foot"] = final_df["preferred_foot"].str.upper().str[0]
        final_df["preferred_foot"] = final_df["preferred_foot"].where(
            final_df["preferred_foot"].isin(["R", "L"]), "R"
        )

        try:
            final_df["birthday"] = pd.to_datetime(final_df["birthday"]).dt.strftime(
                "%Y-%m-%d"
            )
        except:
            pass

        final_df.to_csv(self.out_name, index=False)

        print(f"Done: {self.out_name}")
