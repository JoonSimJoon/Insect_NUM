from cgi import test
from imutils.perspective import four_point_transform
from keras.utils import np_utils
from keras.models import load_model
from PIL import Image
import pytesseract
import imutils
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = '../Img/1234.jpg'
org_image = cv2.imread(path)
image = org_image
ratio = image.shape[1] / float(image.shape[1])
image = imutils.resize(image, width=500)

# 이미지를 grayscale로 변환하고 blur를 적용
# 모서리를 찾기위한 이미지 연산
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
edged = cv2.Canny(blurred, 75, 200)

cv2.imshow('c',edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

receiptCnt = None

numc = 4
# 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
for c in cnts:
	if numc != 0:
		numc=numc-1
		continue
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# contours가 크기순으로 정렬되어 있기때문에 제일 첫번째 사각형을 영수증 영역으로 판단하고 break
	if len(approx) == 4:
		receiptCnt = approx
		break
    

# 만약 추출한 윤곽이 없을 경우 오류
if receiptCnt is None:
	raise Exception(("Could not find receipt outline."))


output = image.copy()
cv2.drawContours(output, [receiptCnt], -1, (0, 255, 0), 2)


receipt = four_point_transform(image, receiptCnt.reshape(4, 2) * ratio)
cv2.imshow('c',receipt)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray = cv2.cvtColor(receipt, cv2.COLOR_BGR2GRAY)
resized_gray = cv2.resize(gray,(104,104))


text = pytesseract.image_to_string(resized_gray, config="--psm 6")
print(text)
# cv2.imshow('c',gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite('../Img/resizecutimg.jpg',resized_gray)