import os
import cv2
import random
from random import shuffle
import argparse
import pathlib

random.seed(12345)

def write_to_file(list_link, output_file):
    with open(output_file, "w") as f:
        for key, links in list_link.items():
            for link in links:
                f.write("{}\t{}\n".format(link, label[key]))


parser = argparse.ArgumentParser()
parser.add_argument("--root_folder", default="/home/tanlm/Downloads/adult_detection/input_image",
                    type=str, help="folder include yes and no")
parser.add_argument("--save_folder", default="/home/tanlm/Downloads/adult_detection/text_label",
                    type=str, help='folder to save train.txt and validation.txt')
args = parser.parse_args()


data_links = {"YES": [], "NO": []}
label = {"YES": 1, "NO": 0}

root_folder = args.root_folder
save_folder = args.save_folder
cannot_read = 0
for sub_folder in os.listdir(root_folder):
    for image_name in pathlib.Path(os.path.join(root_folder, sub_folder)).rglob('*'):
        if not image_name.is_file():
            continue
        img_link = str(image_name.absolute())
        img = cv2.imread(img_link)
        if img is None:
            cannot_read += 1
            print("{} - Opencv can not read:".format(cannot_read))
            print(img_link[len(root_folder) + 1:])
            continue
        data_links[sub_folder].append(img_link[len(root_folder) + 1:])


for key, list_link in data_links.items():
    shuffle(list_link)
    data_links[key] = list_link


data_links_train = {}
data_links_val = {}
data_links_test = {}
percent_each_set = [0.6, 0.8]


for key, list_link in data_links.items():
    index_split = list(map(lambda x: int(x * len(list_link)), percent_each_set))
    train = list_link[0: index_split[0]]
    vali = list_link[index_split[0]: index_split[1]]
    test = list_link[index_split[1]: ]
    data_links_train[key] = train
    data_links_val[key] = vali
    data_links_test[key] = test

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

write_to_file(data_links_train, os.path.join(save_folder, 'train.txt'))
write_to_file(data_links_val, os.path.join(save_folder, 'val.txt'))
write_to_file(data_links_test, os.path.join(save_folder, 'test.txt'))
