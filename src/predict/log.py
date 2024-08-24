import re
from tqdm import tqdm

log_path = 'results/20240820_14_45_44/20240820_14_45_44.log'
output_path = 'src/predict/evaluation_results.txt'

gene_start_pattern = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) - abl - INFO - ---------------------- Single gene training start --------------------------------')
gene_id_pattern = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) - abl - INFO - Abductive Learning on single gene (\S+)\.')
evaluation_pattern = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) - abl - INFO - Evaluation ended, GO/character_accuracy: (\d+\.\d+) GO/reasoning_accuracy: (\d+\.\d+)')
gene_end_pattern = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) - abl - INFO - ---------------------- Single gene training end --------------------------------')

with open(log_path, 'r') as file:
    log_content = file.read()

gene_starts = gene_start_pattern.finditer(log_content)

with open(output_path, 'w') as output_file:
    for match in gene_starts:
        start_pos = match.end()
        next_start_pos = log_content.find('---------------------- Single gene training start --------------------------------', start_pos + 1)
        if next_start_pos == -1:
            next_start_pos = len(log_content)

        gene_log = log_content[start_pos:next_start_pos]

        gene_id_match = gene_id_pattern.search(gene_log)
        if gene_id_match:
            gene_id = gene_id_match.group(2)
        else:
            continue

        evaluation_matches = evaluation_pattern.findall(gene_log)
        if evaluation_matches:
            last_eval_match = evaluation_matches[-1]
            char_accuracy = last_eval_match[1]
            reasoning_accuracy = last_eval_match[2]
            result = f"{gene_id}: GO/character_accuracy: {char_accuracy} GO/reasoning_accuracy: {reasoning_accuracy}"
            output_file.write(result + '\n')
        else:
            # result = f"{gene_id}: No evaluation results found"
            # utput_file.write(result + '\n')
            continue