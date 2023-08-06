#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   loftr.py
@Time    :   2021/06/28 14:53:53
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''

import sys
from pathlib import Path
import numpy as np
import os

import torch

from ..utils.base_model import BaseModel

sys.path.append(str(Path(__file__).parent / '../../models/loftr/'))
# model_path = Path(__file__).parent / '../../../weights/'

from loftr import LoFTR#, default_cfg
from utils.cvpr_ds_config import default_cfg

class loftr(BaseModel):
    default_conf = {
        'weights': 'loftr/outdoor_ds.ckpt',
    }
    required_inputs = [
        'image0', 'image1',
    ]

    def _init(self, conf, model_path):
        self.conf = {**self.default_conf, **conf}
        self.model = LoFTR(config=default_cfg)
        self.model.load_state_dict(torch.load(os.path.join(model_path, 
                                self.conf['weights']))['state_dict'])
        self.model = self.model.eval().cuda()

    def _forward(self, data):
        batch = {'image0': data['image0'], 
                 'image1': data['image1']}
        self.model(batch)
        mkpts0 = batch['mkpts0_f']
        mkpts1 = batch['mkpts1_f']
        mconf = batch['mconf']

        return {
            'keypoints0': [mkpts0],
            'keypoints1': [mkpts1],
            'matches0': [torch.from_numpy(np.arange(mkpts0.shape[0])).to(mkpts0.device)],
            'matching_scores0': [mconf]
        }