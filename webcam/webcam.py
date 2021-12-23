import os
import datetime
import sys
import time
import subprocess

from azure.storage.blob import BloBcLIENT

# read the absolute path
script_dir = os.path.dirname(__file__)
# call the .sh to capture the image
os.system('./webcam.sh')
#get the date and time, set the date and time as a filename.
currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
# create the real path
rel_path = currentdate +".jpg"

block_blob_service = BlockBlobService(account_name='raspiazureproject', account_key='YOURKEY')
block_blob_service.create_blob_from_path(
    'webcamimageupload',
    'firstblood.jpg',
    rel_path,
    content_settings=ContentSettings(content_type='image/jpg'))
print("file uploaded")

# #  join the absolute path and created file name
# abs_file_path = os.path.join(script_dir, rel_path)

# print(abs_file_path)