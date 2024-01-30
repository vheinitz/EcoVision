import cv2
import serial

ThTransparency = 90
ThPlastic = 0.8

def clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cv2.namedWindow("kamera")
cv2.setMouseCallback("kamera", clicked)


ser = serial.Serial('COM3')  # open serial port
print(ser)         # check which port was really used



cam= cv2.VideoCapture(0)
img1 = None
img2 = None
calibrated = False
meanRoi = -1
meanRoiFilter = -1

while True:

    _, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    p1= (150, 160)
    p2= (240, 360)
    offset = 120
    roiFilter = gray[p1[1]: p2[1], p1[0]: p2[0]]
    roi = gray[p1[1]: p2[1], p1[0]+offset: p2[0]+offset]

    if not calibrated:
        meanRoi = cv2.mean(roi)[0]
        meanRoiFilter = cv2.mean(roiFilter)[0]
        calibrated = True
        print("Calibration finished Mean: %d , Mean Filter:%d" % (meanRoi , meanRoiFilter))

    cv2.imshow('roiFilter', roiFilter)
    cv2.imshow('roi', roi)
    cv2.imshow('kamera', img)


    #roiFilterNorm = roiFilter*0.1
    #cv2.imshow('roiFilterNorm', roiFilterNorm)


    k=cv2.waitKey(20)
    if k & 0xFF == ord('c'):
        calibrated = False
    if k & 0xFF == ord('p'):
        img1 = roiFilter.copy()
        ser.write(b'35;')
        img2 = roi.copy()
        mean1 = cv2.mean(img1)[0]
        mean2 = cv2.mean(img2)[0]
        F1 = mean1 / meanRoiFilter
        F2 = mean2 / meanRoi
        result = F1/F2
        print("Finished: Mean: %d , Mean Filter: %d , F1: %f , F2: %f , Result: %f" % (mean2, mean1, F1, F2, result ))
        if mean2 > ThTransparency:
            print("Transparent object")
            if result < ThPlastic:
                print("Plastic object")
            else:
                print("Glas")
        else:
            print("Not transparent object")

        cv2.imshow('img1', img1)
        cv2.imshow('img2', img2)
        cv2.waitKey(20)
    if k & 0xFF == ord('1'):
        ser.write(b'5;')
    if k & 0xFF == ord('2'):
        ser.write(b'-5;')
    if k & 0xFF == ord('s'):
        img1 = roiFilter


    #print(img.shape, imgR.shape)
