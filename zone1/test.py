import cv2 
a = cv2.VideoCapture(0)
#b = cv2.VideoCapture(1)

while True:
    _, frame1 = a.read()
    #_, frame2 = b.read()
    cv2.imshow("frame1",frame1)
    #cv2.imshow("frame2",frame2)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
a.release()
#b.release()
cv2.destroyAllWindows()