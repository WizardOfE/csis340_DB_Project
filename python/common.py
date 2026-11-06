import json
from pathlib import Path

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

# creates file with begin
def createOutFile(out_path):

    Path(out_path).touch()

    o = open(out_path, 'r+')
    o.write("begin;\n")
    return o

class DataWriter:
    def __init__(self, outFile, MAX_CHUNKS, TABLE_NAME, COL_NAMES):
        self.TABLE_NAME = TABLE_NAME
        self.COL_NAMES = COL_NAMES
        self.outFile = outFile
        self.MAX_CHUNKS = MAX_CHUNKS
        self.add_count = 0
        self.values_holder = [] # will hold (a,s,d,f) 


    # add data. Will add to sql when needed
    def add(self, string):
        self.values_holder.append(string)
        self.add_count += 1

        if self.add_count >= self.MAX_CHUNKS:
            self.flush()

    # send what is left over
    def flush(self):
        # create the join of array
        p = ",\n".join(self.values_holder)

        # create head + body + end
        write_string = "INSERT INTO "+self.TABLE_NAME+" ("+self.COL_NAMES+") VALUES \n" + p + ";\n"
        self.outFile.write(write_string) # write out
        
        # restart
        self.values_holder = []
        self.add_count = 0