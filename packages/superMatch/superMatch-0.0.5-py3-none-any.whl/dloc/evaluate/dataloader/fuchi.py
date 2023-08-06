#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   fuchi.py
@Time    :   2021/06/23 10:28:03
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''

import os
import numpy as np

import h5py
import torch
import argparse
import json

class FuchiDataset(torch.utils.data.Dataset):
    def __init__(self, input_pairs, results_path, pairwise=False):
        with open(input_pairs, 'r') as f:
            self.pairs_list = [l.strip('\n').split(' ') for l in f.readlines()]
        self.results_path = results_path
        self.seq_name = ''
        self.pairwise = pairwise

    def __len__(self):
        return len(self.pairs_list)

    def __getitem__(self, idx):
        info = self.pairs_list[idx]
        kpts_shape = int((len(info)-2)/4)
        id = int(kpts_shape*2 + 2)

        template_keypoints = np.array(info[2:id], dtype=float).reshape(kpts_shape, 2)
        query_keypoints = np.array(info[id:], dtype=float).reshape(kpts_shape, 2)
        seq_name = info[0].split('/')[-1][:-4]

        if seq_name != self.seq_name:
            self.keypoints = h5py.File(os.path.join(self.results_path, seq_name, 'keypoints.h5'), 'r')
            self.matches = h5py.File(os.path.join(self.results_path, seq_name, 'matches.h5'), 'r')
            self.seq_name = seq_name
        
        if self.pairwise:
            kpts0, kpts1 = self.keypoints['{}-{}'.format( 
                    info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4])].__array__()
        else:
            kpts0 = self.keypoints[info[0].split('/')[-1][:-4]].__array__()
            kpts1 = self.keypoints[info[1].split('/')[-1][:-4]].__array__()

        matches = self.matches['{}-{}'.format( 
                    info[0].split('/')[-1][:-4], info[1].split('/')[-1][:-4])].__array__()

        return {
            'kpts0': kpts0,
            'kpts1': kpts1,
            'matches': matches,
            'template_keypoints': template_keypoints,
            'query_keypoints': query_keypoints,
            'name0': info[0],
            'name1': info[1]
        }

def parse_keypoint(json_file):
    content = json.load(open(json_file, 'r', encoding='utf-8'))
    for shape in content['shapes']:
        if shape['label'] == 'keypoint':
            keypoint = np.array(shape['points']).reshape((-1))
            return ' '.join(map(str, keypoint))
    raise Exception('{} has no keypoint !'.format(json_file))

def generate_pairs(query_path, template_path):
    pair_file = open('fuchi_pair.txt', 'w')

    for image in os.listdir(query_path):
        if image[-3:] != 'jpg':
            continue
        template_id = image.split('_')[2]
        template_keypoints = parse_keypoint(os.path.join(template_path, template_id + '.json'))
        query_keypoints = parse_keypoint(os.path.join(query_path, image.split('.')[0] + '.json'))
        pair_file.write('{}/{} {}/{} {} {}\n'.format(
                template_path.split('/')[-1], template_id+'.jpg', query_path.split('/')[-1], image, 
                template_keypoints, query_keypoints
        ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Generate Fuchi image pairs',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--query', type=str, default='assets/fuchi/query',
        help='Path to the list of scenes')
    parser.add_argument(
        '--template', type=str, default='assets/fuchi/template',
        help='Path to the list of image pairs') 
    args = parser.parse_args()
    generate_pairs(args.query, args.template)
