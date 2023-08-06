# -*- coding: utf-8 -*-
"""
Author:
    mumuychen@tencent.com

"""

import sys
import torch
from pathlib import Path
# sys.path.append('..')
from ..utils.base_model import BaseModel

sys.path.append(str(Path(__file__).parent / '../../third_party'))
model_path = Path(__file__).parent / '../../models/'

from SADNet.src.model import build_detectors
from SADNet.src.config.default import get_cfg_defaults

class SADNet(BaseModel):
    default_conf = {
        'model': 'sadnet',
        'num_layers': 50,
        'stride': 32,
        'last_layer': 2048,
        'weights': 'sadnet.pth',
        'sampling_radius': 1.0,
    }
    required_inputs = [
        'image0','image1','mask0', 'mask1'
    ]

    def build_cfg(self, conf):
        cfg = get_cfg_defaults()
        cfg.SADNET.MODEL = conf['model']
        cfg.SADNET.BACKBONE.STRIDE = conf['stride']
        cfg.SADNET.BACKBONE.LAYER = conf['layer']
        cfg.SADNET.BACKBONE.LAST_LAYER = conf['last_layer']
        cfg.SADNET.HEAD.SAMPLING_RADIUS = conf['sampling_radius']
        return cfg

    def _init(self, conf):
        self.conf = {**self.default_conf, **conf}
        self.cfg = self.build_cfg(self.conf)
        self.net = build_detectors(self.cfg.SADNET)
        model_file = model_path / self.conf['weights']
        self.net.load_state_dict(torch.load(model_file))

    def _forward(self, data):
        box1, box2 = self.net.forward_dummy(data['image0'], data['image1'] 
                                            ,data['mask0'], data['mask1'])
        return box1, box2