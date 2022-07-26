import json
from random import random
import schedule
import time
import datetime as dt
import os
import pytesseract
import imutils
import cv2
from imutils.perspective import four_point_transform
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def OCR(path):
    org_image = cv2.imread(path)
    image = org_image
    ratio = image.shape[1] / float(image.shape[1])
    image = imutils.resize(image, width=500)

    # 이미지를 grayscale로 변환하고 blur를 적용
    # 모서리를 찾기위한 이미지 연산
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    receiptCnt = None

    # 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
    for c in cnts:
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

    gray = cv2.cvtColor(receipt, cv2.COLOR_BGR2GRAY)
    resized_gray = cv2.resize(gray,(104,104))

    text = pytesseract.image_to_string(resized_gray, config="--psm 6")
    return text


def makedirs(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

def query():
    with open('setting.json','r') as f:
        data = json.load(f)
    pathdata = data['path']
    originalpath = pathdata+"/data"
    detectedpath = pathdata+"/data-filtered"
    nondetectedpath = pathdata+"/data-filtered-notpass"

    #폴더 없으면 폴더 생성
    makedirs(originalpath)
    makedirs(detectedpath)
    makedirs(nondetectedpath)

    #오늘 날짜 접근
    x = dt.datetime.now() 
    year = str(x.year).zfill(4)
    month = str(x.month).zfill(2)
    day = str(x.day).zfill(2)
    today = year+"-"+month+day #폴더 형식으로 변환
    #print(today)

    #path + 오늘 날짜, 폴더 생성
    originalpath_today = originalpath + "/" + today
    detectedpath_today = detectedpath + "/" + today
    nondetectedpath_today = nondetectedpath + "/" + today
    
    makedirs(originalpath_today)
    makedirs(detectedpath_today)
    makedirs(nondetectedpath_today)

    #오리지널 폴더 내 사진들 들고오기 
    og_img_list = os.listdir(originalpath_today)
    for i in og_img_list:
        #print(i)
        path = originalpath_today + "/" + i
        res = OCR(path)
        numbers = re.sub(r'[^0-9]', '', res)
        print(numbers)

    

def main(): 
    #path.json에서 주소 들고오기
    with open('setting.json','r') as f:
        data = json.load(f)
    pathdata = data['path']
    timedata = str(data['time']['hour'])+":"+str(data['time']['min'])
    #특정 시간마다 작업 수행
    # step3.실행 주기 설정
    schedule.every().day.at(timedata).do(query)
    # step4.스캐쥴 시작
    query()
    while False:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()