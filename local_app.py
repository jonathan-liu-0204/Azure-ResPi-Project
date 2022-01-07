import os
from datetime import datetime
import sys
import time
import subprocess

from numpy import asarray
from PIL import Image

#------------azure custom vision--------------

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Replace with valid values
ENDPOINT = "https://driverstatusdetection.cognitiveservices.azure.com/"
training_key = "4b345d978c424700864ab175d9c1cbe1"
prediction_key = "67e043e7eb05473698e2c8b8cd390cfb"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/GPS-Intern-Jonathan-RaspixAzure-Project/providers/Microsoft.CognitiveServices/accounts/DriverStatusDetection-Prediction"
iteration_id = "6af8ff86-a8dd-49b5-ab3f-53b0398cc2d5"


credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

publish_iteration_name = "classifyModel"
#---------------------------------------------

# read the absolute path
script_dir = os.path.dirname(os.path.realpath(__file__))

DATE = datetime.now().strftime("%Y-%m-%d_%H%M")
os.system('fswebcam -r 1280x720 --no-banner ./captured/' + DATE + '.jpg')

# create the real path
rel_path = DATE + ".jpg"

#  join the absolute path and created file name
abs_file_path = os.path.join(script_dir + "/captured", rel_path)

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

#image = Image.open(abs_file_path)

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

with Image.open(abs_file_path, "rb") as image_contents:
    results = predictor.classify_image(iteration_id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))