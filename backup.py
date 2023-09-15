#!/usr/bin/python3

import math
import sys
from backupcfg import jobs, backupDir 
import os
from datetime import datetime
import pathlib
import shutil

def main():
    
    try:
        argCount = len(sys.argv)
        
        if argCount != 2:
            print("ERROR: job not specified .")
        else:
            job = sys.argv[1]
            if not job in jobs:
                print(f"error: job {job} is not in job list")
            
            else:
                jobPath = jobs [job]
                if  not  os.path.exists(jobPath):
                    print("file doesnt exist")
                
                else:
                    destination = backupDir
                    if not os.path.exists(destination):
                        print(f"error: destination {detsination} does not exist")            
                    
                    
                    else:
                        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                        srcPath = pathlib.PurePath(job)
                        dstLoc = destination + "/" + srcPath.name + "-" + dateTimeStamp
                        
                        if pathlib.Path(jobPath).is_dir():
                            shutil.copytree(jobPath, dstLoc)
                        
                        else:    
                            shutil.copy2(jobPath, dstLoc)
                                
                           
                                        
                    pass        
                    
   
    except:

        print("general ERROR: ocurered")

        
if __name__ == '__main__':
    main()