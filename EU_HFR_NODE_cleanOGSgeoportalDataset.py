#!/usr/bin/python3


# Created on Wed Mar 25 13:36:47 2026

# @author: Lorenzo Corgnati
# e-mail: lorenzopaolo.corgnati@cnr.it


# This application periodically removes data older than 4 months from the folder
# dedicated to the OGS geoportal, which contains the last 4 month of total data 
# from HFR-NAdr network. This application runs on the radarcombine 
# virtual machine, that is part of the European HFR Node (EU HFR NODE) workflow 
# for the production of HFR NRT datasets.

import os
import sys
import getopt
import glob
import logging
import datetime as dt
from dateutil.relativedelta import relativedelta
import re

####################
# MAIN DEFINITION
####################

def main(argv):
    
#####
# Setup
#####
       
    # Set the argument structure
    try:
        opts, args = getopt.getopt(argv,"m:h",["memory=","help"])
    except getopt.GetoptError:
        print('Usage: EU_HFR_NODE_cleanOGSgeoportalDataset.py -m <number of months in the past beyond which files are removed (default to 4)>')
        sys.exit(2)
        
    if not argv:
        memory = 4       # number of months in the past beyond which files are removed (default to 15)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage: EU_HFR_NODE_cleanOGSgeoportalDataset.py -m <number of months in the past beyond which files are removed (default to 4)>')
            sys.exit()
        elif opt in ("-m", "--memory"):
            memory = int(arg)
            
    # Create logger
    logger = logging.getLogger('EU_HFR_NODE_cleanOGSgeoportalDataset')
    logger.setLevel(logging.INFO)
    # Create logfile handler
    logFilename = '/var/log/EU_HFR_NODE_NRT/EU_HFR_NODE_cleanOGSgeoportalDataset.log'
    lfh = logging.FileHandler(logFilename)
    lfh.setLevel(logging.INFO)
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] -- %(levelname)s -- %(module)s - %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
    # Add formatter to lfh and ch
    lfh.setFormatter(formatter)
    # Add lfh and ch to logger
    logger.addHandler(lfh)
    
    # Initialize error flag
    cODerr = False
    
    logger.info('Cleaning started.')
    
    try:
        
#####
# Set the earliest date for data cleaning
#####        
        
        # Set datetime of the earliest date for data cleaning
        startDate = (dt.datetime.utcnow()- relativedelta(months=memory))
        
#####
# Set the folder path patterns for the folders to be cleaned
#####
        
        # Set the path pattern for the folder to be cleaned
        clnFolderPath = '/home/radarcombine/EU_HFR_NODE/HFR-NAdr/Totals_nc_Last4Months/'
    
####
# Clean old data
#####        
        
        # Set the datetime pattern YYYY_MM_DD_hhhh in filenames
        pattern = re.compile(r'(\d{4}_\d{2}_\d{2}_\d{4})')
        
        # List all the files to be removed
        allFiles = glob.glob(os.path.join(clnFolderPath,'**/*'), recursive = True)   
        # Keep only files (not folders)
        allFiles = [item for item in allFiles if not os.path.isdir(item)]

        # Remove files
        for file in allFiles:
            match = pattern.search(file)
            if match:
                dateStr = match.group(1)
                if dt.datetime.strptime(dateStr,'%Y_%m_%d_%H%M') < startDate:
                    os.remove(file)
                    logger.info('File ' + file + ' removed.')

        # Remove empty folders
        for root, dirs, files in os.walk(clnFolderPath, topdown=False):
            for d in dirs:
                fullPath = os.path.join(root, d)
                try:
                    # if the directory is empty, remove it
                    if not os.listdir(fullPath):
                        os.rmdir(fullPath)
                        logger.info('Folder ' + d + ' removed.')
                except Exception as e:
                    logger.info('Error removing folder ' + d + ': ' + e)

    except Exception as err:
        cODerr = True
        logger.error(err.args[0])    
    
    
####################
    
    if(not cODerr):
        logger.info('Successfully executed.')
    else:
        logger.error('Exited with errors.')
            
####################


#####################################
# SCRIPT LAUNCHER
#####################################    
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
