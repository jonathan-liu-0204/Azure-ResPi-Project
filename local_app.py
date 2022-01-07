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
ENDPOINT = "https://driverstatusdetection-prediction.cognitiveservices.azure.com/"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/GPS-Intern-Jonathan-RaspixAzure-Project/providers/Microsoft.CognitiveServices/accounts/DriverStatusDetection-Prediction"
iteration_name = "Iteration1"
prediction_key = ""
project_id = ""


prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

#---------------------------------------------
#----------------azure blob storage-------------

from azure.storage.blob import BlobClient

# Retrieve the connection string from an environment variable. Note that a connection
# string grants all permissions to the caller, making it less secure than obtaining a
# BlobClient object using credentials.
conn_string = os.environ["DefaultEndpointsProtocol=https;AccountName=raspiazureproject;AccountKey=DPiBhdEhyfBdyEG32tt4PpL+r4N3oa3ZOIIYBwiXwnCh6NuLfeGTozrJ64BY0/1z0M09Mc7xnoEjFIZ8GGfF9A==;EndpointSuffix=core.windows.net"]

#---------------------------------------------


# read the absolute path
script_dir = os.path.dirname(os.path.realpath(__file__))

DATE = datetime.now().strftime("%Y-%m-%d_%H%M")
os.system('fswebcam -r 1280x720 --no-banner ./captured/' + DATE + '.jpg')

# Create the client object for the resource identified by the connection string,
# indicating also the blob container and the name of the specific blob we want.
blob_client = BlobClient.from_connection_string(conn_string,
    container_name="capturedimages", blob_name=DATE)

# create the real path
rel_path = DATE + ".jpg"

#  join the absolute path and created file name
abs_file_path = os.path.join(script_dir + "/captured", rel_path)

with open(abs_file_path, "rb") as image_contents:

    results = predictor.classify_image(project_id, iteration_name, image_contents)

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
    
    blob_client.upload_blob(image_contents)
