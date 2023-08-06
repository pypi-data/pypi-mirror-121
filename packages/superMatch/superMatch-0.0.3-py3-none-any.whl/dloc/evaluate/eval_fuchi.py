#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   eval_fuchi.py
@Time    :   2021/06/23 10:27:58
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''

import numpy as np
import os
import torch
import argparse

from tqdm import tqdm

from dataloader.fuchi import FuchiDataset
from utils.evaluation import pr_evaluate
from utils.utils import get_logger

def summary(state):
    print('method\t\t\t escape@10\t overkill@10\t escape@20\t overkill@20\t escape@30\t overkill@30\t')
    for k,v in state.items():
        escape, overkill = v
        print('{}\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t'.format(
            k.ljust(20), escape[0], overkill[0], escape[1], overkill[1], escape[2], overkill[2]))


def log_summary(error, method, logger):
    escape, overkill = error
    logger.info('{}\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t {:.3f}\t\t'.format(
            method.ljust(20), escape[0], overkill[0], escape[1], overkill[1], escape[2], overkill[2]))

def benchmark_features(input_pairs, results_path):
    loader = FuchiDataset(input_pairs, results_path)
    loader = torch.utils.data.DataLoader(loader, num_workers=1)
    thresholds = [10, 20, 30]
    trans_result = {
        'total': 0,
        'ret=1': 0,
        'F->T': [0]*len(thresholds),
        'T->T': [0]*len(thresholds),
        'F->F': [0]*len(thresholds),
        'T->F': [0]*len(thresholds),
    }
    for _, data in tqdm(enumerate(loader), total=len(loader)):
        warped_template_kpts, warped_query_kpts = \
                                pr_evaluate(data['kpts0'][0], data['kpts1'][0], 
                                data['matches'][0].transpose(1, 0),
                                data['template_keypoints'][0],
                                data['query_keypoints'][0])
        template_error = np.sqrt(np.sum((data['template_keypoints'][0].numpy() - data['query_keypoints'][0].numpy())**2, axis=1)).mean()
        query_error = np.sqrt(np.sum((warped_template_kpts - data['query_keypoints'][0].numpy())**2, axis=1)).mean()

        for i, t in enumerate(thresholds):
            if template_error >= t and query_error < t:
                trans_result['F->T'][i] += 1
            if template_error < t and query_error < t:
                trans_result['T->T'][i] += 1
            if template_error >= t and query_error >= t:
                trans_result['F->F'][i] += 1
            if template_error < t and query_error >= t:
                trans_result['T->F'][i] += 1
    escape = []
    overkill = []

    for i, t in enumerate(thresholds):
        escape.append(trans_result['F->F'][i]/(trans_result['F->F'][i]+trans_result['F->T'][i]))
        overkill.append(trans_result['T->F'][i]/(trans_result['T->F'][i]+trans_result['T->T'][i]))
    return [escape, overkill]

def main(input_pairs, results_path, dataset_path, methods_file, viz = False):
    with open(methods_file, 'r') as f:
        methods = [l.split() for l in f.readlines()]
    errors = {}

    for i in range(len(methods)):
        if i == 0:
            logger = get_logger('fuchi.log')
            logger.info('method\t\t\t escape@10\t overkill@10\t escape@20\t overkill@20\t escape@30\t overkill@30\t')
    
        method = methods[i][1]
        folder = methods[i][0]
        if os.path.exists(os.path.join(results_path, folder)):
            if "loftr" in method.lower():
                errors[method] = benchmark_features(input_pairs, 
                            os.path.join(results_path, folder), pairwise=True)
            else:
                errors[method] = benchmark_features(input_pairs, 
                                os.path.join(results_path, folder))
            log_summary(errors[method], method, logger)
    summary(errors)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Image pair matching and pose evaluation with SuperGlue',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--input_pairs', type=str, default='assets/haptches/scannet_sample_pairs_with_gt.txt',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--results_path', type=str, default='assets/haptches/results',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--dataset_path', type=str, default='assets/haptches/images',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--methods_file', type=str, default='assets/haptches/methods.txt',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--viz', action='store_true',
        help='Visualization of mAA curve.'
    )
    args = parser.parse_args()
    main(**args.__dict__)
