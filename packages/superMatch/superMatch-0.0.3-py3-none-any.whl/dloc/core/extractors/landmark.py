#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   landmark.py
@Time    :   2021/06/28 11:07:03
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''


from pathlib import Path
import numpy as np

import torch
import sys
import cv2
from ..utils.base_model import BaseModel

class Landmark(BaseModel):
    default_conf = {
        'sift': False,
    }
    required_inputs = ['image']

    def _init(self, conf, model_path):
        # using sift keypoints
        self.conf = {**self.default_conf, **conf}

        self.with_sift = self.conf['sift']
        if self.with_sift:
            self.sift = cv2.xfeatures2d.SIFT_create()
        
    def _forward(self, data):
        if self.with_sift:
            kpts = self.sift.detect(data['image'])
            kpts = np.array([[kp.pt[0], kp.pt[1]] for kp in kpts])
            coord = torch.from_numpy(kpts).float()

            
            return {
                'keypoints': [coord],
            }
        else:
            return
        
