set -e

export PYTHONPATH=.:$PYTHONPATH

VALIDATION_DATA="/var/data/adult-data/text_label/test.txt"
ROOT_FOLDER="/var/data/adult-data/input_image"
RESUME=""
PREDICT_RESULT="/var/data/output/predict_result.txt"

python inference_images.py --validation_data $VALIDATION_DATA \
                           --root_folder $ROOT_FOLDER \
                           --resume $RESUME \
                           --predict_result $PREDICT_RESULT


