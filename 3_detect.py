#-*- coding: utf-8 -*-
import cv2
import numpy as np
import keras.models

import digit_detector.region_proposal as rp
import digit_detector.show as show
import digit_detector.detect as detector
import digit_detector.file_io as file_io
import digit_detector.preprocess as preproc



detect_model = "detector_model.hdf5"
recognize_model = "recognize_model.hdf5"

mean_value_for_detector = 107.524
mean_value_for_recognizer = 112.833

model_input_shape = (32,32,1)
DIR = '../datasets/svhn/train'

# Todo : mean value 가 recognizer 와 detector 가 다르다.
# 잘 모듈화하자.
if __name__ == "__main__":
    # 1. image files
    img_files = file_io.list_files(directory=DIR, pattern="*.png", recursive_option=False, n_files_to_sample=None, random_order=False)

    preproc_for_detector = preproc.GrayImgPreprocessor(mean_value_for_detector)
    preproc_for_recognizer = preproc.GrayImgPreprocessor(mean_value_for_recognizer)

    char_detector = detector.CnnClassifier(detect_model, model_input_shape, preproc_for_detector)
    char_recognizer = detector.CnnClassifier(recognize_model, model_input_shape, preproc_for_recognizer)
    
    digit_spotter = detector.DigitSpotter(char_detector, char_recognizer, rp.MserRegionProposer())
    
    for img_file in img_files[0:]:
        # 2. image
        img = cv2.imread(img_file)
        
        digit_spotter.run(img, threshold=0.5, do_nms=True, nms_threshold=0.1)







