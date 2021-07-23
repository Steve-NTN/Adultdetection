set -e

export PYTHONPATH=.:$PYTHONPATH

ROOT_FOLDER="/var/data/adult-data/input_image"
SAVE_FOLDER="/var/data/adult-data/image_label_split"

python data_preprocess/split_data.py --root_folder $ROOT_FOLDER --save_folder $SAVE_FOLDER