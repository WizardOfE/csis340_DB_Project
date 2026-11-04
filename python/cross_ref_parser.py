import json
import string
import common

filename = "../content/products.jsonl"
out_path = "../test_data/cross_ref_table_first_10.sql"
# search_strings = {
#     "food_vitamin" : sources > fields
#     "food_ingredient" : ingredients_tags 
#     "food_additive" : additives_tags
#     "food_nutrient" : sources > fields
#     "food_allergen" : allergens_tags
# }

i = 0
outfile = common.createOutFile(out_path) # on shared thing to make things consistant

# load dicts of ingredient names

# Usage
for data in common.parse_json(filename):
    # DEBUG: limiting products parsed
    if i > 108:
        break
    # else:
    #     i += 1

    # check if record is relevant (is english)
    if "en:united-states" in data["countries_tags"] and i > 107:

        # start filling set, use search strings, normalize found strings
        if "ingredients_tags" in data:
            for ingredient in data["ingredients_tags"]:
                # take results set and create write strings
                write_string = f"INSERT INTO food_ingredient (food_barcode, ingredient_name) values ({data["_id"]}, '{ingredient[3:]}');\n"
                # write the strings to file
                outfile.write(write_string)

        if "additives_tags" in data:
            for additive in data["additives_tags"]:
                write_string = f"INSERT INTO food_additive (food_barcode, additive_code) values ({data["_id"]}, '{additive[3:]}');\n"
                outfile.write(write_string)

        if "allergens_tags" in data:
            for allergen in data["allergens_tags"]:
                write_string = f"INSERT INTO food_allergen (food_barcode, allergen_name) values ({data["_id"]}, '{allergen[3:]}');\n"
                outfile.write(write_string)

        if "sources" in data:
            for element in data["sources"][0]["fields"]:
                if "nutrients" in element:
                    # field is vitamin
                    if "vitamin" in element:
                        write_string = f"INSERT INTO food_vitamin (food_barcode, vitamin_name) values ({data["_id"]}, '{element[10:]}');\n"
                    # field is just a nutrient
                    else:
                        write_string = f"INSERT INTO food_nutrient (food_barcode, nutrient_name) values ({data["_id"]}, '{element[10:]}');\n"
                    # write_string will have been edited, so write it
                    outfile.write(write_string)
    else:
        i += 1



outfile.close()
