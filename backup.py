#!/usr/bin/python3

import math
import sys
from backupcfg import jobs 
import os

def main():
    
    try:
        argCount = len(sys.argv)
        
        if argCount != 2:
            print("ERROR: job not specified .")
        else:
            jobName = sys.argv[1]
            if not jobName in jobs:
                print(f"error: job {jobName} is not in job list")
            else:
                pass
            
    except:
        print("ERROR: job not specified .")
         
if __name__ == '__main__':
    main()