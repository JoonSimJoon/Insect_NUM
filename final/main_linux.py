from importlib.resources import path
import json
import schedule
import time

pathdata = ""
timedata = " "

def query():
    with open('setting.json','r') as f:
        data = json.load(f)
    pathdata = data['path']
    timedata = str(data['time']['hour'])+":"+str(data['time']['min'])
    print(pathdata)

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
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()