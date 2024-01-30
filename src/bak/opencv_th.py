import cv2
cam= cv2.VideoCapture(1)

while True:

    _, img = cam.read()
    cv2.imshow('image', img)

    #cv2.imshow('roi', roi)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    roi = gray[120:120 * 3, int(640 / 4): int(640 / 4) * 3]
    _, th = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('th', th)
    obj = roi*th
    cv2.imshow('obj', obj)
    count = cv2.countNonZero(th)
    #print(count)
    if count>7400:
        print('alarm')
    cv2.waitKey(20)
    #print(img.shape, imgR.shape)
