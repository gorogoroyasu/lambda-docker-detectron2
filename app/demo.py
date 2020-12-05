# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import boto3
import cv2
import glob
import os
import time
import tqdm

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger
from predictor import VisualizationDemo

def setup_cfg():
    # load config from file and command-line arguments
    cfg = get_cfg()
    # Lambda は CPU しか使えない
    cfg.MODEL.DEVICE = 'cpu'
    # この辺を変えると、別のモデルが使える。
    config_file = '/function/faster_rcnn_R_50_C4_1x.yaml'
    cfg.MODEL.WEIGHTS = 'https://dl.fbaipublicfiles.com/detectron2/COCO-Detection/faster_rcnn_R_50_C4_1x/137257644/model_final_721ade.pkl'

    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = 0.5
    cfg.freeze()
    return cfg

def from_s3_to_tmp(event):
    bucket = event['bucket']
    path = event['s3_path']
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucket)
    bucket.download_file(path, '/tmp/input.jpg')

def get_result(event):
    """
    docstring
    """
    setup_logger(name="fvcore")
    logger = setup_logger()
    cfg = setup_cfg()
    demo = VisualizationDemo(cfg)

    from_s3_to_tmp(event)
    # use PIL, to be consistent with evaluation
    img = read_image('/tmp/input.jpg', format="BGR")
    start_time = time.time()
    predictions, visualized_output = demo.run_on_image(img)
    out_filename = '/tmp/output.jpg'
    visualized_output.save(out_filename)
