import json
import string
import common

filename = "../other-items/nutrients.json"
out_path = "../test_data/nutrient.sql"
TABLE_NAME = "nutrient"
COL_NAMES = "name, measuring_unit, wikidata"

json_field_names = ["name",
                    "unit",
                    "wikidata"
                    ]
# non_string_fields = ["FIXME",
#                      ]

i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant

MAX_CHUNKS = 1000
chunk_counter = 0
first_layer_list = []
# Usage
for data in common.parse_json(filename):

    for obj in data:
        if "zz:vit" not in obj:

            second_layer_list = []

            for field in json_field_names:
                second_layer_list.append("\'" + str(data[obj][field]["en"]).replace("'", "''") + "\'" if field in data[obj] and "en" in data[obj][field] else "NULL")
            chunk_counter += 1
                
            row_out = "(" +",".join(second_layer_list)+ ")"
            first_layer_list.append(row_out)
            
            # if we have reached max
            if chunk_counter >= MAX_CHUNKS:
                # create the join of array
                p = ",\n".join(first_layer_list)

                # create head + body + end
                write_string = "INSERT INTO "+TABLE_NAME+" ("+COL_NAMES+") VALUES \n" + p + ";\n"
                outfile.write(write_string) # write out

                # restart
                first_layer_list = []
                chunk_counter = 0
    
# if not completed
if len(first_layer_list):
    # create the join of array
    p = ",\n".join(first_layer_list)

    # create head + body + end
    write_string = "INSERT INTO "+TABLE_NAME+" ("+COL_NAMES+") VALUES \n" + p + ";\n"
    outfile.write(write_string) # write out
    
    
outfile.close()
