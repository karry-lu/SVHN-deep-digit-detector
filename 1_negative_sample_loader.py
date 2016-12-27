#-*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

import time
import progressbar

import digit_detector.region_proposal as rp
import digit_detector.file_io as file_io
import digit_detector.annotation as ann
import digit_detector.show as show
import digit_detector.eval as eval
import digit_detector.utils as utils


N_IMAGES = 100
DIR = '../datasets/svhn/train'

# 1. file 을 load
files = file_io.list_files(directory=DIR, n_files_to_sample=N_IMAGES, random_order=False)
annotation_file = "../datasets/svhn/train/digitStruct.json"
detector = rp.MserDetector()

negative_samples = []

bar = progressbar.ProgressBar(widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') ',], maxval=len(files)).start()

for i, image_file in enumerate(files):
    image = cv2.imread(image_file)
    candidates = detector.detect(image, False)
    
    gts, _ = ann.get_annotation(image_file, annotation_file)
    #show.plot_bounding_boxes(image, gts)

    # gts, candidates 의 overlap 을 구한다.
    overlaps = eval.calc_iou(candidates, gts)
    #show.plot_bounding_boxes(image, candidates[overlaps>0.05])

    # Ground Truth 와의 overlap 이 5% 미만인 모든 sample 을 negative set 으로 저장
    negative_boxes = candidates[overlaps<0.05]
    
    # negative box 를 crop, resize to 32x32 해서 sample 에 추가
    for bb in negative_boxes:
        sample = utils.crop_bb(image, bb, padding=0, dst_size=(32,32))
        negative_samples.append(sample)
    
    print image_file
    bar.update(i)

bar.finish()


negative_samples = np.array(negative_samples)    
print negative_samples.shape
labels = np.zeros((len(negative_samples), 1))

file_io.FileHDF5().write(negative_samples, "svhn_dataset.hdf5", "features", "a")
file_io.FileHDF5().write(labels, "svhn_dataset.hdf5", "labels", "a")


# show.plot_images(negative_samples)
    
    
    





