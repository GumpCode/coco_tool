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
    parser.add_argument("out_dir", default = "",
            help = "A dir which stores the new xml file.")

    args = parser.parse_args()
    annofile = args.annofile
    imgsetfile = args.imgsetfile
    #namesizefile = args.namesizefile
    out_dir = args.out_dir

    seleted_map = {'5':'1', '2':'2', '15':'3', '9':'4', '40':'5', '6':'6', '3':'7', '16':'8',
            '57':'9', '20':'10', '61':'11', '17':'12', '18':'13', '4':'14', '1':'15', '59':'16',
            '19':'17', '58':'18', '7':'19', '63':'20'}
    depth = 3
    # initialize COCO api.
    coco = COCO(annofile)

    if not os.path.exists(imgsetfile):
        print "{} does not exist".format(imgsetfile)
        sys.exit()

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # Read image info.
    imgs = dict()
    img_ids = coco.getImgIds()
    for img_id in img_ids:
        # get image info
        img = coco.loadImgs(img_id)[0]
        file_name = img["file_name"]
        name = os.path.splitext(file_name)[0]
        xml_path = "{}/{}.xml".format(out_dir, name)
        imgs[name] = img
        if out_dir:
            #get annotation info
            anno_ids = coco.getAnnIds(imgIds=img_id, iscrowd=None)
            anno = coco.loadAnns(anno_ids)
            for ann in anns:
                cat_id = ann['category_id']
                bbox = ann['bbox']
                # Save information to xml
                result = XmlWriter(xml_path, seleted_map[img["id"]],
                        (img["height"], img["width"], depth))
                result.addBndBox(bbox[0], bbox[1], bbox[2], bbox[3], cat_id)
                result.save()
