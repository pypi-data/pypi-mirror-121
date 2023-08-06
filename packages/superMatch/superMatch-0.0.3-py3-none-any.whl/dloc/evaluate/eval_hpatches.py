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

from tqdm import tqdm

from dataloader.hpatches import HpatchesDataset
from utils.evaluation import h_evaluate
from utils.visualization import plot_hpatches_mAA
from utils.utils import get_logger

def summary(stats, n_i=52, n_v=56):
    seq_type, n_feats, n_matches = stats
    print('# Features: {:2f} - [{:d}, {:d}]'.format(np.mean(n_feats), np.min(n_feats), np.max(n_feats)))
    print('# Matches: Overall {:f}, Illumination {:f}, Viewpoint {:f}'.format(
        np.sum(n_matches) / ((n_i + n_v) * 5), 
        np.sum(n_matches[seq_type == 'i']) / (n_i * 5), 
        np.sum(n_matches[seq_type == 'v']) / (n_v * 5))
    )

def log_summary(error, method, logger, n_i=52, n_v=56):
    seq_type, n_feats, n_matches = error[-1]

    logger.info('{}\t {:2f} - [{:d}, {:d}]\t {:.2f}\t {:.2f}\t {:.2f}\t'.format(method.ljust(20), np.mean(n_feats), 
        np.min(n_feats), np.max(n_feats), 
        np.sum(n_matches) / ((n_i + n_v) * 5),
        np.sum(n_matches[seq_type == 'i']) / (n_i * 5),
        np.sum(n_matches[seq_type == 'v']) / (n_v * 5))
    )
        
def benchmark_features(input_pairs, results_path, dataset_path, pairwise=False):
    n_feats = []
    n_matches = []
    seq_type = []
    rng = np.arange(1, 16)
    i_err = {thr: 0 for thr in rng}
    v_err = {thr: 0 for thr in rng}

    loader = HpatchesDataset(input_pairs, dataset_path, results_path, pairwise)
    loader = torch.utils.data.DataLoader(loader, num_workers=1)
    
    for _, data in tqdm(enumerate(loader), total=len(loader)):
        dist = h_evaluate(data['H_gt'][0], data['kpts0'][0], data['kpts1'][0], 
                            data['matches'][0].transpose(1, 0))
        if dist.shape[0] == 0:
            dist = np.array([float("inf")])
        
        for thr in rng:
            if data['seq_name'][0][0] == 'i':
                i_err[thr] += np.mean(dist <= thr)
            else:
                v_err[thr] += np.mean(dist <= thr)
        seq_type.append(data['seq_name'][0][0])
        n_matches.append(data['matches'][0].shape[1])
        n_feats.append(data['kpts1'][0].shape[0])

    seq_type = np.array(seq_type)
    n_feats = np.array(n_feats)
    n_matches = np.array(n_matches)
    
    return i_err, v_err, [seq_type, n_feats, n_matches]

def main(input_pairs, results_path, dataset_path, methods_file, viz = False):
    with open(methods_file, 'r') as f:
        methods = [l.split() for l in f.readlines()]
    errors = {}

    for i in range(len(methods)):
        if i == 0:
            logger = get_logger('hpatches.log')
            logger.info('methods\t\t\t Features\t Overall\t Illumination\t Viewpoint\t')
        method = methods[i][1]
        folder = methods[i][0]
        if os.path.exists(os.path.join(results_path, folder)):
            if "loftr" in method.lower():
                errors[method] = benchmark_features(input_pairs, 
                            os.path.join(results_path, folder), dataset_path, pairwise=True)
            else:
                errors[method] = benchmark_features(input_pairs, 
                                os.path.join(results_path, folder), dataset_path)
            log_summary(errors[method], method, logger)
        # summary(errors[method][-1])
    if viz:
        plot_hpatches_mAA(errors, np.array(methods)[:,1], np.array(methods)[:,1])

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
