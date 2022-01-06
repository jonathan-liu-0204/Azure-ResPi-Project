import os
import datetime


from azure.storage.blob import BlockBlobService

# read the absolute path
script_dir = os.path.dirname(__file__)
# call the .sh to capture the image
os.system('./webcam.sh')
#get the date and time, set the date and time as a filename.
currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
# create the real path
rel_path = currentdate +".jpg"

