import numpy as np
import cv2

def roi(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	masked= cv2.bitwise_and(img, mask)
	return masked

def process_img(original_img):
	processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
	processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	vertices = np.array([[0,530],[0,580],[1280,580],[1280,530]])
	processed_img = roi(processed_img, [vertices])
	# result = np.zeros_like(original_img)
	circles = cv2.HoughCircles(processed_img, cv2.HOUGH_GRADIENT,1,1,param1=200, param2=10, minRadius=0, maxRadius=10)
	print(circles)
	try:
		# circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			cv2.circle(processed_img,(i[0],i[1]), i[2],(255,255,255), thickness=-1)
			# cv2.circle(result,(i[0],i[1]), i[2],(255,255,255), thickness=-1)
	except:
		pass
	return processed_img

img = cv2.imread('stick.jpg')
cv2.imshow('window', process_img(img))
if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows()