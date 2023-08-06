#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   eval_megadepth.py
@Time    :   2021/06/21 16:35:15
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''
import logging
import numpy as np
import os
import torch
import argparse

from tqdm import tqdm

from dataloader.megadepth import MegaDepthDataset
from utils.evaluation import validation_error
from utils.utils import pose_auc, get_logger

def summary(state):
    print('method\t\t\t AUC@5\t AUC@10\t AUC@20\t Prec\t MScore\t')
    for k,v in state.items():
        aucs, prec, ms = v
        print('{}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t'.format(
                        k.ljust(20), aucs[0], aucs[1], aucs[2], prec, ms))

def log_summary(error, method, logger):
    aucs, prec, ms = error
    logger.info('{}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t'.format(
                        method.ljust(20), aucs[0], aucs[1], aucs[2], prec, ms))

def benchmark_features(input_pairs, results_path, pairwise=False):
    loader = MegaDepthDataset(input_pairs, results_path, pairwise)
    loader = torch.utils.data.DataLoader(loader, num_workers=1)
    pose_errors = []
    precisions = []
    matching_scores = []
    for i, data in tqdm(enumerate(loader), total=len(loader)):
        # if i == 944:
        #     from IPython import embed;embed()
        #     continue
        results = validation_error(data)
        pose_error = np.maximum(results['error_t'], results['error_R'])
        pose_errors.append(pose_error)
        precisions.append(results['precision'])
        matching_scores.append(results['matching_score'])
    
    thresholds = [5, 10, 20]
    aucs = pose_auc(pose_errors, thresholds)
    aucs = [100.*yy for yy in aucs]
    prec = 100.*np.mean(precisions)
    ms = 100.*np.mean(matching_scores)
    return [aucs, prec, ms]


def main(input_pairs, results_path, methods_file, viz = False):
    with open(methods_file, 'r') as f:
        methods = [l.split() for l in f.readlines()]
    errors = {}
    for i in range(len(methods)):
        if i == 0:
            logger = get_logger('megadepth.log')
            # logger.info('method\t\t\t AUC@5\t AUC@10\t AUC@20\t Prec\t MScore\t')
    
        method = methods[i][1]
        folder = methods[i][0]
        if os.path.exists(os.path.join(results_path, folder)):
            if 'loftr' in method.lower() or 'sadnet' in method.lower():
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
        '--methods_file', type=str, default='assets/haptches/methods.txt',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--viz', action='store_true',
        help='Visualization of mAA curve.'
    )
    args = parser.parse_args()
    main(**args.__dict__)