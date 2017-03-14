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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Get the image size from an annotation file.")
    parser.add_argument("annofile",
            help = "The file which contains all the annotations for a dataset in json format.")
    parser.add_argument("imgsetfile", default = "",
            help = "A file which contains the image set information.")
    parser.add_argument("namesizefile", default = "",
            help = "A file which stores the name size information.")

    args = parser.parse_args()
    annofile = args.annofile
    imgsetfile = args.imgsetfile
    namesizefile = args.namesizefile

    seleted_map = {'5':'1', '2':'2', '15':'3', '9':'4', '40':'5', '6':'6', '3':'7', '16':'8',
            '57':'9', '20':'10', '61':'11', '17':'12', '18':'13', '4':'14', '1':'15', '59':'16',
            '19':'17', '58':'18', '7':'19', '63':'20'}
    # initialize COCO api.
    coco = COCO(annofile)

    if namesizefile:
        if not os.path.exists(imgsetfile):
            print "{} does not exist".format(imgsetfile)
            sys.exit()

        name_size_dir = os.path.dirname(namesizefile)
        if not os.path.exists(name_size_dir):
            os.makedirs(name_size_dir)
        # Read image info.
        imgs = dict()
        img_ids = coco.getImgIds()
        for img_id in img_ids:
            # get image info
            img = coco.loadImgs(img_id)[0]
            file_name = img["file_name"]
            name = os.path.splitext(file_name)[0]
            imgs[name] = img

        # Save name size information.
        with open(namesizefile, "w") as nf:
            with open(imgsetfile, "r") as sf:
                for line in sf.readlines():
                    name = line.strip("\n")
                    img = imgs[name]
                    nf.write("{} {} {}\n".format(img["id"], img["height"], img["width"]))
