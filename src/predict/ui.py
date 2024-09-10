from pywebio.input import select, input
from pywebio.output import *
import pandas as pd
import os
import io

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
                plt.savefig(os.path.join(out_dir, f"{filename.split('.')[0]}_plot.png"))
                plt.close()

def main():
    current_directory = os.getcwd()
    while True:
        put_markdown(r""" # <center> <font face="楷体"> 基于反绎学习和基因知识库的基因表达预测 </font> </center>
    """)
        put_text("当前工作目录:", current_directory)
        in_pth = input("请正确输入想预测的基因的文件路径:")
        out_dir = input("请正确输入想预测的基因的输出路径:")

        if not os.path.exists(in_pth):
            clear()
            put_error("错误: 输入文件路径不存在。请检查路径是否正确。")
            continue
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir)
            except Exception as e:
                clear()
                put_error(f"错误: 无法创建输出目录。请检查路径是否正确。详细错误: {e}")
                continue

        break
    
    clear()
    put_markdown(r""" # <center> <font face="楷体"> 基于反绎学习和基因知识库的基因表达预测 </font> </center>
    """)
    #in_pth_qut = f"'{in_pth}'"
    #out_dir_qut = f"'{out_dir}'"
    #print(in_pth_qut, out_dir_qut)
    put_text("正在预测中，请稍后")
    predict(in_pth, out_dir)

    clear()
    put_markdown(r""" # <center> <font face="楷体"> 基于反绎学习和基因知识库的基因表达预测 </font> </center>
    """)
    path = out_dir
    put_text("基因表达结果预测如下:")
    
    txt_files = [f for f in os.listdir(out_dir) if f.endswith(".txt")]
    txt_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    for filename in txt_files:
        if filename.endswith(".txt"):
            file_path = os.path.join(out_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                put_text(f"文件名: {filename}")
                put_text(content)
                
                # 调用 plt 函数进行画图
                plot(out_dir)
                image_filename = f"{filename.split('.')[0]}_plot.png"
                image_path = os.path.join(out_dir, image_filename)
                put_text(f"图表: {image_filename}")
                put_image(open(image_path, 'rb').read())

                graph_filename = f"res_{filename.split('.')[0].split('_')[-1]}_graph.png"
                image_path = os.path.join(out_dir, graph_filename)
                put_text(f"关系图表: {graph_filename}")
                put_image(open(image_path, 'rb').read())
                put_text('------------------------------------------------------------------------------------------------------------------')

if __name__ == '__main__':
    main()
