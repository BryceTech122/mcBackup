import shutil
from datetime import datetime
import schedule
import time
import yaml
import os.path
import os
import tarfile
import logging

# Initialize
def init():
    # Initialize logging
    logging.basicConfig(filename='server.log',level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('fBackup Server Started')
    # Open config
    with open('serverConfig.yml') as f:  
        data = yaml.load(f, Loader=yaml.FullLoader)
        source_dir = data.get('bu_folder')
        backup_occurrence = data.get('backup_occurrence')
        backup_time = data.get('backup_time')
    # Schedule backup time
    backup = 'schedule.every().' + backup_occurrence + '.at(\'' + backup_time + '\').do(make_tarfile, source_dir=source_dir)'
    exec(backup)
    logging.info('Init Complete')

# Function to generate filename with .tar extenssion
def make_filename():
    now = datetime.now()
    time = now.strftime("%Y:%m:%d_%H:%M:%S")
    fname = "backup/backup_"+str(time)+'.tar'
    return fname

# Function to remove old backups
def remove_old(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.tar'):
            os.remove(folder_path + file_name)

# Function to check if backup dir exists and if not, create one
def create_bu_dir():
    if(os.path.isdir('./backup/') == True):
        logging.info('Backup Dir Exists')
    else:
        logging.info('Creating Backup Dir')
        os.mkdir('./backup/')
        if(os.path.isdir('./backup/') == True):
            logging.info('Backup Dir Created')
        else:
            logging.info('Backup Dir Creation Failed')

# Function to tarfile your source_dir
def make_tarfile(source_dir):
    logging.info('Starting Backup')
    create_bu_dir()
    remove_old('./backup/')
    logging.info('Removing Previous Backups')
    output_filename = make_filename()
    with tarfile.open(output_filename, "w:gz") as tar:
        logging.info('Starting Backup '+output_filename)
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    logging.info('Backup Complete! '+output_filename)

# Initialize and backup at program start
init()
schedule.run_all()

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)