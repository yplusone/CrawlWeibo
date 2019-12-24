# coding:utf-8
import os
import io
from urllib import request
from PIL import Image

# path = "http://ww1.sinaimg.cn/large/be6ad69bly1ga6w8sk80pj20zk1hc7q0.jpg"
#
# file = request.urlopen(path)
# tmpIm = io.BytesIO (file.read())
# img = Image.open(tmpIm)
#
# print(img.format)  # JPEG
# print(img.size)  # (801, 1200

import pandas as pd
import numpy as np


csv_data = pd.read_csv('./weibo/一沾枕头就能着/6401973058.csv')
data=[{
    'name':'hha',
    'id':1
},{
    'name': 'hha',
    'id': 1
}]
a=data[0].values()
print(a)