import sys
sys.path.insert(1, r"/workspace/data\trojan\data engine")
import patternEngine as pe
import dataPrep      as dp
from datetime import datetime as dt
import subprocess
import schedule
import logging
import time
import sys
import os

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r /workspace/data\trojan\requirements.txt'])
#!pip install -r requirements.txt

#pe.engine()

REST_TIME = 60 # 5 hours

def schedule_engine():
    print("Scheduled task started. ")
    pe.engine()
    print("Scheduled task finished. ")


#schedule.every(1).minutes.do(schedule_engine)
#schedule.every().sunday.at("23:50").do(schedule_engine)
schedule.every(0.5).hours.do(schedule_engine)

while True:
    print("While loop started | Looped task starting | ", str(dt.now())[:-7])
    schedule.run_pending()
    print("Looped task ended | Taking a break | ", str(dt.now())[:-7])
    time.sleep(REST_TIME) # take a good break
    print("Break ended | While loop restarting | " + str(dt.now())[:-7])

#sys.stdout = open("log.txt", "a")
#ERROR_LOGS = r"/workspace/data\trojan\error.log"
#logging.basicConfig(filename = ERROR_LOGS, level = logging.ERROR)

#try:
#    pe.engine()
#except Exception as e:
#    with open(ERROR_LOGS, "a") as f:
#        f.write(str(e))
#    
#    os.system("python main.py")