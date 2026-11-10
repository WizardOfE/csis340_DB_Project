import json
import string
import common

pro_filename = "../content/products.jsonl"
add_filename = "../other-items/additives.json"
all_filename = "../other-items/allergens.json"
ing_filename = "../other-items/ingredients.json"
nut_filename = "../other-items/nutrients.json"

ING_TABLE_NAME = "food_ingredient"
ING_COL_NAMES = "food_barcode, ingredient_name"
ALL_TABLE_NAME = "food_allergen"
ALL_COL_NAMES = "food_barcode, allergen_name"
ADD_TABLE_NAME = "food_additive"
ADD_COL_NAMES = "food_barcode, additive_code"
NUT_TABLE_NAME = "food_nutrient"
NUT_COL_NAMES = "food_barcode, nutrient_name"
VIT_TABLE_NAME = "food_vitamin"
VIT_COL_NAMES = "food_barcode, vitamin_name"

MAX_CHUNK = 100

add_outfile = "../test_data/food_add_cross_ref_table_first_10.sql"
all_outfile = "../test_data/food_all_cross_ref_table_first_10.sql"
ing_outfile = "../test_data/food_ing_cross_ref_table_first_10.sql"
nut_outfile = "../test_data/food_nut_cross_ref_table_first_10.sql"
vit_outfile = "../test_data/food_vit_cross_ref_table_first_10.sql"

ing_chunk_count = 0
all_chunk_count = 0
add_chunk_count = 0
nut_chunk_count = 0
vit_chunk_count = 0

ing_fll = []
all_fll = []
add_fll = []
nut_fll = []
vit_fll = []


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

allergen_out = common.createOutFile(all_outfile)
additive_out = common.createOutFile(add_outfile)
ingredient_out = common.createOutFile(ing_outfile)
nutrient_out = common.createOutFile(nut_outfile)
vitamin_out = common.createOutFile(vit_outfile)


# Usage
for data in common.parse_json(pro_filename):
    # # DEBUG: limiting products parsed
    # if i > 30:
    #     break
    # else:
    #     i += 1

    if "countries_tags" not in data: 
        continue

    # check if record is relevant (is english/united states)
    if "en:united-states" in data["countries_tags"]:
        # start filling set, use search strings, normalize found strings
        if "ingredients_tags" in data:

            for ingredient in data["ingredients_tags"]:
                if ingredient[3:] in possible_ingredients:
                    # take results set and create write strings
                    ing_fll.append(f"({data["_id"]}, \'{ingredient[3:]}\')")
                    ing_chunk_count += 1

                    if ing_chunk_count >= MAX_CHUNKS:
                        # create the join of array
                        p = ",\n".join(ing_fll)

                        # create head + body + end
                        write_string = "INSERT INTO "+ING_TABLE_NAME+" ("+ING_COL_NAMES+") VALUES \n" + p + ";\n"
                        ingredient_out.write(write_string) # write out

                        # restart
                        ing_fll = []
                        ing_chunk_count = 0

        if "additives_tags" in data:
            for additive in data["additives_tags"]:
                if additive[3:] in possible_additives:
                    # write_string = f"INSERT INTO food_additive (food_barcode, additive_code) values ({data["_id"]}, '{additive[4:]}');\n"
                    # additive_out.write(write_string)

                    add_fll.append(f"({data["_id"]}, \'{additive[4:]}\')")
                    add_chunk_count += 1

                    if add_chunk_count >= MAX_CHUNKS:
                        # create the join of array
                        p = ",\n".join(add_fll)

                        # create head + body + end
                        write_string = "INSERT INTO "+ADD_TABLE_NAME+" ("+ADD_COL_NAMES+") VALUES \n" + p + ";\n"
                        additive_out.write(write_string) # write out

                        # restart
                        add_fll = []
                        add_chunk_count = 0

        if "allergens_tags" in data:
            for allergen in data["allergens_tags"]:
                if allergen[3:] in possible_allergens:
                    # write_string = f"INSERT INTO food_allergen (food_barcode, allergen_name) values ({data["_id"]}, '{allergen[3:]}');\n"
                    # allergen_out.write(write_string)

                    all_fll.append(f"({data["_id"]}, \'{allergen[3:]}\')")
                    all_chunk_count += 1

                    if all_chunk_count >= MAX_CHUNKS:
                        # create the join of array
                        p = ",\n".join(all_fll)

                        # create head + body + end
                        write_string = "INSERT INTO "+ALL_TABLE_NAME+" ("+ALL_COL_NAMES+") VALUES \n" + p + ";\n"
                        allergen_out.write(write_string) # write out

                        # restart
                        all_fll = []
                        all_chunk_count = 0

        if "sources" in data:
            sources = data["sources"][0]
            if "fields" not in sources: 
                continue
            for element in sources["fields"]:
                if "nutrients" in element:
                    # field is vitamin
                    if "vitamin" in element:
                        if element[10:] in possible_vitamins:
                            # write_string = f"INSERT INTO food_vitamin (food_barcode, vitamin_name) values ({data["_id"]}, '{element[10:]}');\n"
                            # vitamin_out.write(write_string)

                            vit_fll.append(f"({data["_id"]}, \'{element[10:]}\')")
                            vit_chunk_count += 1

                            if vit_chunk_count >= MAX_CHUNKS:
                                # create the join of array
                                p = ",\n".join(vit_fll)

                                # create head + body + end
                                write_string = "INSERT INTO "+VIT_TABLE_NAME+" ("+VIT_COL_NAMES+") VALUES \n" + p + ";\n"
                                vitamin_out.write(write_string) # write out

                                # restart
                                vit_fll = []
                                vit_chunk_count = 0
                    # field is just a nutrient
                    else:
                        if element[10:] in possible_nutrients:
                            # write_string = f"INSERT INTO food_nutrient (food_barcode, nutrient_name) values ({data["_id"]}, '{element[10:]}');\n"
                            # nutrient_out.write(write_string)

                            nut_fll.append(f"({data["_id"]}, \'{element[10:]}\')")
                            nut_chunk_count += 1

                            if nut_chunk_count >= MAX_CHUNKS:
                                # create the join of array
                                p = ",\n".join(nut_fll)

                                # create head + body + end
                                write_string = "INSERT INTO "+NUT_TABLE_NAME+" ("+NUT_COL_NAMES+") VALUES \n" + p + ";\n"
                                nutrient_out.write(write_string) # write out

                                # restart
                                nut_fll = []
                                nut_chunk_count = 0
                    # write_string will have been edited, so write it

# if not completed - additives
if len(add_fll):
    # create the join of array
    p = ",\n".join(add_fll)

    # create head + body + end
    write_string = "INSERT INTO "+ADD_TABLE_NAME+" ("+ADD_COL_NAMES+") VALUES \n" + p + ";\n"
    add_outfile.write(write_string) # write out

# if not completed - allergens
if len(all_fll):
    # create the join of array
    p = ",\n".join(all_fll)

    # create head + body + end
    write_string = "INSERT INTO "+ALL_TABLE_NAME+" ("+ALL_COL_NAMES+") VALUES \n" + p + ";\n"
    all_outfile.write(write_string) # write out

# if not completed - ingredients
if len(ing_fll):
    # create the join of array
    p = ",\n".join(ing_fll)

    # create head + body + end
    write_string = "INSERT INTO "+ING_TABLE_NAME+" ("+ING_COL_NAMES+") VALUES \n" + p + ";\n"
    ing_outfile.write(write_string) # write out

# if not completed - nutrients
if len(nut_fll):
    # create the join of array
    p = ",\n".join(nut_fll)

    # create head + body + end
    write_string = "INSERT INTO "+NUT_TABLE_NAME+" ("+NUT_COL_NAMES+") VALUES \n" + p + ";\n"
    nut_outfile.write(write_string) # write out

# if not completed - vitamins
if len(vit_fll):
    # create the join of array
    p = ",\n".join(vit_fll)

    # create head + body + end
    write_string = "INSERT INTO "+VIT_TABLE_NAME+" ("+VIT_COL_NAMES+") VALUES \n" + p + ";\n"
    vit_outfile.write(write_string) # write out

allergen_out.close()
additive_out.close()
ingredient_out.close()
nutrient_out.close()
vitamin_out.close()
