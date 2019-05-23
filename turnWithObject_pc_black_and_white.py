#code for turn
import cv2 
import numpy as np
from time import sleep




cap = cv2.VideoCapture(0)

while True:

	ret,frame=cap.read()

	totalCrop=frame[0:720 ,0:600]

	cv2.imshow('frame',totalCrop)
	
	# Convert to grayscale
	gray = cv2.cvtColor(totalCrop, cv2.COLOR_BGR2GRAY)
	
	# Gaussian blur
	blur = cv2.GaussianBlur(gray,(3,3),0)
	
	# Color thresholding
	ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)#60
	
	# Find the contours of the frame
	cv2.imshow('thresh_line',thresh)
	im2,contours,hierarchy = cv2.findContours(thresh.copy(),1,cv2.CHAIN_APPROX_NONE)  #creates outerline of contour


	if len(contours) > 0:
		c = max(contours, key=cv2.contourArea)
		M = cv2.moments(c)
		#formula for centroid of contour
		if M['m00']!=0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
		else:
			cx = int(M['m10']/1)
			cy = int(M['m01']/1)
		print("")
		print("Cx= ",cx)
		print("Cy= ",cy)
		cimg=np.zeros((512,512,3),np.uint8)
		cimg1=cimg[0:720 ,0:600]
		cv2.circle(cimg1,(cx,cy),10,(0,255,0),-1)
		cv2.line(cimg1,(150,0),(150,720),(255,255,255),5)
		cv2.line(cimg1,(450,0),(450,720),(255,255,255),5)
		
		cv2.imshow('centroid',cimg)
		if cx >= 450:
			print("Turn right!")
			#GPIO.OUTPUT(left,GPIO.LOW)
			#GPIO.OUTPUT(right,GPIO.HIGH)
		if cx < 450 and cx > 150:
			print("On Track!")
			#GPIO.OUTPUT(left,GPIO.HIGH)
			#GPIO.OUTPUT(right,GPIO.HIGH)
		if cx <= 150:
			print("Turn left")
			#GPIO.OUTPUT(left,GPIO.HIGH)
			#GPIO.OUTPUT(right,GPIO.LOW)
	else:
		print("I don't see the line")
		#GPIO.OUTPUT(left,GPIO.HIGH)
		#GPIO.OUTPUT(right,GPIO.LOW)

    
	if cv2.waitKey(1) == 27:
		break

cap.release()   
cv2.destroyAllWindows()