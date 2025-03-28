from table_conversions.country import CountryEnricher
from table_conversions.league import LeagueEnricher
from table_conversions.teams import TeamsEnricher

enrichers = [
    CountryEnricher(
        in_name="../csv/Country.csv", out_name="../csv/Country_enriched.csv"
    ),
    LeagueEnricher(in_file="../csv/League.csv", out_file="../csv/League_enriched.csv"),
    TeamsEnricher(
        in_teams_file="../csv/Team.csv",
        in_team_attributes_file="../csv/Team_Attributes.csv",
        out_file="../csv/Team_enriched.csv",
    ),
]


def main():
    for enricher in enrichers:
        if callable(getattr(enricher, "run", None)):
            enricher.run()
        else:
            print(f"run() method not found for enricher {enricher}")


if __name__ == "__main__":
    main()
