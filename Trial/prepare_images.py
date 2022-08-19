#======================================================================
# Project Name    : Machine Learning 
# File Name       : prepare_images.py
# Creation Date   : Jun 9 2021
# 
# Copyright (c) 2021 KAMAKE no SUSUME. All rights reserved.
# 
# This source code or any portion thereof must not be  
# reproduced or used in any manner whatsoever.
#======================================================================

import os
import sys
import shutil
import random

def split_data(original_dir, train_size=0.8):
    if os.path.exists('target_datasets'):
        try:
            shutil.rmtree('target_datasets')
        except FileExistsError:
            print('Cannot remove target_datasets directory.')

    try:
        os.mkdir('target_datasets')
    except FileExistsError:
        print('Cannot create target_datasets directory.')

    # get class name from directory name
    dir_lists = os.listdir(original_dir)
    dir_lists = [f for f in dir_lists if os.path.isdir(os.path.join(original_dir, f))]
    original_dir_path = [os.path.join(original_dir, p) for p in dir_lists]

    try:
        os.mkdir('target_datasets/train')
    except FileExistsError:
        print('Cannot create target_datasets/train.')

    try:
        os.mkdir('target_datasets/val')
    except FileExistsError:
        print('Cannot create target_datasets/val.')

    train_dir_path_lists = []
    val_dir_path_lists = []
    for D in dir_lists:
        train_class_dir_path = os.path.join('target_datasets/train', D)
        try:
            os.mkdir(train_class_dir_path)
        except FileExistsError:
            print('Cannot create ' + train_class_dir_path)
        train_dir_path_lists += [train_class_dir_path]
        val_class_dir_path = os.path.join('target_datasets/val', D)
        try:
            os.mkdir(val_class_dir_path)
        except FileExistsError:
            print('Cannot create ' + val_class_dir_path)
        val_dir_path_lists += [val_class_dir_path]

    for i, path in enumerate(original_dir_path):
        files_class = os.listdir(path)
        random.shuffle(files_class)
        num_bunkatu = int(len(files_class) * train_size)
        for fname in files_class[:num_bunkatu]:
            src = os.path.join(path, fname)
            dst = os.path.join(train_dir_path_lists[i], fname)
            shutil.copyfile(src, dst)
            #os.symlink(src, dst)
        for fname in files_class[num_bunkatu:]:
            src = os.path.join(path, fname)
            dst = os.path.join(val_dir_path_lists[i], fname)
            shutil.copyfile(src, dst)
            #os.symlink(src, dst)
        print('Copied images from ' + path)

if __name__ == '__main__':
    param = sys.argv
    if len(param) == 2:
        split_data(param[1])
    elif len(param) == 3:
        split_data(param[1], train_size=float(param[2]))
    else:
        print('Input Error: prepare_images <data-dir> [<train-percentage>]')

