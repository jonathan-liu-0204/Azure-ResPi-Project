import os
from datetime import datetime
import sys
import time
import subprocess

#------------azure custom vision--------------

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Replace with valid values
ENDPOINT = "PASTE_YOUR_CUSTOM_VISION_TRAINING_ENDPOINT_HERE"
training_key = "PASTE_YOUR_CUSTOM_VISION_TRAINING_SUBSCRIPTION_KEY_HERE"
prediction_key = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_SUBSCRIPTION_KEY_HERE"
prediction_resource_id = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_RESOURCE_ID_HERE"

#---------------------------------------------

# read the absolute path
script_dir = os.path.dirname(__file__)

# call the .sh to capture the image
DATE = datetime.now().strftime("%Y-%m-%d_%H%M")
os.system('fswebcam -r 1280x720 --no-banner ./captured/$' + DATE + '.jpg')

# create the real path
rel_path = DATE +".jpg"

#  join the absolute path and created file name
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

path = "./"

with open(os.path.join(path, "/captured", rel_path), "rb") as image_contents:

    print(image_contents)
    # results = predictor.classify_image(
    #     project.id, publish_iteration_name, image_contents.read())

    # # Display the results.
    # for prediction in results.predictions:
    #     print("\t" + prediction.tag_name +
    #           ": {0:.2f}%".format(prediction.probability * 100))