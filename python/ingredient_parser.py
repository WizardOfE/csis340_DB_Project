import json
import string
from common import *

filename = "../content/ingredients.json"
out_path = "../test_data/ingredients.sql"
TABLE_NAME = "ingredient"
COL_NAMES = "name, title, wikidata"
json_field_names = ["name",
                    "wikidata"
                    # "parents",
                    # "children"
                    ]
# non_string_fields = ["FIXME",
#                      ]

i = 0
outfile = createOutFile(out_path) # on shared thing to make things consistant

MAX_CHUNKS = 100

ing_writer = DataWriter(outfile, MAX_CHUNKS, TABLE_NAME, COL_NAMES)

# Usage
for data in parse_json(filename):
    for obj in data:
        if obj[0:2] == "en":

            second_layer_list = []

            second_layer_list.append( "\'" + str(obj[3:]) + "\'" )

            for field in json_field_names:
                second_layer_list.append( "\'" + str(data[obj][field]["en"]).replace("'", "''") + "\'" if field in data[obj] and "en" in data[obj][field] else "NULL")
                
            row_out = "(" +",".join(second_layer_list)+ ")"
            # add data to our writer
            ing_writer.add(row_out)     

# flush what is left over
ing_writer.flush()   

outfile.close()
