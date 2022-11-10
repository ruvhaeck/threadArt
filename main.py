import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import error
import vis

matplotlib.use('TkAgg')

file = "lena"
thickness = 1  # meaning the line on the image will be 'thickness' pixels wide
nails = 200
shape = 'rectangle'
iterations = 100
boek = []  # keys = (row/height, column/width), value = index 0-nails-1
nailMatrix = np.zeros((nails, nails), bool)  # triangular matrix, only use upper half

def fill_boek(nails, shape, boek, width, height):
	if shape == 'rectangle':
		omtrek = 2 * width + 2 * height - 4
		space = omtrek // nails
		sum = 0
		for i in range(nails):  # yes, not perfect, first draft
			if sum < width:
				boek.append((0, sum))
			elif sum < width + height - 1:
				boek.append((sum - width, width - 1))
			elif sum < 2 * width + height - 1:
				boek.append((height - 1, sum - width - height + 1))
			else:
				boek.append((sum - 2 * width - height + 2, 0))
			sum += space
	return boek, space


def runningThread(pos, boek, canvas, img):
	for i in range(len(boek)):
		if boek[i] == pos:
			posIndex = i

	# find the best line
	maxError = 0.
	maxPos = ()
	maxIndex = 0
	for index, otherPos in enumerate(boek):
		if otherPos[0] >= imgWidth or otherPos[1] >= imgHeight:
			print("wrong")
		if otherPos == pos or nailMatrix[min(posIndex, index), max(posIndex, index)] or otherPos[0] == pos[0] or \
				otherPos[1] == pos[1]:
			# not the following cases:
			# to itself
			# to already connected nails
			# at the edge of the picture
			continue
		else:
			newImg = np.copy(canvas)
			black = np.zeros(canvas.shape)
			newImg = cv2.line(newImg, pos, otherPos, color=(100, 100, 100),
							  thickness=thickness)  # line both overwrites and output the result!
			black = cv2.line(black, pos, otherPos, color=(1, 1, 1), thickness=thickness + 5)
			error_ = error.MAE(newImg, img, black)
			# error = MSE(newImg, img)
			if error_ < 0:
				raise OverflowError()
			if error_ >= maxError:
				maxError = error_
				maxPos = otherPos
				maxIndex = index
	# draw it on the image
	canvasOld = np.copy(canvas)
	if pos == () or maxPos == ():
		return canvas, maxError, maxPos, 1
		raise ArithmeticError("maxPos or pos is () (probably all possibilities are up)")
	canvas = cv2.line(canvas, pos, maxPos, color=(0, 0, 0), thickness=thickness)
	# canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
	nailMatrix[min(posIndex, maxIndex), max(posIndex, maxIndex)] = 1
	return canvas, maxError, maxPos, 0


img = cv2.imread(file + ".png", cv2.IMREAD_GRAYSCALE)  # range: 0 - 255
imgHeight, imgWidth = img.shape

# make the canvas
canvas = np.ones(img.shape, dtype=np.uint8)
canvas = canvas * 255  # we start with a white background
boek, space = fill_boek(nails, shape, boek, imgWidth, imgHeight)
pos = (0, 0)
errorList = []
totalErrorList = []
indexList = [pos]
# need to check that the iterations is not more than all the combinations possible
fact = np.math.factorial
nWidth = imgWidth // space + 1
nHeigth = imgHeight // space + 1
if iterations > (
		fact(nails) / (fact(nails - 2) * 2) - fact(nWidth) / fact(nWidth - 2) - fact(nHeigth) / fact(nHeigth - 2)):
	raise ValueError(
		"to much iterations for the number of nails, either increase the number of nail or decrease the number of iterations")

v = vis.Vis(img)
iter = 0
while True:
	if not v.iterating:
		cv2.imwrite(file + "_canvas.png", canvas)
	while v.iterating:
		canvas, maxError, pos, end = runningThread(pos, boek, canvas, img)
		errorList.append(maxError)
		indexList.append(pos)
		totalErrorList.append(error.MSE(canvas, img))
		if iter % 10 == 0:
			v.update(canvas, errorList, totalErrorList)
		iter += 1
	v.capture()  # needed because otherwise '2' is not captured

