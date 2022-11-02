import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
# Access Web cam
cap = cv2.VideoCapture(0)
# to get more space to drag images around
cap.set(3, 1280)
cap.set(4, 720)
# Detecting hand
detector = HandDetector(detectionCon=0.8)

class DragImg():
    def __init__(self, path, posOrigin, imgType):
        self.posOrigin= posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else :
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2] # basically height, width, channel we ignore channel so only 2
    # Creating a method that will update the position of the images
    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
        # check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            # print(" Inside Image")
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
            # to move image update value of ox, oy


# reading images
# img1 = cv2.imread("ImagesJPG/2.jpg")
# img1 = cv2.imread("ImagesPNG/2.png", cv2.IMREAD_UNCHANGED)
# now importing multipule images
# ox, oy = 500, 200
# list of images in that folder
path = "ImagesMix"
myList = os.listdir(path)  # taking all the images into list
print(myList)
listImg = []
# we will create a class and multipule objects which will have its own size,pixel ,origin

for x, pathImg in enumerate(myList):
    # calling DragImg class
    if 'png' in pathImg:
        # print('png')
        imgType = 'png'
    else:
        # print('jpg')
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x*300, 50], imgType))

print(len(listImg))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # flip image (initial is reverse)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hands, img = detector.findHands(img, flipType=False)
    # slicing method
    if hands:
        lmList = hands[0]['lmList']
        # distance btw fingers and image should be inside. like before project
        # check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        # print(length)
        if length < 50:
            cursor = lmList[8]
            # Calling update function
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        for imgObject in listImg: # here imgObject is an object not image
            # we have image , its origin, type, path, size
            # Draw for jpg iamges
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for png Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])  # the overlay function uses origin not center point
            else:
                img[oy:oy+h, ox:ox+w] = imgObject.img # Next when are we Clicking and Draging





    except:
        pass
    cv2.imshow("Image", img)
    cv2.waitKey(1)
