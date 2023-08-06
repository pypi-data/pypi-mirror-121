#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   match_file.py
@Time    :   2021/09/23 10:48:07
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

from core import extract_features, match_features

from core import extractors, matchers
from core.utils.base_model import dynamic_load
from core.utils.utils import read_image, make_matching_plot

torch.set_grad_enabled(False)

class Matching(torch.nn.Module):
    u""" Image Matching Frontend (SuperPoint + SuperGlue) """
    def __init__(self, config={}):
        super(Matching, self).__init__()
        self.config = config
        if not self.config['direct']:
            self.extractor = dynamic_load(extractors, config['extractor']
                                    ['model']['name'])(config['extractor']['model'])
        self.matcher = dynamic_load(matchers, config['matcher']
                                ['model']['name'])(config['matcher']['model'])

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

def main(config, input, input_pairs, output, resize, resize_float,  with_desc=False, viz=False):
    # Load the SuperPoint and SuperGlue models.
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    matching = Matching(config).eval().to(device)
    if not os.path.exists(output):
        os.makedirs(output)

    with open(input_pairs, u'r') as f:
        pairs = [l.split() for l in f.readlines()]

    for _, pair in tqdm(enumerate(pairs), total=len(pairs)):
        name0, name1 = pair[:2]
        # If a rotation integer is provided (e.g. from EXIF data), use it:

        gray = config['extractor']['preprocessing']['grayscale']
        # Load the image pair.
        align = ''
        if 'disk' in config['extractor']['output']:
            align = 'disk'
        elif 'loftr' in config['extractor']['output']:
            align = 'loftr'

        image0, inp0, scales0 = read_image(
            os.path.join(input, name0), device, resize, 0, resize_float, gray, align)
        image1, inp1, scales1 = read_image(
            os.path.join(input, name1), device, resize, 0, resize_float, gray, align)
        if image0 is None or image1 is None:
            print('Problem reading image pair: {} {}'.format(
                input/name0, input/name1))
            exit(1)

        # Perform the matching.
        if config['landmark']:
            landmark = np.array(pair[2:], dtype=float).reshape(-1, 2)
            landmark_len = int(landmark.shape[0]/2)
            template_kpts = landmark[:landmark_len] / scales0
            pred = matching({'image0': inp0, 'image1': inp1, 'landmark': template_kpts})
        else:
            pred = matching({'image0': inp0, 'image1': inp1})

        pred = dict((k, v[0].cpu().numpy()) for k, v in pred.items())
        kpts0, kpts1 = pred['keypoints0']*scales0, pred['keypoints1']*scales1
        matches, conf = pred['matches0'], pred['matching_scores0']
        if with_desc:
            desc0, desc1 = pred['descriptors0'], pred['descriptors1']

        if viz:
            valid = matches > -1
            mconf = conf[valid]
            mkpts0 = pred['keypoints0'][valid]
            mkpts1 = pred['keypoints1'][matches[valid]]
            H, inliers = cv2.findHomography(mkpts0,mkpts1,cv2.RANSAC,5.0)
            # F, inliers = cv2.findFundamentalMat(mkpts0, mkpts1, cv2.FM_LMEDS) #without intrinsic failed
            mkpts0 = mkpts0[inliers.ravel()==1]
            mkpts1 = mkpts1[inliers.ravel()==1]
            # M = cv2.getPerspectiveTransform(mkpts0, mkpts1)
            perspective_img0 = cv2.warpPerspective(image0, H, (image0.shape[1], image0.shape[0]))
            perspective_img1 = cv2.warpPerspective(image1, np.linalg.inv(H), (image1.shape[1], image1.shape[0]))
            viz_img = cv2.vconcat([cv2.hconcat([image0, image1]), cv2.hconcat([perspective_img1, perspective_img0])])

            warp_path = output + '{}_{}_warp.png'.format(name0.split('/')[-1], name1.split('/')[-1])
            cv2.imwrite(warp_path, viz_img)
            viz_path = output + '{}_{}_matches.png'.format(name0.split('/')[-1], name1.split('/')[-1])
            # Visualize the matches.
            color = cm.jet(mconf)
            text = [
                'Matcher',
                'Keypoints: {}:{}'.format(len(kpts0), len(kpts1)),
                'Matches: {}'.format(len(mkpts0)),
            ]

            # Display extra parameter info.
            small_text = [
                #'Keypoint Threshold: {:.4f}'.format(k_thresh),
                #'Match Threshold: {:.2f}'.format(m_thresh),
                'Image Pair: {}:{}'.format(name0.split('/')[-1], name1.split('/')[-1]),
            ]

            make_matching_plot(
                image0, image1, pred['keypoints0'], pred['keypoints1'], mkpts0, mkpts1, color,
                text, viz_path, True, True, False, 'Matches', small_text)
        return kpts0, kpts1, matches, conf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Image pair matching and pose evaluation with SuperGlue',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--input_pairs', type=str, default='assets/pairs.txt',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--input_dir', type=str, default='assets/',
        help='Path to the directory that contains the images')
    parser.add_argument(
        '--output_dir', type=str, default='dump_match_pairs/',
        help='Path to the directory in which the .npz results and optionally,'
             'the visualization images are written')

    parser.add_argument(
        '--max_length', type=int, default=-1,
        help='Maximum number of pairs to evaluate')
    parser.add_argument(
        '--matcher', choices={'superglue_outdoor', 'superglue_disk', 'superglue_swin_disk',
        'superglue_indoor', 'NN', 'disk', 'cotr', 'loftr'}, 
        default='superglue_outdoor',help='SuperGlue weights')
    parser.add_argument(
        '--extractor', choices={'superpoint_aachen', 'superpoint_inloc', 'd2net-ss', 
        'r2d2-desc','context-desc', 'landmark', 'aslfeat-desc', 'disk-desc', 'swin-disk-desc'}, 
        default='superpoint_aachen', help='SuperGlue weights')
    parser.add_argument(
        '--resize', type=int, nargs='+', default=[-1],
        help='Resize the input image before running inference. If two numbers, '
             'resize to the exact dimensions, if one number, resize the max '
             'dimension, if -1, do not resize')
    parser.add_argument(
        '--resize_float', action='store_true',
        help='Resize the image after casting uint8 to float')
    
    parser.add_argument(
        '--viz', action='store_true',
        help='Visualize the matches and dump the plots')
    parser.add_argument(
        '--eval', action='store_true',
        help='Perform the evaluation'
             ' (requires ground truth pose and intrinsics)')
    parser.add_argument(
        '--fast_viz', action='store_true',
        help='Use faster image visualization with OpenCV instead of Matplotlib')
    parser.add_argument(
        '--cache', action='store_true',
        help='Skip the pair if output .npz files are already found')
    parser.add_argument(
        '--show_keypoints', action='store_true',
        help='Plot the keypoints in addition to the matches')
    parser.add_argument(
        '--viz_extension', type=str, default='png', choices=['png', 'pdf'],
        help='Visualization file extension. Use pdf for highest-quality.')
    parser.add_argument(
        '--opencv_display', action='store_true',
        help='Visualize via OpenCV before saving output images')
    parser.add_argument(
        '--with_desc', action='store_true',
        help='Saving without descriptors')
    parser.add_argument(
        '--landmark', action='store_true',
        help='Keypoints extraction with landmarks')
    parser.add_argument(
        '--direct', action='store_true',
        help='Match images directe without keypoints extraction.')
        
    opt = parser.parse_args()
    extractor_conf = extract_features.confs[opt.extractor]
    matcher_conf = match_features.confs[opt.matcher]
    config = {
        'landmark': opt.landmark,
        'extractor': extractor_conf,
        'matcher': matcher_conf,
        'direct': opt.direct,
    }
    output_path = os.path.join(opt.output_dir, opt.extractor + '_' + opt.matcher+'/')
    kpts0, kpts1, matches, conf = main(config, opt.input_dir, opt.input_pairs, \
        output_path, opt.resize, opt.resize_float, opt.with_desc, opt.viz)
