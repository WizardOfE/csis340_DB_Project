import json
import string
import common

filename = "../content/products.jsonl"
out_path = "../test_data/products.sql"

TABLE_NAME = "food_product"
COL_NAMES = "barcode, name, serving_size, ns_grade, ns_point, nova_group, ecoscore, brand_owner"

json_field_names = ["_id", 
                    "product_name",
                    "serving_size",
                    "nutriscore_group",
                    "nutriscore_score",
                    "nova_group",
                    "ecoscore_score",
                    "brand_owner"
                    ]

i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant

MAX_CHUNKS = 500
chunk_counter = 0
first_layer_list = []

# Usage
for data in common.parse_json(filename):
    if "countries_tags" not in data: 
        continue

    # check if record is relevant (is english)
    if "en:united-states" in data["countries_tags"]:

        second_layer_list = []

        # assemble INSERT statements
       # write_string = "INSERT INTO food_product (barcode, name, serving_size, ns_grade, ns_point, nova_group, ecoscore, brand_owner) VALUES ("
        for field in json_field_names:
            o = str(data[field]).replace("'","''") if field in data else "NULL"
            o = "\'" + o +"\'" if not (field == "_id" or field == "nutriscore_score" or field == "ecoscore_score") else o
           
            second_layer_list.append( o)
           

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

            # break if max
            #break

                
# if not completed
if len(first_layer_list):
    # create the join of array
    p = ",\n".join(first_layer_list)

    # create head + body + end
    write_string = "INSERT INTO "+TABLE_NAME+" ("+COL_NAMES+") VALUES \n" + p + ";\n"
    outfile.write(write_string) # write out

outfile.close()
