import torchvision.transforms as transforms
from torch.utils import data
from PIL import Image
import cv2
import numpy as np
from dataloaders.utils import get_imgs_labels


class AdultImageLoader(data.Dataset):
    def __init__(self, link_label_file, image_size, root_folder, transforms=None):
        super(AdultImageLoader, self).__init__()
        self.labels = []
        self.images, self.labels, self.image_links = get_imgs_labels(link_label_file, image_size, root_folder)
        self.transform = transforms

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        img = self.images[index]
        label = self.labels[index]
        img = Image.fromarray(np.uint8(img[:, :, ::-1]))
        if self.transform is not None:
            img = self.transform(img)
        return img, label