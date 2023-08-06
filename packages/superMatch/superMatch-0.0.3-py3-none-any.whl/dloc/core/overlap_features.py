#! /usr/bin/env python3

import argparse
import torch
from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
import os

from . import overlaps
from .utils.base_model import dynamic_load
from .utils.utils import read_image, visualize_overlap, visualize_overlap_gt, visualize_overlap_crop


'''
A set of standard configurations that can be directly selected from the command
line using their name. Each is a dictionary with the following entries:
    - output: the name of the feature file that will be generated.
    - model: the model configuration, as passed to a feature extractor.
    - preprocessing: how to preprocess the images read from disk.
'''
confs = {
    'sadnet': {
        'output': 'feats-superpoint-n2048-r1024',
        'model': {
            'name': 'sadnet',
            'model': 'sacdnet',
            'stride': 32,
            'last_layer': 2048,
            'num_layers': 50,
            'layer': 'layer4',
            'weights': 'sacdnet_0825_22.pth'#'sacdnet_08111228_6.pth',#'sadnet_08110722_0.pth'
        },
    },
}

@torch.no_grad()
def main(conf, opt):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    Model = dynamic_load(overlaps, conf['model']['name'])
    model = Model(conf['model']).eval().to(device)

    with open(opt.input_pairs, 'r') as f:
        pairs = [l.split() for l in f.readlines()]
    
    for i, pair in tqdm(enumerate(pairs), total=len(pairs)):
        if i % 10 != 0:
            continue
        name1, name2 = pair[:2]
        # Load the image pair.
        image1, inp1, scales1 = read_image(
            os.path.join(opt.input_dir, name1), device, opt.resize, 0, 
                        opt.resize_float, overlap=True)
        image2, inp2, scales2 = read_image(
            os.path.join(opt.input_dir, name2), device, opt.resize, 0, 
                        opt.resize_float, overlap=True)
        box1, box2 = model({'image0': inp1, 'image1': inp2})
        name1 = name1.split('/')[-1]
        name2 = name2.split('/')[-1]
        output = os.path.join(opt.output_dir, name1 + '-' + name2)
        np_box1 = box1[0].cpu().numpy().astype(int)
        np_box2 = box2[0].cpu().numpy().astype(int)
        crop_output = os.path.join(opt.output_dir, 'crop_' + name1 + '-' + name2)
        visualize_overlap_crop(image1, np_box1, image2, np_box2, crop_output)
        # if len(pair) > 2:
        #     gt_box1 = np.array(pair[2:6]).astype(int)
        #     gt_box2 = np.array(pair[6:10]).astype(int)
        #     visualize_overlap_gt(image1, np_box1, gt_box1,
        #                          image2, np_box2, gt_box2, output)
        # else:
        visualize_overlap(image1, np_box1, image2, np_box2, output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_pairs', type=str, default='assets/megadepth/pairs.txt',
        help='Path to the list of image pairs')
    parser.add_argument(
        '--input_dir', type=str, default='assets/megadepth/',
        help='Path to the directory that contains the images')
    parser.add_argument(
        '--output_dir', type=str, default='outputs/',
        help='Path to the directory that contains the images')
    parser.add_argument(
        '--resize', type=int, nargs='+', default=[640, 480],
        help='Resize the input image before running inference. If two numbers, '
             'resize to the exact dimensions, if one number, resize the max '
             'dimension, if -1, do not resize')
    parser.add_argument(
        '--resize_float', action='store_true',
        help='Resize the image after casting uint8 to float')

    parser.add_argument('--conf', type=str, default='sadnet',
                        choices=list(confs.keys()))
    args = parser.parse_args()
    main(confs[args.conf], args)
