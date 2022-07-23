from distutils.command.config import config
import pytesseract
import cv2 
import matplotlib.pyplot as plt
import imutils

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = 'Img/7.jpg'

image = cv2.imread(path)

imageHeight, imageWidth = image.shape[:2]

org_image = cv2.imread(path)
image = org_image
ratio = image.shape[1] / float(image.shape[1])
image = imutils.resize(image, width=500)

# 이미지를 grayscale로 변환하고 blur를 적용
# 모서리를 찾기위한 이미지 연산
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
edged = cv2.Canny(blurred, 75, 200)

text = pytesseract.image_to_string(image, config="--psm 6")
print(text)