import json
import string
import common

filename = "../other-items/additives.json"
out_path = "../test_data/additives.sql"
TABLE_NAME = "additive"
COL_NAMES = "code, name, is_vegan, is_vegetarian"
json_field_names =  ["name",
                     "vegan",
                     "vegetarian"
                     ]
non_string_fields = [
                     ]
bit_fields =        ["vegan",
                     "vegetarian"
                     ]


i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant

MAX_CHUNKS = 1000
chunk_counter = 0
first_layer_list = []
# Usage
for data in common.parse_json(filename):
    for obj in data:
        if obj[0:2] == "en":
            second_layer_list = []
            #print(data[obj])
            for field in json_field_names:
                if field in bit_fields:
                    second_layer_list.append("1" if not (field in data[obj] and "en" in data[obj][field]) else "0")
                else:
                    second_layer_list.append('\''+obj[4:]+ '\'')
                    second_layer_list.append(str('\'' +data[obj][field]["en"])+ '\''if field in data[obj] and "en" in data[obj][field] else "NULL")
                #second_layer_list.append( ("\'" + obj[4:] + "\'") if field == "vegetarian" )
                #print(obj[4:])
            chunk_counter += 1
                
            row_out = "(" +",".join(second_layer_list)+ ")"
            first_layer_list.append(row_out)
            

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
