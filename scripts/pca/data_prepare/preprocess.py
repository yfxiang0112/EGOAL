import re

# Process the dataset
def split_data(line):
    pattern = re.compile(r'(http://purl\.obolibrary\.org/obo/GO_\d+)\s+([-.\de\s]+)')
    match = pattern.match(line)
    if match:
        url = match.group(1)
        values = match.group(2).split()
        return url, values
    return None, None

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()
    
    with open(output_file_path, 'w') as output_file:
        for line in lines:
            url, values = split_data(line)
            if url and values:
                output_file.write(f"{url} {' '.join(values)}\n")

input_file_path = 'dataset/ontology.embeddings.txt'  
output_file_path = 'dataset/embeddings_preprocess.txt'  
process_file(input_file_path, output_file_path)

# Check the dataset
def count_data_values(file_path):
    pattern = re.compile(r'(http://purl\.obolibrary\.org/obo/GO_\d+)\s+([-.\de\s]+)')
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                url = match.group(1)
                values = match.group(2).split()
                print(f"URL {url} has {len(values)} values.")
                count += 1
            else:
                assert("No!")
    return count


# Change it
file_path = 'dataset/embeddings_preprocess.txt'
output_file_path = '.ataset/embeddings_preprocess_modified.txt'

with open(file_path, 'r') as file, open(output_file_path, 'w') as output_file:
    for line in file:
        line = line.replace('http://purl.obolibrary.org/obo/', '')
        line = line.replace('GO_', 'GO:')
        output_file.write(line)

print_count = count_data_values(file_path)
print(f"Total print statements executed: {print_count}")
