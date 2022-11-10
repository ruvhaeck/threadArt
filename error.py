import numpy as np


def MSE(canvas, img):
	return np.sum(np.square(canvas - img))


def MAE(canvas, img, black):
	return np.sum(np.abs(canvas * black - img * black)) / np.sum(black)
