#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Gump from CQU
# * Email         : gumpglh@qq.com
# * Create time   : 2017-03-14 23:28
# * Last modified : 2017-03-16 03:54
# * Filename      : counting_voc.py
# * Description   :
# * Copyright © gump. All rights reserved.
# **********************************************************

import argparse
from collections import OrderedDict
import json
import os
import sys
import shutil
sys.path.append(os.path.dirname(sys.path[0]))

from pycocotools.coco import COCO
from pycocotools.json2xml import XmlWriter, XmlReader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Get the image size from an annotation file.")
    parser.add_argument("anno_dir",
            help = "The file which contains all the annotations for a dataset in json format.")
    parser.add_argument("imgsetfile", default = "",
            help = "A file which contains the image set information.")
    parser.add_argument("anno_set", default = "",
            help = "the name of dataset.")
    parser.add_argument("data_type", default = "",
            help = "Specify the output datatpy, eg:val/train.")
    parser.add_argument("anno_out_dir", default = "",
            help = "A dir which stores the new xml file.")
    parser.add_argument("img_out_dir", default = "",
            help = "A dir which stores the new img file.")

    args = parser.parse_args()
    anno_dir = args.anno_dir
    imgsetfile = args.imgsetfile
    data_type = args.data_type
    anno_set = args.anno_set
    anno_out_dir = args.anno_out_dir
    img_out_dir = args.img_out_dir

    """
    #######coco map to voc(id to name)#########
    class_map = {5:"aeroplane", 2:"bicycle", 15:"bird", 9:"boat", 40:"bottle", 6:"bus",
            3:"car", 16:"cat", 57:"chair", 20:"cow", 61:"diningtable", 17:"dog", 18:"horse",
            4:"motorbike", 1:"person", 59:"pottedplant", 19:"sheep", 58:"sofa", 7:"train",
            63:"tvmonitor"}
    #######coco map to voc(id to id)##########
    catId_map = {5:1, 2:2, 15:3, 9:4, 40:5, 6:6, 3:7, 16:8,
            57:9, 20:10, 61:11, 17:12, 18:13, 4:14, 1:15, 59:16,
            19:17, 58:18, 7:19, 63:20}
    """
    class_map = {"background":0, "aeroplane":1, "bicycle":2, "bird":3, "boat":4, "bottle":5,
        "bus":6, "car":7, "cat":8, "chair":9, "cow":10, "diningtable":11, "dog":12, "horse":13,
        "motorbike":14, "person":15, "pottedplant":16, "sheep":17, "sofa":18, "train":19,
        "tvmonitor":20}
    depth = 3
    bboxcount_list = [0 for i in range(len(class_map.keys()))]


    dirname = imgsetfile.split('.')[0]

    if not os.path.exists(imgsetfile):
        print "{} does not exist".format(imgsetfile)
        sys.exit()

    if not os.path.exists(anno_out_dir):
        os.makedirs(anno_out_dir)
    if anno_out_dir:
        #get annotation info
        with open(imgsetfile, 'r') as f:
            for line in f.readlines():
                anno_file = "{}/{}.xml".format(anno_dir, line.strip('\n'))
                anns = XmlReader(anno_file)
                #print anns.getShapes()
                for anno in anns.getShapes():
                    #print bboxcount_list[class_map[anno[0]]]
                    bboxcount_list[class_map[anno[0]]] += 1

#            for ann in anns:
#                cat_id = ann['category_id']
#                if cat_id not in class_map.keys():
#                    continue
#                bbox = ann['bbox']
#                #count the bbox number per class
#                bboxcount_list[catId_map[cat_id] -1] += 1
#
#
#    src = "{}/{}".format(dirname, file_name)
#    dst_dir = "{}/{}".format(img_out_dir, data_type)
#    if not os.path.exists(dst_dir):
#        os.makedirs(dst_dir)
#    dst_path = "{}/{}".format(dst_dir, file_name)
#    shutil.copy(src, dst_path)
#
    output_txt = "{}_{}.txt".format(anno_set, data_type)
    with open(output_txt, "w") as f:
        for i in range(len(bboxcount_list)):
            f.write(str(bboxcount_list[i]) + "\n")
