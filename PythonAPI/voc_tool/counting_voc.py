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
coco_data_dir = "/data/coco"
# The sets that we want to get the size info.
anno_sets = ["instances_val2014","instances_train2014"]
data_types = ["val", "train"]
#anno_sets = ["image_info_test-dev2015", "instances_val2014", "image_info_test2014",
#        "image_info_test2015", "instances_train2014"]
#anno_sets = anno_sets + ["instances_minival2014", "instances_valminusminival2014"]
# The directory which contains the full annotation files for each set.
anno_dir = "{}/annotations".format(coco_data_dir)
# The directory which stores the imageset information for each set.
imgset_dir = "{}/ImageSets".format(coco_data_dir)
# The directory which stores the image id and size info.
#out_dir = "{}/data/coco".format(CAFFE_ROOT)
anno_out_dir = "/data/MixedData/Annotations"
img_out_dir = "/data/MixedData/ImageSets"
if not os.path.exists(anno_out_dir):
    os.makedirs(anno_out_dir)

### Get image size info ###
for i in xrange(0, len(anno_sets)):
    anno_set = anno_sets[i]
    data_type = data_types[i]
    anno_file = "{}/{}.json".format(anno_dir, anno_set)
    if not os.path.exists(anno_file):
        continue
    anno_name = anno_set.split("_")[-1]
    imgset_file = "{}/{}.txt".format(imgset_dir, anno_name)
    if not os.path.exists(imgset_file):
        print "{} does not exist".format(imgset_file)
        sys.exit()
    #name_size_file = "{}/{}_name_size.txt".format(out_dir, anno_name)
    if redo or not os.path.exists(anno_out_dir):
        cmd = "python {}/json2xml_coco.py {} {} {} {} {}" \
                .format(CURDIR, anno_file, imgset_file, data_type, anno_out_dir, img_out_dir)
                #all.json train/val.txt output_dir
        print cmd
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
