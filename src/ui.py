from pywebio.input import select, input
from pywebio.output import *
import pandas as pd
import os

import numpy as np
from predict import predict

def main():
    put_markdown(r""" # <center> <font face="楷体"> 基于反绎学习和基因知识库的基因表达预测 </font> </center>
    """)
    current_directory = os.getcwd()
    while True:
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
    in_pth = f"'{in_pth}'"
    out_dir = f"'{out_dir}'"
    print(in_pth, out_dir)
    put_text("正在预测中，请稍后")
    predict(in_pth, out_dir)
    clear()
    put_text("基因表达结果预测如下:")

if __name__ == '__main__':
    main()