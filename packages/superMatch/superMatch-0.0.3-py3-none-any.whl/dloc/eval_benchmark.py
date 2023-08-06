#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   eval_benchmark.py
@Time    :   2021/06/21 14:28:26
@Author  :   mumuychen 
@Version :   1.0
@Contact :   mumuychen@tencent.com
@Copyright:  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
'''


from pathlib import Path
import torch
from tqdm import tqdm
import os
import cv2
import matplotlib.cm as cm
import argparse
import h5py
import numpy as np
from collections import defaultdict

from dloc.core import extract_features, match_features

from dloc.core import extractors, matchers
from dloc.core.utils.base_model import dynamic_load
from dloc.core.utils.utils import read_image, make_matching_plot

torch.set_grad_enabled(False)

class Matching(torch.nn.Module):
    u""" Image Matching Frontend (SuperPoint + SuperGlue) """
    def __init__(self, config={}):
        super(Matching, self).__init__()
        self.config = config
        if not self.config['direct']:
            self.extractor = dynamic_load(extractors, config['extractor']
                                    ['model']['name'])(config['extractor']['model'])

        config['matcher']['model']['landmark'] = config['landmark']
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

def save_h5(dict_to_save, filename):
    """Saves dictionary to hdf5 file"""

    with h5py.File(filename, 'w') as f:
        for key in dict_to_save:
            f.create_dataset(key, data=dict_to_save[key])

def viz_pairs(output, image0, image1, name0, name1, mconf, kpts0, kpts1, mkpts0, mkpts1):
    viz_path = output + '{}_{}_matches.png'.format(name0.split('/')[-1], name1.split('/')[-1])
    # Visualize the matches.
    color = cm.jet(mconf)
    text = [
        'Matcher',
        'Keypoints: {}:{}'.format(len(kpts0), len(kpts1)),
        'Matches: {}'.format(len(mkpts0)),
    ]

    small_text = [
        #'Keypoint Threshold: {:.4f}'.format(k_thresh),
        #'Match Threshold: {:.2f}'.format(m_thresh),
        'Image Pair: {}:{}'.format(name0.split('/')[-1], name1.split('/')[-1]),
    ]

    make_matching_plot(
        image0, image1, kpts0, kpts1, mkpts0, mkpts1, color,
        text, viz_path, True, True, False, 'Matches', small_text)

def main(config, input, input_pairs, output, with_desc=False, resize=[-1], 
        resize_float=True, viz=False):
    # Load the SuperPoint and SuperGlue models.
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    matching = Matching(config).eval().to(device)
    if not os.path.exists(output):
        os.makedirs(output)

    with open(input_pairs, 'r') as f:
        pairs = [l.split() for l in f.readlines()]

    seq_keypoints = defaultdict(dict)
    seq_descriptors = defaultdict(dict)
    seq_matches = defaultdict(dict)
    for i, pair in tqdm(enumerate(pairs), total=len(pairs)):
        # if i % 100:
        #     continue
        name0, name1 = pair[:2]
        # name0, name1 = pair[0], pair[5]
        gray = config['extractor']['preprocessing']['grayscale']
        # Load the image pair.
        align = ''
        if 'disk' in config['extractor']['output']:
            align = 'disk'
        elif 'loftr' in config['matcher']['output']:
            align = 'loftr'

        image0, inp0, scales0 = read_image(
            os.path.join(input, name0), device, resize, 0, resize_float, gray, align)
        image1, inp1, scales1 = read_image(
            os.path.join(input, name1), device, resize, 0, resize_float, gray, align)
        if image0 is None or image1 is None:
            print('Problem reading image pair: {}/{} {}/{}'.format(
                input, name0, input, name1))
            continue

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

        valid = matches > -1
        index0 = np.nonzero(valid)[0]
        index1 = matches[valid]
        if 'megadepth' in input_pairs:
            scene = name0.split('/')[1]
        elif 'imc' in input_pairs:
            scene = name0.split('/')[0] + '/' + name0.split('/')[1]
        elif 'fuchi' in input_pairs:
            scene = name0.split('/')[-1][:-4]
        else:
            scene = name0.split('/')[0]
        # Write matching results
        if 'loftr' in config['matcher']['output']:
            # For all matcher-dependent keypoints
            im0, im1 = name0.split('/')[-1][:-4], name1.split('/')[-1][:-4]
            if "{}-{}".format(im0, im1) not in seq_keypoints[scene]:
                seq_keypoints[scene]["{}-{}".format(im0, im1)] = np.array([kpts0, kpts1])
        else:
            if name0 not in seq_keypoints[scene]:
                seq_keypoints[scene][name0.split('/')[-1][:-4]] = kpts0
                if with_desc:
                    seq_descriptors[scene][name0.split('/')[-1][:-4]] = desc0

            if name1 not in seq_keypoints[scene]:
                seq_keypoints[scene][name1.split('/')[-1][:-4]] = kpts1
                if with_desc:
                    seq_descriptors[scene][name1.split('/')[-1][:-4]] = desc1
        
        seq_matches[scene]['{}-{}'.format(name0.split('/')[-1][:-4], 
                name1.split('/')[-1][:-4])] = np.concatenate([[index0], [index1]])
                
        if viz and i%10==0:
            mconf = conf[valid]
            if not os.path.exists(os.path.join(output, 'viz')):
                os.makedirs(os.path.join(output, 'viz'))
            viz_pairs(os.path.join(output, 'viz/'), image0, image1, 
            name0, name1, mconf, pred['keypoints0'], pred['keypoints1'], 
            pred['keypoints0'][index0], pred['keypoints1'][index1])

    for k in seq_keypoints.keys():
        if not os.path.exists(os.path.join(output, k)):
            os.makedirs(os.path.join(output, k))
        if with_desc:
            save_h5(seq_descriptors[k], os.path.join(output, k,  'descriptors.h5'))
        save_h5(seq_keypoints[k], os.path.join(output, k, 'keypoints.h5'))
        save_h5(seq_matches[k], os.path.join(output, k, 'matches.h5'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Image pair matching and pose evaluation with SuperGlue',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--input_pairs', type=str, default='assets/scannet_sample_pairs_with_gt.txt',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--input_dir', type=str, default='assets/scannet_sample_images/',
        help='Path to the directory that contains the images')
    parser.add_argument(
        '--output_dir', type=str, default='dump_match_pairs/',
        help='Path to the directory in which the .npz results and optionally,'
             'the visualization images are written')

    parser.add_argument(
        '--matcher', choices={'superglue_outdoor', 'superglue_disk', 'superglue_swin_disk',
        'superglue_indoor', 'NN', 'disk', 'cotr', 'loftr'}, 
        default='indoor',help='SuperGlue weights')
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
        '--with_desc', action='store_true',
        help='Saving without descriptors')
    parser.add_argument(
        '--viz', action='store_true',
        help='Visualization matching results')
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
    main(config, opt.input_dir, opt.input_pairs, output_path, opt.with_desc, opt.resize, viz=opt.viz)
