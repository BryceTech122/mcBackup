from ftplib import FTP
from datetime import datetime
import schedule
import time
import yaml

# Open config file
with open('clientConfig.yml') as f:  
    data = yaml.load(f, Loader=yaml.FullLoader)
    servip = data.get('server_ip')
    uname = data.get('username')
    passwd = data.get('password')
    budir = data.get('backup_folder')

# Initial connect to FTP to confirm credentials
ftp = FTP(host=servip,user=uname,passwd=passwd)
ftp.close()

def current_time():
    now = datetime.now()
    time = now.strftime('%Y:%m:%d_%H:%M:%S')
    return time

# Function to copy files from budir to ./backup
def copy_backup():
    print('['+str(current_time())+'] Starting Download of All Backups')
    ftp = FTP(host=servip,user=uname,passwd=passwd)
    ftp.cwd(budir)
    files = ftp.nlst()
    # TODO: If statment to autogenerate ./backup directory
    for file in files:
        print('    - Downloading... '+file)
        if file.endswith('.tar'):
            ftp.retrbinary('RETR ' + file ,open('./backup/' + file, 'wb').write)
    print('['+str(current_time())+'] Done Downloading All Backups\n')
    ftp.close()

# Schedule backup and run at client start
schedule.every(5).minutes.at(":30").do(copy_backup)
schedule.run_all()

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)