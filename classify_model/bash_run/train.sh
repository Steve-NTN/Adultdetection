set -e

export PYTHONPATH=.:$PYTHONPATH

TRAIN_DATA="/var/data/adult-data/text_label/train.txt"
VALIDATION_DATA="/var/data/adult-data/text_label/val.txt"
ROOT_FOLDER="/var/data/adult-data/input_image"
TRAINER_SAVE_DIR="/var/data/adult-data/save"
EXPERIMENT_NAME="exp1"

python train.py --train_data $TRAIN_DATA \
                --validation_data $VALIDATION_DATA \
                --root_folder $ROOT_FOLDER \
                --trainer_save_dir $TRAINER_SAVE_DIR \
                --exper_name $EXPERIMENT_NAME


