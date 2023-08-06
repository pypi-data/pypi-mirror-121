#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   imc.py
@Time    :   2021/06/21 15:53:56
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''

import os
import numpy as np

import h5py
import torch

class IMCDataset(torch.utils.data.Dataset):
    def __init__(self, input_pairs, results_path, pairwise=False):
        with open(input_pairs, 'r') as f:
            self.pairs_list = [l.strip('\n').split(' ') for l in f.readlines() if l.split('/')[0] in ['googleurban-val', 'pragueparks-val']]
        # self.pairs_list = self.pairs_list[::10]
        
        self.results_path = results_path
        self.seq_name = ''
        self.pairwise = pairwise

    def __len__(self):
        return len(self.pairs_list)

    def __getitem__(self, idx):
        info = self.pairs_list[idx]
        K0 = np.array(info[2:11], dtype=float).reshape(3, 3)
        K1 = np.array(info[11:20], dtype=float).reshape(3, 3)
        pose = np.array(info[20:36], dtype=float).reshape(4, 4)

        seq_name = info[0].split('/')[1]
        data_name = info[0].split('/')[0]
        if seq_name != self.seq_name:
            self.keypoints = h5py.File(os.path.join(self.results_path, data_name, seq_name, 'keypoints.h5'), 'r')
            self.matches = h5py.File(os.path.join(self.results_path, data_name, seq_name, 'matches.h5'), 'r')
            self.seq_name = seq_name
        
        if self.pairwise:
            kpts0 = self.keypoints['{}-{}'.format( 
                    info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4])].__array__()
            kpts1 = self.keypoints['{}-{}'.format( 
                    info[1].split('/')[-1][:-4], info[0].split('/')[-1][:-4])].__array__()
            # if '{}-{}'.format(info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4]) not in self.keypoints.keys():
            #     print('{}-{}'.format(info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4]))
            # else:
            #     print(self.keypoints['{}-{}'.format( 
            #         info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4])].__array__().shape)
            # kpts0, kpts1 = self.keypoints['{}-{}'.format( 
            #         info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4])].__array__()
        else:
            kpts0 = self.keypoints[info[0].split('/')[-1][:-4]].__array__()
            kpts1 = self.keypoints[info[1].split('/')[-1][:-4]].__array__()

        matches = self.matches['{}-{}'.format( 
                    info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4])].__array__()

        return {
            'kpts0': kpts0,
            'kpts1': kpts1,
            'matches': matches,
            'intrinsics0': K0,
            'intrinsics1': K1,
            'pose': pose,
            'scene': self.seq_name,
            'data': data_name,
            'name0': info[0],
            'name1': info[1],
        }