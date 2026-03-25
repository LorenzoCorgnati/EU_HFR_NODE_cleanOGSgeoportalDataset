# EU_HFR_NODE_cleanOGSgeoportalDataset
Python3 scripts for periodically removing old data created for the OGS geoportal. Tool to be run at the EU HFR Node.

This application is written in Python3 language and it is designed for High Frequency Radar (HFR) data management according to the European HFR node processing workflow.

This application periodically removes data older than 4 months from the folder dedicated to the OGS geoportal, which contains the last 4 month of total data from HFR-NAdr network. This application runs on the radarcombine virtual machine, that is part of the European HFR Node (EU HFR NODE) workflow for the production of HFR NRT datasets.

The application EU_HFR_NODE_cleanOGSgeoportalDataset.py has to be run on daily basis and it is launched via the cron.daily scheduler. When calling the application it is possible to specify the number of months in the past beyond which files are removed. If no input is specified, 4 months are used as time limit.

The application EU_HFR_NODE_cleanOGSgeoportalDataset.py takes as input the number of months in the past beyond which files are removed, lists all the files in the OGS geoportal folder, removes files older than the input time limit and finally removes all empty folders.

Usage: EU_HFR_NODE_cleanOGSgeoportalDataset.py -m <number of months in the past beyond which files are removed (default to 4)>

The required packages are:
- os
- sys
- getopt
- glob
- logging
- datetime as dt
- dateutil.relativedelta.relativedelta
- re

Cite as:
Lorenzo Corgnati. (2026). EU_HFR_NODE_cleanOGSgeoportalDataset. DOI: 


Author: Lorenzo Corgnati

Date: March 25, 2026

E-mail: lorenzopaolo.corgnati@cnr.it
