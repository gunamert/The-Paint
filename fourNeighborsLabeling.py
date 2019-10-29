import PIL.Image

def fourConnectedLabeling (img):
	targetImage = img
	pix =targetImage.load()
	rowSize,columnSize=targetImage.size
	pixelValues=[[ 0 for x in range(columnSize)] for y in range(rowSize)]

	for i in range(rowSize):
		for j in range(columnSize):
			pixelValues[i][j]=pix[i,j]

	for i in range (rowSize):
		for j in range (columnSize):
			if i == 0 or j == 0 or i == rowSize-1 or j == columnSize-1:
				pixelValues[i][j]=0

	labelValues=[[ 0 for x in range (columnSize)] for y in range(rowSize)]
	for i in range (rowSize):
		for j in range (columnSize):
			labelValues[i][j]=0

	labelCounter=2
	for i in range (1,rowSize-1):
		for j in range (1,columnSize-1):
			if pixelValues[i][j]==1:
				if pixelValues[i-1][j]==1 and pixelValues[i][j-1]==1:
					if labelValues[i-1][j]==labelValues[i][j-1]:
						labelValues[i][j]=labelValues[i][j-1]
					else:
						labelValues[i][j]=labelValues[i-1][j]
						for t in range(0,i+1):
							for k in range (0,j+1):
								if labelValues[t][k]==labelValues[i][j-1]:
									labelValues[t][k]=labelValues[i-1][j]
				elif  pixelValues[i-1][j]==1 or pixelValues[i][j-1]==1:
					if pixelValues[i-1][j]==1:
						labelValues[i][j]=labelValues[i-1][j]
					else:
						labelValues[i][j]=labelValues[i][j-1]
				else:
					labelValues[i][j]=labelCounter
					labelCounter+=1
			else:
				labelValues[i][j]=1

	for j in range (columnSize):
		for i in range (rowSize):
			pix[i,j] = labelValues[i][j]

	colors = {}
	output_img = PIL.Image.new("RGB", (columnSize, rowSize))
	outdata = output_img.load()

	for i in range(rowSize):
		for j in range(columnSize):

			component = labelValues[i][j]

			if component not in colors:
				if component is not 1:
					colors[component] = (255, 255, 255)
				else:
					colors[component] = (0, 0, 0)

			outdata[i, j] = colors[component]

	return labelValues,output_img

def converToBinaryValue(rgbValues):
	if rgbValues == 255 :
		return 1
	return 0