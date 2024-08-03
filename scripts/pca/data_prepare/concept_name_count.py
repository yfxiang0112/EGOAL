import re

pattern = re.compile(r'GO_\d{7}')

input_file_path = 'dataset/embeddings_preprocess_modified.txt'
output_file_path = 'dataset/concepts/all_concept_name.txt'

with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

matches = []
for line in lines:
    match = pattern.findall(line)
    if match:
        matches.extend(match)
        
with open(output_file_path, 'w') as output_file:
    for match in matches:
        output_file.write(match + '\n')

print(f"Extracted {len(matches)} identifiers and saved to {output_file_path}")
