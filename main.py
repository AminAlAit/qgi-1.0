import sys
sys.path.insert(1, r"/workspace/data\trojan\data engine")
import patternEngine as pe
import dataPrep      as dp
import subprocess
import schedule
import time

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r /workspace/data\trojan\requirements.txt'])
#!pip install -r requirements.txt


REST_TIME = 86400 # 5 hours


def schedule_engine():
    print("Scheduled task started. ")
    pe.engine()
    print("Scheduled task finished. ")


#schedule.every(1).minutes.do(schedule_engine)
schedule.every().monday.at("23:59").do(schedule_engine)


while True:
    print("While loop started. ")
    print("Looped task starting: ")
    schedule.run_pending()
    print("Looped task ended. ")
    print("Taking a break. ")
    time.sleep(REST_TIME) # take a good break
    print("Break ended. ")
    print("While loop restarting. ")