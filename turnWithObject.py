#code for turn
import cv2 as cv
import numpy as np
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
#import RPi.GPIO as GPIO




def red_color_detect(crop_img):
    hsv = cv.cvtColor(crop_img, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)

    mask = mask0 + mask1

    # Bitwise-AND mask and original image
    output = cv.bitwise_and(crop_img, crop_img, mask=mask)

    gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv.GaussianBlur(gray, (3, 3), 0)

    # Color thresholding
    ret, thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY)  # 60
    #cv.imshow('thresh_red', thresh)

    # Find the contours of the frame
    contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)# creates outerline of contour

    if(len(contours)>0):
        return 1
    else:
        return 0


def blue_color_detect(crop_img):
    boundries_blue = [
        ([86, 31, 4], [220, 88, 50])
    ]

    # Convert BGR to HSV
    hsv = cv.cvtColor(crop_img, cv.COLOR_BGR2HSV)

    for (lower, upper) in boundries_blue:
        lower_blue = np.array(lower, dtype="uint8")
        upper_blue = np.array(upper, dtype="uint8")

        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        output = cv.bitwise_and(crop_img, crop_img, mask=mask)

    gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv.GaussianBlur(gray, (3, 3), 0)

    # Color thresholding
    ret, thresh1 = cv.threshold(blur, 60, 255, cv.THRESH_BINARY)  # 60

    # Find the contours of the frame
    contours, hierarchy = cv.findContours(thresh1.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)# creates outerline of contour

    if(len(contours)>0):
        return 1
    else:
        return 0




def contour(img):
    #boundries_white = [([211, 237, 235], [255, 255, 255])]	#boundries of color detected

    boundries_black = [([0, 0, 0], [55, 55, 55])]

    #for (lower, upper) in boundries_white:
    for (lower, upper) in boundries_black:
		# create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
        mask = cv.inRange(img, lower, upper)
        output = cv.bitwise_and(img, img, mask = mask)

    #Convert to grayscale
    gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)

	# Gaussian blur
    blur = cv.GaussianBlur(gray,(5,5),0)
	
	# Color thresholding
    ret, thresh = cv.threshold(blur,60,255,cv.THRESH_BINARY)  #60


    contours, h=cv.findContours(thresh.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)


    if(len(contours)>0):
        return 1, thresh
    else:
        return 0, thresh


def edgeDetect(img):

    blue=blue_color_detect(img)
    red=red_color_detect(img)
    
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    edges=cv.Canny(gray,100,200)

    cv.imshow('edges',edges)

    line=edgeContour(edges)  

    
    
    if line and not (blue or red):
        return 1
    else:
        return 0


def edgeLineDetect(img):
    copyImg = img.copy()

    blue=blue_color_detect(img)
    red=red_color_detect(img)

    line,im=contour(copyImg)
    edge=edgeDetect(copyImg)

    if line==1 and edge==1 and not (blue or red):
        return 1
    else:
        return 0

def edgeContour(img):

    contours,h=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)

    if len(contours)>0:
        return 1
    else:
        return 0


camera = PiCamera()
camera.resolution=(800,608)
camera.framerate=30
rawCapture=PiRGBArray(camera,size=(800,608))



for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    
    totalCrop=frame.array
    #cv.imshow('frame',totalCrop)
    imgf1=0
    imgf2=0
    imgf3=0
    imgf4=0
    imgf5=0
    imgf6=0
    imgf7=0
    imgf8=0
    imgf9=0

    o1=totalCrop[0:200,0:100]
    o2=totalCrop[0:200,100:500]
    o3=totalCrop[0:200,500:600]

    
    grid1=totalCrop[200:400,0:200]
    grid4=totalCrop[400:600,0:200]
    grid7=totalCrop[600:800,0:200]
    grid2=totalCrop[200:400,200:400]
    grid5=totalCrop[400:600,200:400]
    grid8=totalCrop[600:800,200:400]
    grid3=totalCrop[200:400,400:600]
    grid6=totalCrop[400:600,400:600]
    grid9=totalCrop[600:800,400:600]
    
    '''
    cv.imshow('grid1',grid1)
    cv.imshow('grid2',grid2)
    cv.imshow('grid3',grid3)
    cv.imshow('grid4',grid4)
    cv.imshow('grid5',grid5)
    cv.imshow('grid6',grid6)
    cv.imshow('grid7',grid7)
    cv.imshow('grid8',grid8)
    cv.imshow('grid9',grid9)
    '''
    cv.imshow('o1',o1)
    cv.imshow('o2',o2)
    cv.imshow('o3',o3)

    imgf1,h1 = contour(grid1)
    imgf2,h2 = contour(grid2)
    imgf3,h3 = contour(grid3)
    imgf4,h4 = contour(grid4)
    imgf5,h5 = contour(grid5)
    imgf6,h6 = contour(grid6)
    imgf7,h7 = contour(grid7)
    imgf8,h8 = contour(grid8)
    imgf9,h9 = contour(grid9)

    object1 = edgeDetect(o1)
    object2 = edgeLineDetect(o2)
    object3 = edgeDetect(o3)

    #print(type(object1),type(object2),type(object3))

    
    print("o1",object1,'o2',object2,'o3',object3)

    
    '''cv.imshow('h1', h1)
    cv.imshow('h2', h2)
    cv.imshow('h3', h3)
    cv.imshow('h4', h4)
    cv.imshow('h5', h5)
    cv.imshow('h6', h6)
    cv.imshow('h7', h7)
    cv.imshow('h8', h8)
    cv.imshow('h9', h9)'''

    #cv.imshow('grid5',grid5)
    #cv.imshow('thresh5',h5)


##################################################################
    # blue7=blue_color_detect(grid7)
    # blue9=blue_color_detect(grid9)

    # red7=red_color_detect(grid7)
    # red9=red_color_detect(grid9)
##################################################################
    
    
    #if(blue7 or blue9):
        #print("I got blue")

##################################################################
    # if imgf8:
    #     if ((imgf2 and imgf4 and imgf5 and imgf6) and (blue7 and blue9) or (red7 and red9)) :
    #         print("cross")
    #     elif imgf2 and imgf5:
    #         print("straight")
    #     elif imgf1:
    #         print("left")
    #     elif imgf3:
    #         print('right')
    # elif imgf1 or imgf4 or imgf7:
    #     print("Left Balance")
    # elif imgf3 or imgf6 or imgf9:
    #     print("Right Balance")
    # elif ((not imgf1) and (not imgf2) and (not imgf3) and (not imgf4) and (not imgf5) and (not imgf6) and (not imgf7) and (not imgf8) and (not imgf9)):
    #     print("There ain't no line bitch")


    # if object1 and object2 and object3:
    #     print("Object Detected")
################################################################


#Conditions for Black and white Background
    if imgf8:
            if ((imgf2 and imgf4 and imgf5 and imgf6) :
                print("cross")
            elif imgf2 and imgf5:
                print("straight")
            elif imgf1:
                print("left")
            elif imgf3:
                print('right')
    
    elif imgf1 or imgf4 or imgf7:
        print("Left Balance")
    elif imgf3 or imgf6 or imgf9:
        print("Right Balance")
    elif ((not imgf1) and (not imgf2) and (not imgf3) and (not imgf4) and (not imgf5) and (not imgf6) and (not imgf7) and (not imgf8) and (not imgf9)):
        print("There ain't no line bitch")


    if object1 and object2 and object3:
        print("Object Detected")

    
    if cv.waitKey(1) == 27:
        break
    rawCapture.truncate(0)
    
cv.destroyAllWindows()
