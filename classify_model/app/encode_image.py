# import the necessary packages
import numpy as np
from PIL import Image
import io
import base64
import sys
import torch
import torchvision.transforms as transforms 

def base64_encode_image(tensor_image):
	# base64 encode the input tensor
	return base64.b64encode(tensor_image).decode("utf-8")

def base64_decode_image(str_image, shape, dtype):
	# if this is Python 3, we need the extra step of encoding the
	# serialized NumPy string as a byte object
	if sys.version_info.major == 3:
		str_image = bytes(str_image, encoding="utf-8")

	# transform image to tensor
	validation_transform = transforms.Compose(
        [transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
	
	# read string image and convert to tensor
	np_image = np.frombuffer(base64.decodestring(str_image), dtype=dtype)
	np_image = np_image.reshape(shape)
	tensor_image = torch.from_numpy(np_image[0])

	# transform resized image to tensor
	tensor_image = transforms.ToPILImage()(tensor_image)
	tensor_image = validation_transform(tensor_image).unsqueeze(0)
	# return the decoded image
	return tensor_image

def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")
	
	# resize the input image and preprocess it
	image = image.resize(target)
	imgt = transforms.ToTensor()(image)
	image = np.expand_dims(imgt.numpy(), axis=0)

	# return the processed image
	return image