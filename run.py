#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/8/19 15:55
# @Author : duweidong
# @File : run.py
# @Software: PyCharm

import os
import shutil

import numpy as np
import pandas as pd

from joblib import delayed
from joblib import Parallel
from Tool import *


def run(params):
    picture_id, url = params

    save_path = os.path.join(save_root, picture_id)
    os.makedirs(save_path, exist_ok=True)
    try:
        cmd = f"you-get -o {save_path} {url}"
        os.system(cmd)
    except:
        pass

    if len(os.listdir(save_path)) == 0:
        shutil.rmtree(save_path)


def run2(params):
    picture_id, url = params
    save_path = os.path.join(save_root, picture_id)
    os.makedirs(save_path, exist_ok=True)
    try:
        cmd = f"wget -P {save_path} {url}"
        os.system(cmd)
    except:
        print('failed download')
    if len(os.listdir(save_path)) == 0:
        shutil.rmtree(save_path)


save_root = '/mnt/dl-storage/dg-cephfs-0/public/Ambilight/Xsidu2'
os.makedirs(save_root, exist_ok=True)


def get_download_urls():
    urls = []
    downloaded_picture_ids = []
    for downloaded_picture_id in os.listdir(save_root):
        if len(os.listdir(os.path.join(save_root, downloaded_picture_id))) == 0:
            continue
        downloaded_picture_ids.append(downloaded_picture_id)

    for picture_id, url in read_txt("files/id_urls"):
        if picture_id not in downloaded_picture_ids:
            urls.append([picture_id, url])
    return urls


urls = get_download_urls()

Parallel(n_jobs=50)(delayed(run)(url) for url in urls)