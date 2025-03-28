import pathlib

from table_conversions.country import CountryEnricher
from table_conversions.league import LeagueEnricher
from table_conversions.player import PlayerEnricher
from table_conversions.teams import TeamsEnricher
from table_conversions.matches import MatchEnricher

CSVDIR = (pathlib.Path(__file__).parent / "../csv").resolve()

enrichers = [
    CountryEnricher(
        in_name=str(CSVDIR / "Country.csv"),
        out_name=str(CSVDIR / "Country_enriched.csv"),
    ),
    LeagueEnricher(
        in_file=str(CSVDIR / "League.csv"), out_file=str(CSVDIR / "League_enriched.csv")
    ),
    TeamsEnricher(
        in_teams_file=str(CSVDIR / "Team.csv"),
        in_team_attributes_file=str(CSVDIR / "Team_Attributes.csv"),
        out_file=str(CSVDIR / "Team_enriched.csv"),
    ),
    PlayerEnricher(
        in_name=str(CSVDIR / "Player.csv"),
        in_attributes_name=str(CSVDIR / "Player_Attributes.csv"),
        out_name=str(CSVDIR / "Player_enriched.csv"),
    ),
    MatchEnricher(
        in_file=(CSVDIR / "Match.csv"), 
        in_player_file=(CSVDIR / "Player.csv"), 
        out_file= (CSVDIR / "Match_enriched.csv"), 
        out_match_player_file= (CSVDIR / "MatchPlayer_enriched.csv"),
    )
]


def main():
    for enricher in enrichers:
        if callable(getattr(enricher, "run", None)):
            enricher.run()
        else:
            print(f"run() method not found for enricher {enricher}")


if __name__ == "__main__":
    main()
