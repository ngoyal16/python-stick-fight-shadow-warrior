import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import time

vertices = np.array([[0,310],[0,280],[720,280],[720,310]])

def roi(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	masked= cv2.bitwise_and(img, mask)
	return masked
    
	
def click_left():
	print("clicking left")
	pyautogui.click(300, 400)
	
	
def click_right():
	print("clicking right")
	pyautogui.click(500, 400)
	

def find_target(original_img):
	global vertices
	img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
	img = roi(img, [vertices])
	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,1,param1=200, param2=13, minRadius=0, maxRadius=10)
	try:
		x = np.array([])
		for i in circles[0,:]:
			if i[0] > 265 and i[0] < 435 and i[1] > 285 and i[1] < 295:
				x = np.append(x, i[0])
		if len(x):
			index = (np.abs(x-325)).argmin()
			if x[index] > 325:
				click_right()
			else:
				click_left()
				
			print(x)
			if len(x) < 3:
				time.sleep(0.165)
			else:
				time.sleep(0.130)
	except Exception as e:
		pass
	
def process_img(original_img):
	global vertices
	processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
	# processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	processed_img = roi(processed_img, [vertices])
	result = np.zeros_like(original_img)
	circles = cv2.HoughCircles(processed_img, cv2.HOUGH_GRADIENT,1,1,param1=200, param2=13, minRadius=0, maxRadius=10)
	print(circles)
	try:
		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			cv2.circle(result,(i[0],i[1]), i[2],(0,255,0), thickness=-1)
	except:
		pass
	return result

count = 0
time.sleep(1)
click_left()
while(True):
	screen = np.array(ImageGrab.grab(bbox=(70, 90, 720, 480)))
	find_target(screen)
	count = count + 1
	print(count)
	# new_screen = process_img(screen)
    # cv2.imshow('window', new_screen)
    # cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    # if cv2.waitKey(25) & 0xFF == ord('q'):
        # cv2.destroyAllWindows()
	if count >500:
		break
