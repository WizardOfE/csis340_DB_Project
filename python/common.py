import json

def parse_json(file_path):
    """Parse JSON"""
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")
                    continue                   