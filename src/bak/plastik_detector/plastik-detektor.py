import cv2
import serial
import numpy as np
import math as m

#Hintergrund fuer das Haubtfenster
GuiImage = np.zeros((800,1024,3), np.uint8)


ThTransparency = 90        #Grenzwert-Konstante fuer Transparenz
ThPlastic = 0.8            #Grenzwert-Konstante fuer Plastik

MyCamera = None
MySerialInterface = None

GuiWindowName = "Plastik Detector"

AvgRoiTest=0              #Mittelwert von dem ROI nach dem Bewegen des Objekts
AvgRoiTestFilter=0        #Mittelwert von dem ROI-Filter vor dem Bewegen des Objekts

RoiPosUL = (160, 160)
RoiPosBR = (250, 360)
RoiOffset = 120
DistDetectorPusher = 500

FactorRoiFilterObjectToEmpty=0  #Factor zeigt die Aenderung in dem Filter-Bereich
                                #Werte bei 1.0 - Keine Aenderung, kein Objekt
                                #Werte > 1.0   - Objekt ist heller als Hintergrund (unwahrscheinlich, licht kommt durch Objekt)
                                #Werte < 1.0   - Objekt im Bereich

FactorRoiObjectToEmpty=0        #Das gleiche wie oben nur für den Bereich ohne Filter


result=None                     #Ergebnis
                                #Ein Faktor der angibt ob das Objekt ROI und ROI mit Filter im gleichen Maaße abdunkelt
                                #Werte um 1 bedeuten das das Objekt Glass oder nicht transparent ist

objectDetected=False


#Funktion um aktuelle Mausposition herauszufinden
def clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cv2.namedWindow(GuiWindowName)               #Fenster erstellen
cv2.setMouseCallback(GuiWindowName, clicked) #Maus dem Fenster zuweisen


try:
    MySerialInterface = serial.Serial('COM3')  #
except:
    MySerialInterface=None

MySerialInterface.write(b'2:5;')

try:
    MyCamera = cv2.VideoCapture(0)
except:
    MyCamera=None


#img1 = None

#img2 = None
calibrated = False  #Zustandsvariable Kalibrierung durchgeführt
AvgRoi = -1        #
AvgRoiFilter = -1

# Bildobjekte zum anzeigen des Objektes
imgGlas = cv2.imread("glass.png")
imgPet = cv2.imread("pet.png")
imgTp = cv2.imread("tp.png")

imgAct = None # zuletzt erkannter Objekttyp zum Anzeigen

PosCamImg = (10,10)         # Position im GUI zum zeichen des Kamerabildes
PosRecImg = (10,680)        # Position im GUI zum zeichen des erkannten Objekttypes

k=0
while True:

    errCode, img = MyCamera.read()    # Kamerabild lesen

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Kopie vom Bild in grau Stufen erstellen
    roiFilter = gray[RoiPosUL[1]: RoiPosBR[1], RoiPosUL[0]: RoiPosBR[0]]
    roi = gray[RoiPosUL[1]: RoiPosBR[1], RoiPosUL[0] + RoiOffset: RoiPosBR[0] + RoiOffset]
    GuiImage = np.zeros((800, 1024, 3), np.uint8)
    detText=""
    if not calibrated:
        AvgRoi = cv2.mean(roi)[0]
        AvgRoiFilter = cv2.mean(roiFilter)[0]
        calibrated = True
        result=None
        objectDetected = False
        print("Calibration finished Mean: %d , Mean Filter:%d" % (AvgRoi , AvgRoiFilter))
    else:
        absDiff = meanRoiAct = cv2.mean(roi)[0]
        meanRoiFilterAct = cv2.mean(roiFilter)[0]

        absDiff = m.fabs(AvgRoi - meanRoiAct)
        absDiffF = m.fabs(AvgRoiFilter - meanRoiFilterAct)
        if absDiff / AvgRoi  > 0.1 or absDiffF / AvgRoiFilter  > 0.1:
            objectDetected = True
            #cv2.waitKey(3000)
        else:
            objectDetected = False
            #imgAct = None

        detText = "Object detected: %d (ROIF diff: %d%% : ROI diff: %d%%)" % (objectDetected,
                                                                              int(absDiffF / AvgRoiFilter * 100),
                                                                              int(absDiff / AvgRoi * 100))

        cv2.putText(GuiImage, detText,
                    (10, 650),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    2)



    GuiImage[ PosCamImg[0]:PosCamImg[0]+img.shape[0], PosCamImg[1]:PosCamImg[1]+img.shape[1] ] = img
    if imgAct is not None:
        GuiImage[PosRecImg[0]:PosRecImg[0] + imgAct.shape[0], PosRecImg[1]:PosRecImg[1] + imgAct.shape[1]] = imgAct

    cv2.rectangle(GuiImage, (PosRecImg[1],PosRecImg[0]), (PosRecImg[1]+150,PosRecImg[0]+300), (0, 255, 0), 4, 1)

    cv2.rectangle(GuiImage,(PosCamImg[1],PosCamImg[0]), (PosCamImg[1]+img.shape[1],PosCamImg[0]+img.shape[0]),(255,0,0),2,1 )

    cv2.rectangle(GuiImage, RoiPosUL, RoiPosBR, (255, 255, 0), 2, 1)
    p1tmp = (RoiPosUL[0] + RoiOffset, RoiPosUL[1])
    p2tmp = (RoiPosBR[0] + RoiOffset, RoiPosBR[1])
    cv2.rectangle(GuiImage, p1tmp, p2tmp, (255, 255, 255), 2, 1)

    if k & 0xFF == ord('c'):
        imgAct = None
        calibrated = False
        GuiImage = np.zeros((800, 1024, 3), np.uint8)

    if k & 0xFF == ord('q'):
        exit(0)
    if k & 0xFF == ord('p'):
        GuiImage = np.zeros((800, 1024, 3), np.uint8)
        imgAct = None
        #img1 = roiFilter.copy()
        MySerialInterface.write(b'1:35;')

        cv2.waitKey(1500)

        _, img = MyCamera.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi = gray[RoiPosUL[1]: RoiPosBR[1], RoiPosUL[0] + RoiOffset: RoiPosBR[0] + RoiOffset]

        #img2 = roi.copy()
        AvgRoiTestFilter = cv2.mean(roiFilter)[0]
        AvgRoiTest = cv2.mean(roi)[0]
        FactorRoiFilterObjectToEmpty = AvgRoiTestFilter / AvgRoiFilter
        FactorRoiObjectToEmpty = AvgRoiTest / AvgRoi
        result = FactorRoiFilterObjectToEmpty / FactorRoiObjectToEmpty
        print("Finished: Avg: %d , Avg Filter: %d , F1: %f , F2: %f , Result: %f" % (AvgRoiTest, AvgRoiTestFilter, FactorRoiFilterObjectToEmpty, FactorRoiObjectToEmpty, result))
        if AvgRoiTest > ThTransparency:
            print("Transparent object")
            if result < ThPlastic:
                imgAct = imgPet
                print("Plastic object")
                MySerialInterface.write(b'2:5;')
                MySerialInterface.write(b"1:%d;" % (DistDetectorPusher) )
                MySerialInterface.write(b'2:175;')
            else:
                imgAct = imgGlas
                print("Glas")
                MySerialInterface.write(b'2:5;')
                MySerialInterface.write(b'1:1000;')
        else:
            print("Not transparent object")
            imgAct = imgTp
            MySerialInterface.write(b'2:175;')
            MySerialInterface.write(b"1:%d;" % (DistDetectorPusher))
            MySerialInterface.write(b'2:5')

        #MySerialInterface.write(b'1:500;')

        #cv2.waitKey(3000)

    if k & 0xFF == ord('1'):
        MySerialInterface.write(b'1:5;')
    if k & 0xFF == ord('2'):
        MySerialInterface.write(b'1:-5;')
    #if k & 0xFF == ord('s'):
        #img1 = roiFilter

    if calibrated:
        calText = "Calibrated. Avg ROI_Filter/ROI: %d / %d" % (AvgRoiFilter, AvgRoi)

        cv2.putText(GuiImage, calText,
                (10, 550),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 255),
                1,
                2)

    if result is not  None:
        restext = "Finished: Mean: %d , Mean Filter: %d , F1: %f , F2: %f , Result: %f" % (AvgRoiTest, AvgRoiTestFilter, FactorRoiFilterObjectToEmpty, FactorRoiObjectToEmpty, result)
        cv2.putText(GuiImage, restext,
                    (10, 600),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    2)

    cv2.imshow(GuiWindowName, GuiImage)
    k = cv2.waitKey(100)