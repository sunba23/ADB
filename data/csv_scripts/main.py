from country import CountryEnricher

enrichers = [
    CountryEnricher(in_name="../csv/Country.csv", out_name="../csv/Country_enriched.csv")
]

def main():
    for enricher in enrichers:
        if callable(getattr(enricher, 'run', None)):
            enricher.run()

if __name__ == "__main__":
    main()
