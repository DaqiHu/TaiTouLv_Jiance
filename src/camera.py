#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import cv2 #需要提前安装opencv

import config


cap = cv2.VideoCapture(0)
print(cap.isOpened())
ret, img = cap.read()
print(ret, img)
cv2.imshow("Image", img)
cv2.imwrite(config.image_path, img) #此处填写摄像头拍摄的照片的存储路径
cv2.waitKey(0)

# 释放摄像头资源
cap.release()


# In[ ]:
