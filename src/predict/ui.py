from pywebio.input import select, input
from pywebio.output import *
import pandas as pd
import os
import io
import sys
import numpy as np
from predict import predict
import matplotlib.pyplot as plt

def plot(out_dir):
    for filename in os.listdir(out_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(out_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                df = pd.read_csv(io.StringIO(content), sep='\t')
                gene_ids = df['gene_id']
                confs = df['conf']
                
                plt.figure(figsize=(10, 6))
                plt.bar(gene_ids, confs, color='skyblue')
                plt.xlabel('Gene ID')
                plt.ylabel('Confidence')
                plt.title('Gene Expression Confidence')
                plt.xticks(rotation=90)  
                plt.tight_layout()
                plt.savefig(os.path.join(out_dir, "conf_plot.png"))
                plt.close()

def main():
    clear()
    current_directory = os.getcwd()
    while True:
        put_markdown(r""" # <center> EGOAL: gene Expression prediction based on Abductive Learning and Gene Ontology </font> </center>
    """)
        put_text("current working dir:", current_directory)
        in_str = input("experiment descriptions:")
        out_dir = input("output directory:")
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir)
            except Exception as e:
                clear()
                put_error(f"Error: cannot create directory\n {e}")
                continue
        break
    
    clear()
    put_markdown(r""" # <center> EGOAL: gene Expression prediction based on Abductive Learning and Gene Ontology </font> </center>
    """)
    #put_text("正在预测中，请稍后")
    predict('', out_dir, use_gui= True, input_str= in_str)
    clear()
    put_markdown(r""" # <center> EGOAL: gene Expression prediction based on Abductive Learning and Gene Ontology </font> </center>
    """)
    path = out_dir
    put_text("Predict Result:")
    
    #txt_files = [f for f in os.listdir(out_dir) if f.endswith(".txt")]
    #txt_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    txt_files = ['result.txt']
    
    for filename in txt_files:
        if filename.endswith(".txt"):
            file_path = os.path.join(out_dir, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                put_text(f"reading from {filename}")
                put_text(content)
                
                plot(out_dir)
                image_filename = "conf_plot.png"
                image_path = os.path.join(out_dir, image_filename)
                put_text(f"Classification Confidence: {image_filename}")
                put_image(open(image_path, 'rb').read())
                graph_filename = f"regulation_graph.png"
                image_path = os.path.join(out_dir, graph_filename)
                put_text(f"Regulation Pathway Graph: {graph_filename}")
                put_image(open(image_path, 'rb').read())
                put_text('------------------------------------------------------------------------------------------------------------------')
    
    put_buttons(['Exit', 'Home'], onclick=[sys.exit(), main])

if __name__ == '__main__':
    main()
