
# Some basic setup:
# Setup detectron2 logger


import random
import json
from math import sqrt
import os
import pandas as pd
import math
from scipy.spatial import distance as dist
import cv2
import torch
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import numpy as np
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries

# import some common detectron2 utilities
# import matplotlib.pyplot as plt

# https://gilberttanner.com/blog/detectron-2-object-detection-with-pytorch#inference-with-pre-trained-model
seg_cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
seg_cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
# seg_cfg.merge_from_file("./mask_rcnn_R_50_FPN_3x.yaml")

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'
seg_cfg.MODEL.DEVICE = device
seg_cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
seg_cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
# seg_cfg.MODEL.WEIGHTS = "./mask_rcnn_R_50_FPN_3x.yaml"
seg_predictor = DefaultPredictor(seg_cfg)


image_files = ['./images/Zac.jpeg',
               './images/Norman.jpeg',
               './images/Kenichi.jpeg',
               './images/Hafiz.jpeg']

measurement_dict = {
    'Norman': {"name": "Norman",
               "shoulder": 17,
               "wrist": 13,
               "waist": 38,
               "knee": 23,
               "ankle": 14,
               "elbow_to_wrist": 22.5,
               "knee_to_ankle": 35,
               "height": 171,
               "shoulder_to_elbow": 0,
               "waist_to_knee": 0,
               "biceps": 0,
               "quad": 0,
               "calf": 0,
               },
    'Kenichi': {"name": "Kenichi",
                "shoulder": 18.5,
                "wrist": 12,
                "elbow_to_wrist": 22.5,
                "knee_to_ankle": 36.5,
                "waist": 37.5,
                "knee": 20.5,
                "ankle": 16.9,
                "height": 176,
                "shoulder_to_elbow": 0,
                "waist_to_knee": 0,
                "biceps": 0,
                "quad": 0,
                "calf": 0,
                },
    "Zac": {"name": "Zac",
            "shoulder": 50,
            "shoulder_to_elbow": 30,
            "elbow_to_wrist": 26,
            "waist": 40,
            "waist_to_knee": 41,
            "knee_to_ankle": 39,
            "biceps": 35,
            "quad": 54,
            "calf": 42,

            "wrist": 8,
            "knee": 16,
            "ankle": 12,
            "height": 175,
            },
    "Hafiz": {"name": "Hafiz",
              "shoulder": 50,
              "shoulder_to_elbow": 30,
              "elbow_to_wrist": 26,
              "waist": 30,
              "waist_to_knee": 49,
              "knee_to_ankle": 38,
              "biceps": 36,
              "quad": 58,
              "calf": 40,

              "wrist": "No Reference Data",
              "knee": "No Reference Data",
              "ankle": "No Reference Data",
              "height": "No Reference Data",
              }
}
rows = ['height', 'shoulder', 'shoulder_to_elbow', 'elbow_to_wrist', 'waist',
        'waist_to_knee', 'knee_to_ankle', 'biceps', 'quad', 'calf']  # 'wrist','knee','ankle']


# Function to find the perimeter
# of an Ellipse
def Perimeter(a, b):
    permeter = 0

    # Compute perimeter
    permeter = (2 * 3.14 *
                sqrt((a * a + b * b) /
                     (2 * 1.0)))

    return permeter


def get_pose(im):
    protoFile = "./pose_deploy_linevec_faster_4_stages.prototxt"
    # protoFile = './pose_deploy_linevec.prototxt'
    weightsFile = "./pose_iter_160000.caffemodel"
    # weightsFile = './pose_iter_440000.caffemodel'
    nPoints = 15
    # nPoints = 18
    frame = im.copy()
    frameCopy = np.copy(frame)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    threshold = 0.1
    POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [
        1, 14], [14, 8], [8, 9], [9, 10], [14, 11], [11, 12], [12, 13]]
    # POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]
    # Read the network into Memory
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
    # Read image
    # frame = cv2.imread(uploaded_file)

    # Specify the input image dimensions
    inWidth = 368
    inHeight = 368

    # Prepare the frame to be fed to the network
    inpBlob = cv2.dnn.blobFromImage(
        frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

    # Set the prepared object as the input blob of the network
    net.setInput(inpBlob)
    output = net.forward()
    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []

    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold:
            cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255),
                       thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(x), int(
                y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)

            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else:
            points.append(None)
    return points


def plot_mes_points(im_mask, points, shoulder_points, waists_points, thigh_points, calf_points):
    try:
        cv2.circle(
            im_mask, (shoulder_points[0], points[2][1]), 8, (0, 0, 255), -1)
        cv2.circle(
            im_mask, (shoulder_points[1], points[2][1]), 8, (0, 255, 0), -1)
    except:
        print("shoulder point problem")
    try:
        cv2.circle(
            im_mask, (waists_points[0], points[8][1]), 8, (0, 0, 255), -1)
        cv2.circle(
            im_mask, (waists_points[1], points[8][1]), 8, (0, 255, 0), -1)
        cv2.circle(
            im_mask, (waists_points[2], points[8][1]), 8, (0, 0, 255), -1)
        cv2.circle(
            im_mask, (waists_points[3], points[8][1]), 8, (0, 255, 0), -1)
        cv2.circle(
            im_mask, (waists_points[4], points[8][1]), 8, (0, 0, 255), -1)
        cv2.circle(
            im_mask, (waists_points[5], points[8][1]), 8, (0, 255, 0), -1)
    except:
        print("wasit  point problem")
    try:
        cv2.circle(im_mask, (thigh_points[0],
                             points[9][1]), 8, (0, 0, 255), -1)
        cv2.circle(im_mask, (thigh_points[1],
                             points[9][1]), 8, (0, 255, 0), -1)
        cv2.circle(im_mask, (thigh_points[2],
                             points[9][1]), 8, (0, 0, 255), -1)
        cv2.circle(im_mask, (thigh_points[3],
                             points[9][1]), 8, (0, 255, 0), -1)
    except:
        print("Thigh point problem")
    try:
        cv2.circle(im_mask, (calf_points[0],
                             points[10][1]), 8, (0, 0, 255), -1)
        cv2.circle(im_mask, (calf_points[1],
                             points[10][1]), 8, (0, 255, 0), -1)
        cv2.circle(im_mask, (calf_points[2],
                             points[10][1]), 8, (0, 0, 255), -1)
        cv2.circle(im_mask, (calf_points[3],
                             points[10][1]), 8, (0, 255, 0), -1)
    except:
        print("Calf point problem")
    return im_mask


def plot_pair_points(im_mask, x, y, text=None):
    cv2.circle(im_mask, (x, y), 8, (0, 255, 0), -1)
    if text:
        cv2.putText(im_mask, text,  (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    1.4, (0, 0, 255), 3, lineType=cv2.LINE_AA)
    return im_mask


def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))


def my_midpoint(ptA, ptB):
    return (ptA[0] + int((ptB[0] - ptA[0]) * 0.5), ptA[1] + int((ptB[1] - ptA[1]) * 0.5))


def threequarterpoint(ptA, ptB):
    return (ptA[0] + int((ptB[0] - ptA[0]) * 0.75), ptA[1] + int((ptB[1] - ptA[1]) * 0.75))


def get_measurements(img_file, im, height, right_side_img=None, left_side_img=None):
    # for img_file in image_files:['height','shoulder','','','','','','','','','','','']
    default_ref = {"name": "None",
                   "shoulder": "No Reference Data",
                   "shoulder_to_elbow": "No Reference Data",
                   "elbow_to_wrist": "No Reference Data",
                   "waist": "No Reference Data",
                   "waist_to_knee": "No Reference Data",
                   "knee_to_ankle": "No Reference Data",
                   "biceps": "No Reference Data",
                   "quad": "No Reference Data",
                   "calf": "No Reference Data",
                   "height": "No Reference Data",

                   "wrist": "No Reference Data",
                   "knee": "No Reference Data",
                   "ankle": "No Reference Data"

                   }

    outputs = seg_predictor(im)
    v = Visualizer(
        im[:, :, ::-1], MetadataCatalog.get(seg_cfg.DATASETS.TRAIN[0]), scale=1.2)

    out = outputs["instances"].pred_masks[0].to("cpu").numpy()

    out_mask = np.zeros(out.shape).astype("uint8")
    out_mask[out] = 255
    # detect pose points
    points = get_pose(im)

    # get the measurements
    edged = cv2.Canny(out_mask, 0, 255)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    shoulder_points = np.argwhere(edged[points[2][1], :] == 255).flatten()
    shoulder_points = [shoulder_points[0], shoulder_points[-1]]

    waists_points = np.argwhere(edged[points[8][1], :] == 255).flatten()

    print("mid point of ", (points[2], points[3]))
    (bicepsx, bicepsy) = threequarterpoint(points[2], points[3])
    print((bicepsx, bicepsy))

    print("mid point of ", (points[8], points[9]))
    (thighx, thighy) = threequarterpoint(points[8], points[9])
    print((thighx, thighy))

    print("mid point of ", (points[9], points[10]))
    (calfx, calfy) = my_midpoint(points[9], points[10])
    print((calfx, calfy))

    thigh_points = np.argwhere(edged[thighy, :] == 255).flatten()
    calf_points = np.argwhere(edged[calfy, :] == 255).flatten()
    biceps_points = np.argwhere(edged[bicepsy, :] == 255).flatten()

    knee_points = np.argwhere(edged[points[9][1], :] == 255).flatten()
    ankle_points = np.argwhere(edged[points[10][1], :] == 255).flatten()

    edged[points[2][1], :] = 255
    edged[bicepsy, :] = 255
    edged[points[8][1], :] = 255
    edged[thighy, :] = 255
    edged[points[9][1], :] = 255
    edged[calfy, :] = 255
    edged[points[10][1], :] = 255

    im_mask = np.copy(im)
    # im_mask = plot_mes_points(im_mask,points,shoulder_points,waists_points,knee_points,ankle_points)
    # cv2_imshow(im_mask)

    try:
        im_mask = plot_pair_points(
            im_mask, shoulder_points[0], points[2][1], text="shoulder")
        im_mask = plot_pair_points(
            im_mask, shoulder_points[1], points[2][1], text="shoulder")
    except:
        print("shoulder point problem")
    try:
        im_mask = plot_pair_points(
            im_mask, waists_points[0], points[8][1], text="Wrist")
        im_mask = plot_pair_points(
            im_mask, waists_points[1], points[8][1], text="Wrist")
        im_mask = plot_pair_points(
            im_mask, waists_points[2], points[8][1], text="Waist")
        im_mask = plot_pair_points(
            im_mask, waists_points[3], points[8][1], text="Waist")
        im_mask = plot_pair_points(
            im_mask, waists_points[4], points[8][1], text="Wrist")
        im_mask = plot_pair_points(
            im_mask, waists_points[5], points[8][1], text="Wrist")
    except:
        print("Waist and Wrist  point problem")
    try:
        im_mask = plot_pair_points(
            im_mask, thigh_points[0], thighy, text="Thigh")
        im_mask = plot_pair_points(
            im_mask, thigh_points[1], thighy, text="Thigh")
        im_mask = plot_pair_points(
            im_mask, thigh_points[2], thighy, text="Thigh")
        im_mask = plot_pair_points(
            im_mask, thigh_points[3], thighy, text="Thigh")
    except:
        print("Thigh point problem")
    try:
        im_mask = plot_pair_points(im_mask, calf_points[0], calfy, text="Calf")
        im_mask = plot_pair_points(im_mask, calf_points[1], calfy, text="Calf")
        im_mask = plot_pair_points(im_mask, calf_points[2], calfy, text="Calf")
        im_mask = plot_pair_points(im_mask, calf_points[3], calfy, text="Calf")
    except:
        print("Calf point problem")
    try:
        im_mask = plot_pair_points(
            im_mask, knee_points[0], points[9][1], text="Knee")
        im_mask = plot_pair_points(
            im_mask, knee_points[1], points[9][1], text="Knee")
        im_mask = plot_pair_points(
            im_mask, knee_points[2], points[9][1], text="Knee")
        im_mask = plot_pair_points(
            im_mask, knee_points[3], points[9][1], text="Knee")
    except:
        print("Knee point problem")
    try:
        im_mask = plot_pair_points(
            im_mask, calf_points[0], points[10][1], text="Ankle")
        im_mask = plot_pair_points(
            im_mask, calf_points[1], points[10][1], text="Ankle")
        im_mask = plot_pair_points(
            im_mask, calf_points[2], points[10][1], text="Ankle")
        im_mask = plot_pair_points(
            im_mask, calf_points[3], points[10][1], text="Ankle")
    except:
        print("Ankle point problem")
    try:
        im_mask = plot_pair_points(
            im_mask, biceps_points[0], bicepsy[10][1], text="Biceps")
        im_mask = plot_pair_points(
            im_mask, biceps_points[1], bicepsy[10][1], text="Biceps")
        im_mask = plot_pair_points(
            im_mask, biceps_points[2], bicepsy[10][1], text="Biceps")
        im_mask = plot_pair_points(
            im_mask, biceps_points[3], bicepsy[10][1], text="Biceps")
    except:
        print("Biceps point problem")
    (feetx, feety) = midpoint(points[10], points[13])
    dB = dist.euclidean(points[0], (feetx, feety))
    pixelsPerMetric = dB / height
    height_r = dB / pixelsPerMetric

    shoulder_pixel = dist.euclidean(
        (points[2][1], shoulder_points[0]), (points[2][1], shoulder_points[1]))
    shoulder_width = shoulder_pixel / pixelsPerMetric

    shoulder_to_elbow = dist.euclidean(points[2], points[3])
    shoulder_to_elbow_length = shoulder_to_elbow / pixelsPerMetric

    elbow_to_wrist = dist.euclidean(points[3], points[4])
    elbow_to_wrist_length = elbow_to_wrist / pixelsPerMetric

    waist_to_knee = dist.euclidean(points[8], points[9])
    waist_to_knee_length = waist_to_knee / pixelsPerMetric

    knee_to_ankle = dist.euclidean(points[9], points[10])
    knee_to_ankle_length = knee_to_ankle / pixelsPerMetric

    try:
        waist_pixel = dist.euclidean(
            (points[8][1], waists_points[2]), (points[8][1], waists_points[3]))
        waist_width = waist_pixel / pixelsPerMetric
    except:
        waist_width = 35

    wrist_pixel = dist.euclidean(
        (points[8][1], waists_points[0]), (points[8][1], waists_points[1]))
    wrist_width = wrist_pixel / pixelsPerMetric

    biceps_pixel = dist.euclidean(
        (bicepsy, biceps_points[0]), (bicepsy, biceps_points[1]))
    biceps_width = biceps_pixel / pixelsPerMetric

    quad_pixel = dist.euclidean(
        (thighy, thigh_points[0]), (thighy, thigh_points[1]))
    quad_width = quad_pixel / pixelsPerMetric

    knee_pixel = dist.euclidean(
        (points[9][1], knee_points[0]), (points[9][1], knee_points[1]))
    knee_width = quad_pixel / pixelsPerMetric

    calf_pixel = dist.euclidean(
        (calfy, calf_points[0]), (calfy, calf_points[1]))
    calf_width = calf_pixel / pixelsPerMetric

    ankle_pixel = dist.euclidean(
        (points[10][1], ankle_points[0]), (points[10][1], ankle_points[1]))
    ankle_width = ankle_pixel / pixelsPerMetric

    print("reference: ", measurement_dict.get(img_file, default_ref))
    ref = []
    measured = []
    for mes in rows:
        ref.append(measurement_dict.get(img_file, default_ref)[mes])

    measured.append(height_r)

    measured.append(shoulder_width)
    measured.append(shoulder_to_elbow_length)
    measured.append(elbow_to_wrist_length)
    measured.append(((waist_width)))
    measured.append(waist_to_knee_length)
    measured.append(knee_to_ankle_length)

    measured.append(biceps_width)
    measured.append(((quad_width)*math.pi))
    measured.append(((calf_width)*math.pi))

    measured.append(((wrist_width)*math.pi))
    measured.append(((knee_width)*math.pi))
    measured.append(((ankle_width)*math.pi))

    mes_data = pd.DataFrame(zip(rows, ref, measured), columns=[
                            'Part', 'Reference', 'Measurement'])

    print(mes_data)
    print(f"""Front Height: {height_r}, shoulder: {shoulder_width/2.54}, arm: {(wrist_width*2) / 2.54}, 
            waist: {(waist_width*2) / 2.54}, quad: {(quad_width*2) / 2.54}, calf: {(calf_width*2) / 2.54}""")

    return im_mask, mes_data, edged
