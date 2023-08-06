# -*- coding: utf-8 -*-
"""
Author:
    mumuychen@tencent.com

"""
import os
import sys

import numpy as np
import tensorflow as tf
from pathlib import Path
import torch
from ..utils.base_model import BaseModel

aslfeat_path = Path(__file__).parent / '../../models/ASLFeat'
# model_path = Path(__file__).parent / '../../../weights/aslfeat'
sys.path.append(str(aslfeat_path))

from models import get_model

class ASLFeat(BaseModel):
    default_conf = {
        'model': 'model.ckpt-380000',
        'max_keypoints': 2048,
        'net': {
            'max_dim': 2048,
            'config': {
                'kpt_n': 8000,
                'kpt_refinement': True,
                'deform_desc': 1,
                'score_thld': 0.5,
                'edge_thld': 10,
                'multi_scale': True,
                'multi_level': True,
                'nms_size': 3,
                'eof_mask': 5,
                'need_norm': True,
                'use_peakiness': True,
            }
        }
    }
    required_inputs = ['image']

    def _init(self, conf, model_path):
        self.conf = {**self.default_conf, **conf}
        path = str(model_path / Path(self.conf['model']))
        self.model = get_model('feat_model')(path, **self.conf['net'])
        self.topk = conf['max_keypoints']

    def _forward(self, data):
        gray_img = data['image'][0].cpu().numpy()*255
        gray_img = gray_img.transpose(1,2,0)

        descriptors, keypoints, scores = self.model.run_test_data(gray_img)
        idxs = scores.argsort()[-self.topk or None:]
        return {
            'keypoints': [torch.from_numpy(keypoints[idxs])],
            'scores': [torch.from_numpy(scores[idxs])],
            'descriptors': [torch.from_numpy(descriptors[idxs].T)],
        }
        
