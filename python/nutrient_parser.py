import json
import string

filename = "other-items/nutrients.json"
out_path = "test_data/nutrient_first_10.sql"
json_field_names = ["name",
                    "unit",
                    "wikidata"
                    # "parents",
                    # "children"
                    ]
# non_string_fields = ["FIXME",
#                      ]

def parse_json(file_path):
    """Parse JSON"""
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")
                    continue

i = 0
outfile = open(out_path, 'a')
outfile.write("begin;\n")
# Usage
for data in parse_json(filename):
    for obj in data:
        write_string = "INSERT INTO nutrient (name, measuring_unit, wikidata) VALUES ("
        for field in json_field_names:
            write_string += "\'" + str(data[obj][field]["en"]).replace("'", "''") + "\'" if field in data[obj] and "en" in data[obj][field] else "\'unknown\'"
            write_string += ", " if field != "wikidata" else ");\n"

        write_string = write_string.replace("\'unknown\'", "NULL")
        write_string = write_string.replace("unknown", "NULL")
        outfile.write(write_string)


        # FIXME: DEBUG, limit results returned by loop
        if i == 10:
            break
        else:
            i += 1

outfile.close()
