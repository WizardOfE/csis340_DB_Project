import common

filename = "../content/fixed.jsonl"
found_barcodes = set(("temp"))
line_number = 0

for data in common.parse_json(filename):
    if "countries_tags" not in data: 
        continue

    # check if record is relevant (is english)
    if "en:united-states" in data["countries_tags"]:
        if data["code"] in found_barcodes:
            # found a duplicate
            print(f"FOUND DUP: line {line_number}, code: {data["code"]}")
        else:
            # did not find duplicate
            found_barcodes.add(data["code"])

    line_number += 1

