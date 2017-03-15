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

    seleted_map = {5:1, 2:2, 15:3, 9:4, 40:5, 6:6, 3:7, 16:8,
            57:9, 20:10, 61:11, 17:12, 18:13, 4:14, 1:15, 59:16,
            19:17, 58:18, 7:19, 63:20}
    depth = 3
    #data_dir = "/data/coco"
    #Imageset_dir = "ImageSets"
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
            result = XmlWriter("coco", name,
                (int(img["height"]), int(img["width"]), depth))
            for ann in anns:
                #print ann
                cat_id = ann['category_id']
                if cat_id not in seleted_map.keys():
                    continue
                bbox = ann['bbox']
                #print "cat_id is " + str(cat_id)
                #print seleted_map[cat_id]
                # Save information to xml
                # XmlWriter(id_name, file_name, (height, width, depth))
                result.addBndBox(bbox[0], bbox[1], bbox[2], bbox[3], seleted_map[cat_id])
                result.save(xml_path)

            src = "{}/{}".format(dirname, file_name)
            dst_dir = "{}/{}".format(img_out_dir, data_type)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            dst_path = "{}/{}".format(dst_dir, file_name)
            shutil.copy(src, dst_path)
