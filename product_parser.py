import json
import string

filename = "products.jsonl"
out_path = "test_data/products_first_10.sql"
json_field_names = ["_id", 
                    "product_name",
                    "serving_size",
                    "nutriscore_group",
                    "nutriscore_score",
                    "nova_group",
                    "ecoscore_score",
                    "brand_owner"
                    ]

def parse_jsonl(file_path):
    """Parse a JSONL file line by line"""
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
for data in parse_jsonl(filename):
    if data["languages_tags"][0] == "en:english":
        # assemble INSERT statements
        write_string = "INSERT INTO food_product (barcode, name, serving_size, ns_grade, ns_point, nova_group, ecoscore, brand_owner) VALUES ("
        for field in json_field_names:
            # add data[field] if exists, else add "unknown"
            # + " for string fields
            write_string += "" if (field == "_id" or field == "nutriscore_score" or field == "ecoscore_score") else "\""
            # + field data
            write_string += str(data[field]) if field in data else "unknown"
            # + closing " for string fields
            write_string += "" if (field == "_id" or field == "nutriscore_score" or field == "ecoscore_score") else "\""
            # comma delimited but for the last field
            write_string += ", " if field != "brand_owner" else ");\n"
            # write_string += data["_id"] + ", " + data["product_name"] + ", " + data["serving_size"] + ", " + data["nutriscore_group"] + ", " + data[] + ", " + data["nova_group"] + ", " + data["ecoscore_score"] + ", " + data["brand_owner"]
        # write to a file
        outfile.write(write_string)


    # DEBUG: limit results in loop
    if i == 10:
        break
    else:
        i += 1

outfile.close()
