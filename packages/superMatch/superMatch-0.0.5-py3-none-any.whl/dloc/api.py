#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   build_model.py
@Time    :   2021/09/28 12:05:27
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''
from pathlib import Path
from pprint import pformat
import torch
from tqdm import tqdm
import os
import cv2
import matplotlib.cm as cm
import argparse
import numpy as np

from .core import extract_features, match_features

from .core import extractors, matchers
from .core.utils.base_model import dynamic_load
from .core.utils.utils import read_image, make_matching_plot

import pydegensac as pyransac

torch.set_grad_enabled(False)

class Matching(torch.nn.Module):
    u""" Image Matching Frontend (SuperPoint + SuperGlue) """
    def __init__(self, config={}, model_path=Path('weights/')):
        super(Matching, self).__init__()
        self.config = config
        if not self.config['direct']:
            self.extractor = dynamic_load(extractors, config['extractor']
                                    ['model']['name'])(config['extractor']['model'], model_path)
        self.matcher = dynamic_load(matchers, config['matcher']
                                ['model']['name'])(config['matcher']['model'], model_path)

    def forward(self, data):
        u""" Run SuperPoint (optionally) and SuperGlue
        SuperPoint is skipped if ['keypoints0', 'keypoints1'] exist in input
        Args:
          data: dictionary with minimal keys: ['image0', 'image1']
        """
        if self.config['direct']:
            return self.matcher(data)
        pred = {}
        # Extract SuperPoint (keypoints, scores, descriptors) if not provided
        if 'keypoints0' not in data:
            pred0 = self.extractor({'image': data['image0']})
            pred.update(dict((k+'0', v) for k, v in pred0.items()))
        if 'keypoints1' not in data:
            pred1 = self.extractor({'image': data['image1']})
            pred.update(dict((k+'1', v) for k, v in pred1.items()))
        # Batch all features
        # We should either have i) one image per batch, or
        # ii) the same number of local features for all images in the batch.
        data.update(pred)
        for k in data:
            if isinstance(data[k], (list, tuple)):
                data[k] = torch.stack(data[k])

        # Perform the matching
        matches = self.matcher(data)
        pred.update(matches)
        return pred


def build_model(extractor, matcher, model_path='', landmark=False, direct=False):
    extractor_conf = extract_features.confs[extractor]
    matcher_conf = match_features.confs[matcher]
    config = {
        'landmark': landmark,
        'extractor': extractor_conf,
        'matcher': matcher_conf,
        'direct': direct,
    }
    # Load the SuperPoint and SuperGlue models.
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = Matching(config, Path(model_path)).eval().to(device)
    return model, config

def get_matches(name0, name1, model, config, resize=[-1], with_desc=False, landmarks=None):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    gray = config['extractor']['preprocessing']['grayscale']
    # Load the image pair.
    align = ''
    if 'disk' in config['extractor']['output']:
        align = 'disk'
    elif 'loftr' in config['extractor']['output']:
        align = 'loftr'

    image0, inp0, scales0 = read_image(name0, device, resize, 0, True, gray, align)
    image1, inp1, scales1 = read_image(name1, device, resize, 0, True, gray, align)
    if image0 is None or image1 is None:
        print('Problem reading image pair: {} {}'.format(
            input/name0, input/name1))
        exit(1)

    # Perform the matching.
    if landmarks:
        template_kpts = landmarks / scales0
        pred = model({'image0': inp0, 'image1': inp1, 'landmark': template_kpts})
    else:
        pred = model({'image0': inp0, 'image1': inp1})

    pred = dict((k, v[0].cpu().numpy()) for k, v in pred.items())
    output = {}
    kpts0, kpts1 = pred['keypoints0']*scales0, pred['keypoints1']*scales1
    matches, conf = pred['matches0'], pred['matching_scores0']
    if with_desc:
        desc0, desc1 = pred['descriptors0'], pred['descriptors1']
        return {'keypoints0': kpts0,
                'keypoints1': kpts1,
                'matches': matches,
                'mconf': conf,
                'descriptors0': desc0,
                'descriptors1': desc1,
            }
    return {'keypoints0': kpts0,
            'keypoints1': kpts1,
            'matches': matches,
            'mconf': conf,
            }

def get_pose(img1, img2, model, config, resize=[-1], landmarks=None, mode='H'):
    output = get_matches(img1, img2, model, config, resize, False, landmarks)
    valid = output['matches'] > -1
    mkpts0 = output['keypoints0'][valid]
    mkpts1 = output['keypoints1'][output['matches'][valid]]
    if mode=='H':
        M, inliers = cv2.findHomography(mkpts0, mkpts1, cv2.RANSAC, 5.0)
    elif mode=='A':
        M, inliers = cv2.getAffineTransform(mkpts0, mkpts1, cv2.RANSAC, 5.0)
    else:
        raise ValueError(f"Pose type {mode} not supported.")
    mkpts0 = mkpts0[inliers.ravel()==1]
    mkpts1 = mkpts1[inliers.ravel()==1]
    return {'pose': M,
            'mkpts0': mkpts0,
            'mkpts1': mkpts1,
            }
