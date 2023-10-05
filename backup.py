#!/usr/bin/python3
"""
Program: backuo.py
Author: Daniel
version:1.0
copytight 2023 Daniel Carradine

This program is used to Backup files and directories
"""
import math
import sys
from backupcfg import jobs, backupDir, smtp, backupLog 
import os
from datetime import datetime
import pathlib
import shutil
import smtplib



def writeLogMessage(logmessage, dateTimeStamp, isSuccess):
    """
    writes log message to backup log file

    Arguments

    logmessage - string - message to be written to the file
    datetimestamp - string - current date time stamp to be written to the file 
    isSuccess - boolean - if true, write "SUCCESS to file else write "FAILURE"
    """
    try:
        file = open(backupLog, "a")

        # write success or failure message depending upon job outcome
        
        if isSuccess:
            file.write(f"SUCCESS {dateTimeStamp} {logmessage}\n")
        else:
            file.write(f"FAILURE {dateTimeStamp} {logmessage}\n")
            
            file.close()
                
    except FileNotFoundError:
        print(f"ERRROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accesible.")
        
        
def errorHandler(errorMessage, dateTimeStamp):
    print(errorMessage)
    writeLogMessage(errorMessage, dateTimeStamp, False)
    sendEmail(errorMessage) 
    """
    Writes an error message to the screen and the log file backup.log and send
    an error message as an email to the system administrator
        
    Arguments
    errorMessage - string error message to be displayed
    dateTimeStamp - string - displays date and time within the file, when error 
    occured
    """
    
# append all error messages and send 
def sendEmail(message):

    email = 'To: ' + smtp["recipient"] + "\n" + "From: " + smtp["sender"] + '\n' + 'Subject: backup error\n\n' + message + "\n" 
    
    #connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: and error occured.")
        
        
def main(): 
    """
    Perform one or more jobs specified on the command line.
    The file or directory to be backed up for a job is specified in the 
    backup.fg.py configuration file.ArithmeticError
    
    all successfull and failed jobs are logged onto backups.log file.
    
    Failed jobs are displayed on the screen and emailed to the system
    administrator
    """
    try:
        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        # check for number of cli arguments
        argCount = len(sys.argv) 
        if argCount < 2:
           errorHandler("ERROR: job not specified.", dateTimeStamp)
        else:
            # loop through all CLI arguments
            for job in sys.argv[1:]:
                # check job is valid                       
                if not  (job in jobs):
                    errorHandler("ERROR: job {job} is not on job list", dateTimeStamp)
                else:
                    #check source is valid for file or directory
                    source = jobs[job] 
                    if  not  os.path.exists(source):
                        errorHandler(f"ERROR: source {source} does not exist", dateTimeStamp)
                    else:
                        #check backup location is valid directory       
                        destination = backupDir
                        if not os.path.exists(destination):
                            errorHandler(f"error: destination {destination} does not exist", dateTimeStamp)            
                        else:
                            srcPath = pathlib.PurePath(job)
                            dstLoc = destination + "/" + srcPath.name + "-" + dateTimeStamp
                            # copies of file and/or direcctory to backup directory
                            if pathlib.Path(source).is_dir():
                                shutil.copytree(source, dstLoc)
                            else:    
                                shutil.copy2(source, dstLoc)
                                
                            writeLogMessage(f"backed up {source} to {dstLoc}", dateTimeStamp, True)
                                    
    except Exception as e:
        print("ERROR: An error has occured.")
        print (e)
      
if __name__ == '__main__':
    
    main()
    