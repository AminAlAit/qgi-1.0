from datetime import datetime as dt
import statistics as st
import dataPrep as   dp
import pandas as     pd
import numpy as      np

def displayTime(i):
    if i == 0:                      
        print("////////////////// START \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("Script started execution at:")
        print(dt.now())
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ START //////////////////")
        return dt.now()
    elif i == 1:
        print("////////////////// END \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("Script ended execution at:")
        print(dt.now())
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ END //////////////////")
        return dt.now()