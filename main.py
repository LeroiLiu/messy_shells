import cv2
import numpy as np

def aoiGravityCenter(thresh):
	M=cv2.moments(thresh)
	# print(M)
	# return (1,1)
	if M['m00']==0:
		return False
	cx=int(M['m10']/M['m00'])
	cy=int(M['m01']/M['m00'])
	return (cx,cy)

def biggerSort(cnt1,cnt2):
	if cv2.contourArea(cnt1)>cv2.contourArea(cnt2):
		return True
	return False

# VideoCapture cap("http://192.168.1.1:8080/?action=stream"); 
# capture the video from web cam  
cap = cv2.VideoCapture(0)
# set the Resolution
cap.set(3,640)
cap.set(4,480)

if not cap.isOpened():
	print("Cannot open the web cam")

iLowH = 23;
iHighH = 51;

iLowS = 80;
iHighS = 255;

iLowV = 30;
iHighV = 255;

# target_img   = cv2.imread("target.png")
# gray_img     = cv2.cvtColor(target_img,cv2.COLOR_BGR2GRAY)
# target_img   = cv2.threshold(gray_img, 60, 255, cv2.THRESH_BINARY)
# contours_tar = cv2.findContours(target_img,cv2.CV_RETR_EXTERNAL,cv2.CV_CHAIN_APPROX_NONE)

while (True):
	imgOriginal = np.zeros((320,240,3),np.uint8)
	ret , imgOriginal = cap.read()

	imgHSV = cv2.cvtColor(imgOriginal,cv2.COLOR_BGR2HSV)
	(r,g,b) = cv2.split(imgHSV)
	b = cv2.equalizeHist(b)
	imgHSV = cv2.merge((r,g,b))

	imgThresholded = cv2.inRange(imgHSV, np.array([iLowH, iLowS, iLowV]), np.array([iHighH, iHighS, iHighV]))

	element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

	imgThresholded = cv2.morphologyEx(imgThresholded,cv2.MORPH_OPEN,element)
	imgThresholded = cv2.morphologyEx(imgThresholded,cv2.MORPH_CLOSE,element)

	gravity = aoiGravityCenter(imgThresholded)
	if gravity:
		rows,cols = imgThresholded.shape
		rows = rows/2
		cols = cols/2
		cv2.line(imgOriginal,gravity,(cols,rows),np.array([0,0,255]),5)
		cv2.circle(imgOriginal,gravity,40,np.array([0,0,255]),2)

	cv2.imshow('imgOriginal',imgOriginal)
	if cv2.waitKey(100) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()	
