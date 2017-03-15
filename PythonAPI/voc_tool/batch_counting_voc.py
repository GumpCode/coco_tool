import os
import subprocess
import sys

HOMEDIR = os.path.expanduser("~")
CURDIR = os.path.dirname(os.path.realpath(__file__))

### Modify the address and parameters accordingly ###
# If true, redo the whole thing.
redo = True
# The caffe root.
CAFFE_ROOT = "{}/GumpCode/ssd".format(HOMEDIR)
# The root directory which stores the coco images, annotations, etc.
voc_data_dir = "/home/ganlinhao/voc/VOCdevkit"
# The sets that we want to get the size info.
anno_sets = ["VOC2007","VOC2012"]
data_types = ["val", "train"]
# The directory which stores the image id and size info.
anno_out_dir = "/data/MixedData/Annotations"
img_out_dir = "/data/MixedData/ImageSets"
if not os.path.exists(anno_out_dir):
    os.makedirs(anno_out_dir)

### Get image size info ###
for i in xrange(0, len(anno_sets)):
    anno_set = anno_sets[i]
    # The directory which contains the full annotation files for each set.
    anno_dir = "{}/{}/Annotations".format(voc_data_dir, anno_set)
    # The directory which contains the full jpeg imgages for each set.
    jpeg_dir = "{}/{}/JPEGImages".format(voc_data_dir, anno_set)
    # The directory which stores the imageset information for each set.
    imgset_dir = "{}/ImageSets/Main".format(voc_data_dir)
    for j in range(len(data_types)):
        data_type = data_types[i]
        imagset_file = "{}/{}.txt".format(anno_dir, data_type)
        if not os.path.exists(anno_file):
            continue
        #anno_name = anno_set.split("_")[-1]
        #imgset_file = "{}/{}.txt".format(imgset_dir, anno_name)
        if not os.path.exists(imgset_file):
            print "{} does not exist".format(imgset_file)
            sys.exit()
        #name_size_file = "{}/{}_name_size.txt".format(out_dir, anno_name)
        if redo or not os.path.exists(anno_out_dir):
            cmd = "python {}/counting_voc.py {} {} {} {} {}" \
                    .format(CURDIR, anno_dir, imgset_file, data_type, anno_out_dir, img_out_dir)
            print cmd
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            print output
