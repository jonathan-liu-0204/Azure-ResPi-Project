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
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient

# IMPORTANT: Replace connection string with your storage account connection string
# Usually starts with DefaultEndpointsProtocol=https;...
MY_CONNECTION_STRING = "REPLACE_THIS"
 
# Replace with blob container. This should be already created in azure storage.
MY_IMAGE_CONTAINER = "myimages"

#---------------------------------------------

class AzureBlobFileUploader:
  def __init__(self):
    print("Intializing AzureBlobFileUploader")
 
    # Initialize the connection to Azure storage account
    self.blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
 
  def upload_all_images_in_folder(self):
    # Get all files with jpg extension and exclude directories
    all_file_names = [f for f in os.listdir(LOCAL_IMAGE_PATH)
                    if os.path.isfile(os.path.join(LOCAL_IMAGE_PATH, f)) and ".jpg" in f]
 
    # Upload each file
    for file_name in all_file_names:
      self.upload_image(file_name)
 
  def upload_image(self,file_name):
    # Create blob with same name as local file name
    blob_client = self.blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER,
                                                          blob=file_name)
    # Get full path to the file
    upload_file_path = os.path.join(LOCAL_IMAGE_PATH, file_name)
 
    # Create blob on storage
    # Overwrite if it already exists!
    image_content_setting = ContentSettings(content_type='image/jpeg')
    print(f"uploading file - {file_name}")
    with open(upload_file_path, "rb") as data:
      blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)

# read the absolute path
script_dir = os.path.dirname(os.path.realpath(__file__))

DATE = datetime.now().strftime("%Y-%m-%d_%H%M")
os.system('fswebcam -r 1280x720 --no-banner ./captured/' + DATE + '.jpg')

# create the real path
rel_path = DATE + ".jpg"

#  join the absolute path and created file name
abs_file_path = os.path.join(script_dir + "/captured", rel_path)

LOCAL_IMAGE_PATH = abs_file_path

with open(abs_file_path, "rb") as image_contents:
    results = predictor.classify_image(project_id, iteration_name, image_contents)

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
