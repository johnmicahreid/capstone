import cv2
import numpy as np

cv2.namedWindow("preview")

frame = cv2.imread("Photo\ on\ 6-2-17\ at\ 5.14\ PM.jpg", 1)
print("read image, dimensions are", frame.shape)
cv2.imshow("preview", frame)

#image = frame.array

# Process the image

# First, transform to greyscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Apply a Canny filter to pick out edges
edged = cv2.Canny(gray, 50, 200, apertureSize = 3)

# Apply a probabilistic Hough transform to the image
minLineLength = 50
maxLineGap = 10
lines = cv2.HoughLinesP(edged, 1, np.pi/180, 100, minLineLength, maxLineGap)

if lines is not None:
    print("Found lines")
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(frame, (x1, y1),(x2, y2), (0, 255, 0), 10)
    
##    lines = cv2.HoughLines(edged,1,np.pi/180,200)
##    
##    for rho,theta in lines[0]:
##        a = np.cos(theta)
##        b = np.sin(theta)
##        x0 = a*rho
##        y0 = b*rho
##        x1 = int(x0 + 1000*(-b))
##        y1 = int(y0 + 1000*(a))
##        x2 = int(x0 - 1000*(-b))
##        y2 = int(y0 - 1000*(a))
##
##    cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
##
cv2.imshow("preview", frame)


key = cv2.waitKey(20)
if key == 27: # exit on ESC
    cv2.destroyWindow("preview")