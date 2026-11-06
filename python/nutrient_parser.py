import json
import string
import common

filename = "../other-items/nutrients.json"
out_path = "../test_data/nutrient.sql"
json_field_names = ["name",
                    "unit",
                    "wikidata"
                    # "parents",
                    # "children"
                    ]
# non_string_fields = ["FIXME",
#                      ]

i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant

MAX_CHUNKS = 10

chunk_counter = 0

# Usage
for data in common.parse_json(filename):
    first_layer_list = []


    for obj in data:
        if "zz:vit" not in obj:

            second_layer_list = []

            for field in json_field_names:
                second_layer_list.append("\'" + str(data[obj][field]["en"]).replace("'", "''") + "\'" if field in data[obj] and "en" in data[obj][field] else "NULL")
                chunk_counter += 1
                
            row_out = "(" +",".join(second_layer_list)+ ")"
            first_layer_list.append(row_out)

            
        
            if chunk_counter == MAX_CHUNKS:
                print("chuck")
                p = ",\n".join(first_layer_list)
                write_string = "INSERT INTO nutrient (name, measuring_unit, wikidata) VALUES (" + p + ")"
                outfile.write(write_string)
                break
            else:
                first_layer_list = []
    
outfile.close()
