import cv2
cam= cv2.VideoCapture(0)

while True:

    _, img = cam.read()
    imgB, imgG, imgR = cv2.split(img)
    cv2.imshow('image', img)
    cv2.imshow('image rot', imgR)
    cv2.imshow('image blau', imgB)
    cv2.imshow('image gruen', imgG)
    #imgR = 0
    imgR *= 0
    imgB *= 0
    cv2.merge([imgB, imgG, imgR], img)
    cv2.imshow('image1', img)
    cv2.waitKey(20)
    #print(img.shape, imgR.shape)
