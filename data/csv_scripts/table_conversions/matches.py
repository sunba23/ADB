import random
import pandas as pd

class MatchEnricher:
    def __init__(
        self,
        in_file: str,
        in_player_file: str,
        out_file: str,
        out_match_player_file: str,
    ) -> None:
        self.in_file = in_file
        self.in_player_file = in_player_file
        self.out_file = out_file
        self.out_match_player_file = out_match_player_file
        self.players_df = pd.read_csv(self.in_player_file)
        self.players_df["player_api_id"] = self.players_df["player_api_id"].astype(int)

    def get_random_player(self, used_players):
        """Returns a random player not already used in the current match"""
        available_players = self.players_df[
            ~self.players_df["player_api_id"].isin(used_players)
        ]
        if available_players.empty:
            raise ValueError("No available unique players left in the database")
        return int(available_players.sample(1)["player_api_id"].values[0])

    def process_matches(self):
        """Processes the match data and adds additional fields"""
        df = pd.read_csv(self.in_file)

        df = df[
            [
                "id",
                "home_team_api_id",
                "away_team_api_id",
                "league_id",
                "season",
                "home_team_goal",
                "away_team_goal",
                "date",
            ]
        ]
        df.rename(
            columns={
                "home_team_api_id": "home_team_id",
                "away_team_api_id": "away_team_id",
                "home_team_goal": "ht_goal",
                "away_team_goal": "at_goal",
                "date": "match_date",
            },
            inplace=True,
        )

        df["weather_id"] = [random.randint(1, 5) for _ in range(len(df))]
        df["odds_home"] = [round(random.uniform(1.0, 5.0), 2) for _ in range(len(df))]
        df["odds_draw"] = [round(random.uniform(1.0, 5.0), 2) for _ in range(len(df))]
        df["odds_away"] = [round(random.uniform(1.0, 5.0), 2) for _ in range(len(df))]

        df.to_csv(self.out_file, index=False)
        print(f"Processed matches saved to {self.out_file}")

    def process_match_players(self):
        """Processes player assignments with automatic duplicate resolution"""
        df = pd.read_csv(self.in_file)
        match_players = []
        
        for _, row in df.iterrows():
            match_id = row["id"]
            used_players = set()
            
            for team_prefix in ["home_player_", "away_player_"]:
                for position in range(1, 12):
                    col = f"{team_prefix}{position}"
                    player = row[col]
                    
                    if pd.isna(player) or player == 0:
                        player = None
                    else:
                        player = int(float(player))
                    
                    if player is not None and player in used_players:
                        player = None
                    
                    if player is None:
                        player = self.get_random_player(used_players)
                    
                    match_players.append([match_id, player])
                    used_players.add(player)
        
        match_player_df = pd.DataFrame(match_players, columns=["match_id", "player_id"])
        match_player_df.insert(0, "id", range(1, len(match_player_df) + 1))
        match_player_df.to_csv(self.out_match_player_file, index=False)
        print(f"Match players saved to {self.out_match_player_file}")

    def run(self):
        """Main execution method"""
        self.process_matches()
        self.process_match_players()
        print(f"Processing complete. Output files:")
        print(f"- Match data: {self.out_file}")
        print(f"- Player assignments: {self.out_match_player_file}")


if __name__ == "__main__":
    processor = MatchEnricher(
        in_file="../csv/Match.csv",
        in_player_file="../csv/Player.csv",
        out_file="../csv/Match_enriched.csv",
        out_match_player_file="../csv/MatchPlayer_enriched.csv"
    )
    processor.run()