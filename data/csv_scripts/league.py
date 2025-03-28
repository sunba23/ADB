import csv

input_file = "../csv/League.csv"
output_file = "../csvNew/Formatted_League.csv"
photo_url_template = "https://example.com/images/leagues/{id}.png"

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    header = next(reader)
    
    writer.writerow(["id", "country_id", "name", "photo"])
    
    for row in reader:
        league_id, country_id, name = row[0], row[1], row[2]
        photo_url = photo_url_template.format(id=league_id)
        writer.writerow([league_id, country_id, name, photo_url])

print("Formatted_League.csv has been created successfully.")
