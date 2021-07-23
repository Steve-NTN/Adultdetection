import io
import torch 
import torch.nn as nn 
import numpy as np
import torchvision.transforms as transforms 
from PIL import Image
from torchvision import datasets, models, transforms
import settings
import redis
import time
import base64
import json
from encode_image import base64_decode_image

# Connect to Redis server
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

class_index_name = {0: "is not adult image", 1: "is adult image"}

# Init model and return model
def get_model():
    model = models.resnet50(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    checkpoint = torch.load("model_best.pth", map_location=torch.device('cpu'))
    state_dict = checkpoint['state_dict']
    model.load_state_dict(state_dict)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    return model

# Get tensor from image bytes
def get_tensor(image_byte):
	validation_transform = transforms.Compose(
        [transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

	image = Image.open(io.BytesIO(image_byte))
	return validation_transform(image).unsqueeze(0)

# Get class index and name with image byte input
def get_label(model, image_bytes):
	image_tensor = get_tensor(image_bytes)
	output = model(image_tensor)
	_, predict = output.max(1)
	class_index = predict.item()
	class_name = class_index_name[class_index]
	return class_index, class_name

def classify_process():
	print("* Loading model...")
	model = get_model()
	print("* Model loaded")

	while True:
		# attempt to grab a batch of images from the database, then
		# initialize the image IDs and batch of images themselves
		queue = db.lrange(settings.IMAGE_QUEUE, 0,
			settings.BATCH_SIZE - 1)
		imageIDs = []
		batch = None
		
		# loop over the queue
		for q in queue:
			# deserialize the object and obtain the input image
			q = json.loads(q.decode("utf-8"))
			image = base64_decode_image(q["image"],
				(1, settings.IMAGE_CHANS, settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH),
				settings.IMAGE_DTYPE)

			# check to see if the batch list is None
			if batch is None:
				batch = image
			else:
				batch = np.vstack((batch, image))
			imageIDs.append(q["id"])

		# check to see if we need to process the batch
		if len(imageIDs) > 0:
			# classify the batch
			print("* Batch size: {}".format(batch.shape))
			
			# get class label 
			results = model.forward(batch)
			_, predict = torch.max(results, dim=1)
			
			# loop over the image IDs and their corresponding set of
			# results from our model
			for (imageID, resultSet) in zip(imageIDs, predict.tolist()):
				output = []
				output.append({"index": resultSet, "name": class_index_name[resultSet]})

				# store the output predictions in the database, using
				# the image ID as the key so we can fetch the results
				db.set(imageID, json.dumps(output))

			# remove the set of images from our queue
			db.ltrim(settings.IMAGE_QUEUE, len(imageIDs), -1)

		# sleep for a small amount
		time.sleep(settings.SERVER_SLEEP)

# if this is the main thread of execution start the model server
# process
if __name__ == "__main__":
	classify_process()