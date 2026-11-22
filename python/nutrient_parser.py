import json
import string
import common

filename = "../content/nutrients.json"
out_path = "../test_data/nutrients.sql"
TABLE_NAME = "nutrient"
COL_NAMES = "name, measuring_unit, wikidata"

json_field_names = [#"name",
                    "unit",
                    "wikidata"
                    ]
# non_string_fields = ["FIXME",
#                      ]

i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant

MAX_CHUNKS = 1000

nut_writer = common.DataWriter(outfile, MAX_CHUNKS, TABLE_NAME, COL_NAMES)
# Usage
for data in common.parse_json(filename):

    for obj in data:
        if "zz:vit" not in obj:
            # build the row of data
            #should look like ('a', NULL , 1) in each index

            # to build the string of data for this obj
            second_layer_list = []
            second_layer_list.append("\'" + str(obj)[3:] + "\'")
            for field in json_field_names:
                second_layer_list.append("\'" + str(data[obj][field]["en"]).replace("'", "''") + "\'" if field in data[obj] and "en" in data[obj][field] else "NULL")
            row_out = "(" +",".join(second_layer_list)+ ")"
            
            # add to writer and flush if full
            nut_writer.add(row_out)

#flush what is left
nut_writer.flush()
    
outfile.close()
