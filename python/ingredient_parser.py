import json
import string
import common

filename = "../other-items/ingredients.json"
out_path = "../test_data/ingredients_first_10.sql"
json_field_names = ["name",
                    "wikidata"
                    # "parents",
                    # "children"
                    ]
# non_string_fields = ["FIXME",
#                      ]

i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant
# Usage
for data in common.parse_json(filename):
    for obj in data:
        if obj[0:2] == "en":
            write_string = "INSERT INTO ingredient (name, wikidata) VALUES ("
            for field in json_field_names:
                write_string += "\'" + str(data[obj][field]["en"]).replace("'", "''") + "\'" if field in data[obj] and "en" in data[obj][field] else "\'unknown\'"
                write_string += ", " if field != "wikidata" else ");\n"

            write_string = write_string.replace("\'unknown\'", "NULL")
            write_string = write_string.replace("unknown", "NULL")
            outfile.write(write_string)


outfile.close()
