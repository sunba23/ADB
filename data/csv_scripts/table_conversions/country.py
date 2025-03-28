import csv
from datetime import datetime

import pycountry
import pytz


class CountryEnricher:
    def __init__(self, in_name: str, out_name: str) -> None:
        self.in_name = in_name
        self.out_name = out_name

    def get_country_details(self, name):
        abbrev = "XX"
        flag_url = ""
        is_eu = False
        tz_offset = "Unknown"

        try:
            country = pycountry.countries.get(name=name)
            if not country:
                return None

            abbrev = country.alpha_2
            flag_url = f"https://flagcdn.com/w320/{abbrev.lower()}.png"
            is_eu = abbrev in {
                "AT",
                "BE",
                "BG",
                "HR",
                "CY",
                "CZ",
                "DK",
                "EE",
                "FI",
                "FR",
                "DE",
                "GR",
                "HU",
                "IE",
                "IT",
                "LV",
                "LT",
                "LU",
                "MT",
                "NL",
                "PL",
                "PT",
                "RO",
                "SK",
                "SI",
                "ES",
                "SE",
            }
            if abbrev in ["PT", "IE", "EN", "IS", "SCO", "WL"]:
                tz_offset = "UTC+00:00"
            elif abbrev in ["GR", "TR", "BG", "RO", "UA", "MO", "LT", "LV", "EE", "FI"]:
                tz_offset = "UTC+02:00"
            else:
                tz_offset = "UTC+01:00"

        except Exception as e:
            print(f"Error processing {name}: {str(e)}")

        return abbrev, flag_url, is_eu, tz_offset

    def run(self) -> None:
        with open(self.in_name, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            countries = []
            for row in reader:
                details = self.get_country_details(row["name"])
                if details:
                    row.update(
                        {
                            "abbrev": details[0],
                            "flag": details[1],
                            "is_eu": details[2],
                            "tz_offset": details[3],
                        }
                    )
                    countries.append(row)

        with open(self.out_name, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["id", "name", "abbrev", "flag", "is_eu", "tz_offset"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(countries)

        print(f"Done: {self.out_name}")
