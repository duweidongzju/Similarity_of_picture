#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/8/19 15:55
# @Author : duweidong
# @File : run.py
# @Software: PyCharm

import os
import glob
import cv2
import sys
import shutil

import numpy as np
import pandas as pd

from joblib import delayed
from joblib import Parallel
from Tool import *


def run(url):
    global failed_urls

    suffix = url.split('.')[-1].split('?')[0]
    save_path = os.path.join(save_root, suffix)
    os.makedirs(save_path, exist_ok=True)
    try:
        cmd = f"you-get -o {save_path} {url}"
        os.system(cmd)
    except:
        failed_urls.append([url])


Gallery819 = 'files/819Gallery.xlsx'
save_root = 'data'

txt = os.path.join(save_root, 'failed_log.txt')

urls = []
if os.path.exists(txt):
    with open(txt, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            urls.append(line.strip())
else:
    pd_excel = pd.read_excel(Gallery819)
    # 如果有多个sheet, 可以指定sheet name
    # pd_excel = pandas.read_excel(excel_name， sheet_name='student')
    table1 = pd_excel.values

    for i, line in enumerate(table1.tolist()):
        _, _, url = line
        urls.append(url)

failed_urls = []
Parallel(n_jobs=5)(delayed(run)(url) for url in urls[:40])
write_txt(txt)