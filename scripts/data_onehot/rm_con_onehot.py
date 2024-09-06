import pandas as pd
import re

def remove_columns_by_regex(df, regex_pattern):
    # Compile the regular expression pattern
    pattern = re.compile(regex_pattern)
    
    # Filter out columns that match the pattern
    columns_to_keep = [col for col in df.columns if not pattern.search(col)]
    
    # Return the DataFrame with only the columns to keep
    return df[columns_to_keep]

df = pd.read_csv('dataset/importance/dataset_onehot.csv')
regex_pattern = r'GO_\d*'

# Remove columns with names matching the regex pattern
df_filtered = remove_columns_by_regex(df, regex_pattern)

df_filtered.drop(columns=['Unnamed: 0'], inplace=True)
df_filtered = df_filtered.set_index('NAME')

float_cols = df_filtered.select_dtypes(include=['float64']).columns
df_filtered[float_cols] = df_filtered[float_cols].fillna(0).astype(int)

print(df_filtered)
df_filtered.to_csv('dataset/importance/dataset_onehot.csv')
