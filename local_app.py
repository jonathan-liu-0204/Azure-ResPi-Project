import os
from datetime import datetime
import sys
import time
import subprocess

# read the absolute path
script_dir = os.path.dirname(__file__)

# call the .sh to capture the image
DATE = datetime.now().strftime("%Y-%m-%d_%H%M")
os.system('fswebcam -r 1280x720 --no-banner ./$' + DATE + '.jpg')

# create the real path
rel_path = DATE +".jpg"

#  join the absolute path and created file name
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)