#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   eval_imc.py
@Time    :   2021/06/17 17:03:09
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''

import numpy as np
import os
import torch
import argparse
import logging

from tqdm import tqdm
from collections import defaultdict

from dataloader.imc import IMCDataset
from utils.evaluation import validation_error
from utils.utils import pose_auc, pose_mAA, get_logger

def summary(state):
    print('methods\t\t\t datasets\t AUC@5\t AUC@10\t AUC@20\t Prec\t MScore\t mAA@10\t')
    for k,v in state.items():
        data, aucs, prec, ms, mAA = v
        for i in range(len(data)):
            if i == 0:
                print('{}\t {}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.6f}\t'.format(
                    k.ljust(20), data[i].split('-')[0], aucs[i][0], aucs[i][1], aucs[i][2], prec[i], ms[i], mAA[i]))
            else:
                print('{}\t {}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.6f}\t'.format(
                    ''.ljust(20), data[i].split('-')[0], aucs[i][0], aucs[i][1], aucs[i][2], prec[i], ms[i], mAA[i]))

def log_summary(error, method, logger):
    data, aucs, prec, ms, mAA = error
    for i in range(len(data)):
        if i == 0:
            logger.info('{}\t {}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.6f}\t'.format(
                method.ljust(20), data[i].split('-')[0], aucs[i][0], aucs[i][1], aucs[i][2], prec[i], ms[i], mAA[i]))
        else:
            logger.info('{}\t {}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.2f}\t {:.6f}\t'.format(
                ''.ljust(20), data[i].split('-')[0], aucs[i][0], aucs[i][1], aucs[i][2], prec[i], ms[i], mAA[i]))


def benchmark_features(input_pairs, results_path, pairwise=False):
    loader = IMCDataset(input_pairs, results_path, pairwise)
    loader = torch.utils.data.DataLoader(loader, num_workers=1)
    pose_errors = defaultdict(list)
    precisions = defaultdict(list)
    matching_scores = defaultdict(list)
    for _, data in tqdm(enumerate(loader), total=len(loader)):
        results = validation_error(data)
        pose_error = np.maximum(results['error_t'], results['error_R'])
        pose_errors[data['data'][0]].append(pose_error)
        precisions[data['data'][0]].append(results['precision'])
        matching_scores[data['data'][0]].append(results['matching_score'])
    
    thresholds = [5, 10, 20]
    all_aucs = []
    all_prec = []
    all_ms = []
    all_mAA = []
    all_data = []
    for k in matching_scores.keys():
        all_data.append(k)
        aucs = pose_auc(pose_errors[k], thresholds)
        all_aucs.append([100.*yy for yy in aucs])
        all_prec.append(100.*np.mean(precisions[k]))
        all_ms.append(100.*np.mean(matching_scores[k]))
        all_mAA.append(100.*pose_mAA(pose_errors[k]))

    all_data.append('total\t')
    aucs = pose_auc(sum(list(pose_errors.values()), []), thresholds)
    all_aucs.append([100.*yy for yy in aucs])
    all_prec.append(100.*np.mean(sum(list(precisions.values()), [])))
    all_ms.append(100.*np.mean(sum(list(matching_scores.values()), [])))
    all_mAA.append(100.*pose_mAA(sum(list(pose_errors.values()), [])))
    return [all_data, all_aucs, all_prec, all_ms, all_mAA]


def main(input_pairs, results_path, methods_file, viz = False):
    with open(methods_file, 'r') as f:
        methods = [l.split() for l in f.readlines()]
    errors = {}
    for i in range(len(methods)):
        if i == 0:
            logger = get_logger('imc.log')
            logger.info('methods\t\t\t datasets\t AUC@5\t AUC@10\t AUC@20\t Prec\t MScore\t mAA@10\t')
    
        method = methods[i][1]
        folder = methods[i][0]
        if os.path.exists(os.path.join(results_path, folder)):
            if 'loftr' in method.lower() or 'sadnet' in  method.lower():
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