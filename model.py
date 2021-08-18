import torch

import os
import numpy as np


class Model:
    def __init__(self, name):
        self.model = torch.load(name)
        self.image = list()

    def image_preprocessing(self):
        image = self.image.resize((55, 55))
        x = np.array(image).reshape((1, 55, 55))
        return x

    def get_result(self, image):
        self.image = image.copy()
        inp = self.image_preprocessing()
        out = self.model(inp).argmax(dim=1)
        return out
