import cv2

vc = cv2.VideoCapture(0)
cv2.namedWindow("WebCam", cv2.WINDOW_NORMAL)

#----------------------------------------
# Setup the TLS Socket 
#----------------------------------------

while vc.isOpened():
    status, frame = vc.read()
    cv2.imshow("WebCam", frame)
    print(frame)
    #-------------------------------
    #  Send Frame over an encrypted 
    #  TCP connection one frame at 
    #  a time 
    #------------------------------- 
    key = cv2.waitKey(20) #Wait 20 milliseconds before reading the next frame
    if key == 27: #Close if ESC key is pressed.
        break

vc.release()
cv2.destroyWindow("WebCam")
#Uncomment the following to extend your script.
#from mss import mss
#with mss() as sct:
#    image = sct.shot()
