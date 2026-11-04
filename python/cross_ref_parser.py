import json
import string
import common

pro_filename = "../content/products.jsonl"
out_path = "../test_data/cross_ref_table_first_10.sql"
add_filename = "../content/additives.json"
all_filename = "../content/allergens.json"
ing_filename = "../content/ingredients.json"
nut_filename = "../content/nutrients.json"

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
possible_ingredients = {}
ing_count = 0
for ing_data in common.parse_json(ing_filename):
    for ing_name in ing_data:
        possible_ingredients[ing_name[3:]] = True
        ing_count += 1

# load dicts of additive names
possible_additives = {}
add_count = 0
for add_data in common.parse_json(add_filename):
    for add_name in add_data:
        possible_additives[add_name[3:]] = True
        add_count += 1

# load dicts of allergen names
possible_allergens = {}
all_count = 0
for all_data in common.parse_json(all_filename):
    for all_name in all_data:
        possible_allergens[all_name[3:]] = True
        all_count += 1

# load dicts of nutrient names
possible_nutrients = {}
possible_vitamins = {}
nut_count = 0
vit_count = 0
for nut_data in common.parse_json(nut_filename):
    for nut_name in nut_data:
        if "vitamin" in nut_name:
            possible_vitamins[nut_name[3:]] = True
            vit_count += 1
        else:
            possible_nutrients[nut_name[3:]] = True
            nut_count += 1

print(f"# of additives: {add_count}\n" +
      f"# of allergens: {all_count}\n" +
      f"# of ingredients: {ing_count}\n" +
      f"# of nutrients: {nut_count}\n" +
      f"# of vitamins: {vit_count}\n")

# Usage
for data in common.parse_json(pro_filename):
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
                if ingredient[3:] in possible_ingredients:
                    # take results set and create write strings
                    write_string = f"INSERT INTO food_ingredient (food_barcode, ingredient_name) values ({data["_id"]}, '{ingredient[3:]}');\n"
                    # write the strings to file
                    # DEBUG: print(f"{ingredient[3:]}: {write_string}")
                    outfile.write(write_string)

        if "additives_tags" in data:
            for additive in data["additives_tags"]:
                if additive[3:] in possible_additives:
                    write_string = f"INSERT INTO food_additive (food_barcode, additive_code) values ({data["_id"]}, '{additive[3:]}');\n"
                    outfile.write(write_string)

        if "allergens_tags" in data:
            for allergen in data["allergens_tags"]:
                if allergen[3:] in possible_allergens:
                    write_string = f"INSERT INTO food_allergen (food_barcode, allergen_name) values ({data["_id"]}, '{allergen[3:]}');\n"
                    outfile.write(write_string)

        if "sources" in data:
            for element in data["sources"][0]["fields"]:
                if "nutrients" in element:
                    # field is vitamin
                    if "vitamin" in element:
                        if element[10:] in possible_vitamins:
                            write_string = f"INSERT INTO food_vitamin (food_barcode, vitamin_name) values ({data["_id"]}, '{element[10:]}');\n"
                            outfile.write(write_string)
                    # field is just a nutrient
                    else:
                        if element[10:] in possible_nutrients:
                            write_string = f"INSERT INTO food_nutrient (food_barcode, nutrient_name) values ({data["_id"]}, '{element[10:]}');\n"
                            outfile.write(write_string)
                    # write_string will have been edited, so write it
    else:
        i += 1



outfile.close()
