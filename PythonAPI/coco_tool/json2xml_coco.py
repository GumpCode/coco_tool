#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Gump from CQU
# * Email         : gumpglh@qq.com
# * Create time   : 2017-03-14 23:28
# * Last modified : 2017-03-14 23:28
# * Filename      : json2xml_coco.py
# * Description   :
# * Copyright © 2016. All rights reserved.
# **********************************************************

import argparse
from collections import OrderedDict
import json
import os
import sys
import shutil
import cv2
sys.path.append(os.path.dirname(sys.path[0]))

from pycocotools.coco import COCO
from pycocotools.json2xml import XmlWriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Get the image size from an annotation file.")
    parser.add_argument("annofile",
            help = "The file which contains all the annotations for a dataset in json format.")
    parser.add_argument("imgsetfile", default = "",
            help = "A file which contains the image set information.")
    #parser.add_argument("namesizefile", default = "",
    #        help = "A file which stores the name size information.")
    parser.add_argument("data_type", default = "",
            help = "Specify the output datatpy, eg:val/train.")
    parser.add_argument("anno_out_dir", default = "",
            help = "A dir which stores the new xml file.")
    parser.add_argument("img_out_dir", default = "",
            help = "A dir which stores the new img file.")

    args = parser.parse_args()
    annofile = args.annofile
    imgsetfile = args.imgsetfile
    #namesizefile = args.namesizefile
    data_type = args.data_type
    anno_out_dir = args.anno_out_dir
    img_out_dir = args.img_out_dir

    class_map = {5:"aeroplane", 2:"bicycle", 16:"bird", 9:"boat", 44:"bottle", 6:"bus",
            3:"car", 17:"cat", 62:"chair", 21:"cow", 67:"diningtable", 18:"dog", 19:"horse",
            4:"motorbike", 1:"person", 64:"pottedplant", 20:"sheep", 63:"sofa", 7:"train",
            72:"tvmonitor"}
    catId_map = {5:1, 2:2, 16:3, 9:4, 44:5, 6:6, 3:7, 17:8,
            62:9, 21:10, 67:11, 18:12, 19:13, 4:14, 1:15, 64:16,
            20:17, 63:18, 7:19, 72:20}
    depth = 3
    bboxcount_list = [0 for i in range(len(class_map.keys()))]
    imgcount_list = [0 for i in range(len(class_map.keys()))]


    dirname = imgsetfile.split('.')[0]
    # initialize COCO api.
    coco = COCO(annofile)

    if not os.path.exists(imgsetfile):
        print "{} does not exist".format(imgsetfile)
        sys.exit()

    if not os.path.exists(anno_out_dir):
        os.makedirs(anno_out_dir)
    # Read image info.
    imgs = dict()
    img_ids = coco.getImgIds()
    prog = 0
    for img_id in img_ids:
        # get image info
        img = coco.loadImgs(img_id)[0]
        file_name = img["file_name"]
        name = os.path.splitext(file_name)[0]
        xml_path = "{}/{}.xml".format(anno_out_dir, name)
        imgs[name] = img
        if anno_out_dir:
            #get annotation info
            anno_ids = coco.getAnnIds(imgIds=img_id, iscrowd=None)
            anns = coco.loadAnns(anno_ids)
            result = XmlWriter("coco", file_name,
                (int(img["height"]), int(img["width"]), depth))
            flag = 0
            for ann in anns:
                cat_id = ann['category_id']
                if cat_id not in class_map.keys():
                    continue
                else:
                    flag = 1
                bbox = ann['bbox']
                #count the bbox number per class
                #bboxcount_list[catId_map[cat_id] -1] += 1
                #if file_name == "COCO_val2014_000000333294.jpg":
                #    print cat_id
                #    print class_map[cat_id]
                #    sys.exit(0)
                result.addBndBox(bbox[0], bbox[1], bbox[0]+ bbox[2], bbox[1]+ bbox[3], class_map[cat_id])

            if flag == 1:
                result.save(xml_path)
                src = "{}/{}".format(dirname, file_name)
                dst_dir = "{}/{}".format(img_out_dir, data_type)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                dst_path = "{}/{}".format(dst_dir, file_name)
                if not os.path.exists(dst_path):
                    shutil.copy(src, dst_path)

        prec = 100. * prog / len(img_ids)
        x = int(2 * prec/5)
        print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
        print '%.2f%%' % prec, '(%d/%d)' % (prog, len(img_ids)),
        sys.stdout.flush()
        prog += 1
    if prog:print

#    output_txt = "{}.txt".format(data_type)
#    with open(output_txt, "w") as f:
#        for i in range(len(bboxcount_list)):
#            f.write(str(bboxcount_list[i]) + "\n")
