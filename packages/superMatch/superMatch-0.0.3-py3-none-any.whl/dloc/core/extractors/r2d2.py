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
import torchvision.transforms as tvf

from ..utils.base_model import BaseModel

r2d2_path = Path(__file__).parent / '../../models/r2d2'
# model_path = Path(__file__).parent / '../../../weights/'
sys.path.append(str(r2d2_path))

from extract import load_network, NonMaxSuppression, extract_multiscale
import torchvision.transforms as tvf

class R2D2Desc(BaseModel):
    default_conf = {
        'model': 'r2d2_WASF_N16.pt',
        'scale_f': 2**0.25,
        'min_scale': 0,
        'max_scale': 1,
        'min_size': 256,
        'max_size': 1024,
        'reliability-thr': 0.7,
        'repeatability-thr': 0.7,
        'topk': 5000,
        'RGB_mean': [0.485, 0.456, 0.406],
        'RGB_std': [0.229, 0.224, 0.225],
    }
    required_inputs = ['image']

    def _init(self, conf, model_path):
        self.conf = {**self.default_conf, **conf}

        model_file = str(model_path / Path(self.conf['model']))
        self.net = load_network(model_file)
        self.detector = NonMaxSuppression(
                    rel_thr = self.conf['reliability_thr'], 
                    rep_thr = self.conf['repeatability_thr'])
        self.norm_RGB = tvf.Compose([tvf.Normalize(mean=self.conf['RGB_mean'], std=self.conf['RGB_std'])])
        self.scale_f = self.conf['scale_f']
        self.min_scale = self.conf['min_scale']
        self.max_scale = self.conf['max_scale']
        self.min_size = self.conf['min_size']
        self.max_size = self.conf['max_size']
        self.topk = self.conf['topk']

    def _forward(self, data):
        image = data['image'][0]
        image = self.norm_RGB(image)
        xys, desc, scores = extract_multiscale(self.net, image[None], self.detector,
                                                scale_f   = self.scale_f, 
                                                min_scale = self.min_scale, 
                                                max_scale = self.max_scale,
                                                min_size  = self.min_size, 
                                                max_size  = self.max_size, 
                                                verbose = True)
        xys = xys[:,:2].cpu().numpy()
        desc = desc.cpu().numpy()
        scores = scores.cpu().numpy()
        idxs = scores.argsort()[-self.topk or None:]

        return {
            'keypoints': [torch.from_numpy(xys[idxs])],
            'scores': [torch.from_numpy(scores[idxs])],
            'descriptors': [torch.from_numpy(desc[idxs].T)],
        }
        
