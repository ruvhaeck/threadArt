import cv2
import numpy as np
from matplotlib import pyplot as plt
import error


class Vis:
	def __init__(self, img):
		self.iterating = True
		self.iterations = 0
		plt.ion()
		self.fig, self.ax = plt.subplots(2, 2)
		self.ax[0, 0].imshow(img, cmap='gray', vmin=0, vmax=255)
		self.ax[0, 0].set(title="original")
		#self.ax[0, 1].imshow(self.canvas, cmap='gray', vmin=0, vmax=255)  # canvas
		self.ax[0, 1].set(title="result")
		self.ax[1, 0].plot()
		self.ax[1, 0].set(title="total error", xlabel="iterations", ylabel="total error")
		self.ax[1, 1].plot()
		self.ax[1, 1].set(title="error for drawing line", xlabel="iterations", ylabel="error")

		self.fig.canvas.mpl_connect('key_press_event', self.onKey)

	def onKey(self, event):
		if event.key == 'q':
			exit(0)
		elif event.key == '1':
			print("stop the iterating and writing image")
			self.iterating = False
		elif event.key == '2':
			print('resume iterating')
			self.iterating = True

	def update(self, canvas, errorList, totalErrorList):
		self.ax[1, 0].clear()  # inefficient
		self.ax[1, 0].plot(totalErrorList)
		self.ax[1, 1].clear()
		self.ax[1, 1].plot(errorList)
		self.ax[0, 1].clear()  # inefficient
		self.ax[0, 1].imshow(canvas, cmap='gray', vmin=0, vmax=255)
		self.fig.canvas.flush_events()

	def capture(self):
		self.fig.canvas.flush_events()

