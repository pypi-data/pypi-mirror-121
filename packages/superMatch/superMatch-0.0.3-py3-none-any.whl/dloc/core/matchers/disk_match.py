# -*- coding: utf-8 -*-
"""
Author:
    mumuychen@tencent.com

"""
from pathlib import Path
import sys
import torch
import numpy as np

from ..utils.base_model import BaseModel

disk_path = Path(__file__).parent / '../../models/disk'
sys.path.append(str(disk_path))

from match import match

class DiskBrute(BaseModel):
    default_conf = {
        'rt': 0.1,
        'u16': False,
    }
    required_inputs = ['descriptors0', 'descriptors1']

    def _init(self, conf):
        pass

    def _forward(self, data):
        matches = match(data['descriptors0'][0].T, data['descriptors1'][0].T)
        matches0 = torch.ones(data['descriptors0'].shape[2], dtype=int) * -1

        for i in range(matches.shape[1]):
            matches0[matches[0, i]] = matches[1, i]

        return {
            'matches0': [matches0],
            'matching_scores0': [torch.from_numpy(np.ones(matches0.shape[0]))]
        }