import json
import string
import common

filename = "other-items/additives.json"
out_path = "test_data/additives_first_10.sql"
json_field_names =  ["name",
                     "vegan",
                     "vegetarian",
                     "e_number"
                     ]
non_string_fields = [
                     ]
bit_fields =        ["vegan",
                     "vegetarian"
                     ]


i = 0
outfile = open(out_path, 'r+')
outfile.write("begin;\n")
# Usage
for data in common.parse_json(filename):
    for obj in data:
        if obj[0:2] == "en":
            write_string = "INSERT INTO additive (name, is_vegan, is_vegetarian, code) VALUES ("
            for field in json_field_names:
                write_string += "\'" if field not in non_string_fields else ""
                if field in bit_fields:
                    write_string += "1" if field in data[obj] and "en" in data[obj][field] else "0"
                else:
                    write_string += str(data[obj][field]["en"]).replace("'","''") if field in data[obj] and "en" in data[obj][field] else "unknown"
                write_string += "\'" if field not in non_string_fields else ""
                write_string += ", " if field != "e_number" else ");\n"
            outfile.write(write_string)


            # FIXME: DEBUG, limit results returned by loop
            # if i == 10:
            #     break
            # else:
            #     i += 1

outfile.close()
