import cv2
cam= cv2.VideoCapture(1)

while True:

    _, img = cam.read()
    cv2.imshow('image', img)
    roi = img[120:120*3, int(640/4): int(640/4)*3]
    cv2.imshow('roi', roi)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    cv2.waitKey(20)
    #print(img.shape, imgR.shape)
