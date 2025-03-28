import csv


class LeagueEnricher:
    def __init__(self, in_file: str, out_file: str) -> None:
        self.input_file = in_file
        self.output_file = out_file
        self.photo_url_template = "https://example.com/images/leagues/{id}.png"

    def run(self):
        with (
            open(self.input_file, mode="r", encoding="utf-8") as infile,
            open(self.output_file, mode="w", encoding="utf-8", newline="") as outfile,
        ):
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader)

            writer.writerow(["id", "country_id", "name", "photo"])

            for row in reader:
                league_id, country_id, name = row[0], row[1], row[2]
                photo_url = self.photo_url_template.format(id=league_id)
                writer.writerow([league_id, country_id, name, photo_url])

        print(f"Done: {self.output_file}")
