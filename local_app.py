import os
from datetime import datetime
import time

from numpy import asarray
from PIL import Image

#------------azure custom vision--------------

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

# Replace with valid values
ENDPOINT = "https://driverstatusdetection-prediction.cognitiveservices.azure.com/"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/GPS-Intern-Jonathan-RaspixAzure-Project/providers/Microsoft.CognitiveServices/accounts/DriverStatusDetection-Prediction"
iteration_name = "Iteration1"
prediction_key = ""
project_id = ""

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# read the absolute path
script_dir = os.path.dirname(os.path.realpath(__file__))

def counter(num_of_secs):
    while num_of_secs:
        time.sleep(1)
        num_of_secs -= 1
    print("The time of detection process has expired.")
    stop_token = 1


#ask the user for the total time to observe
total_time = input("Hi there :) Please enter the total observation time (minutes): ")
counter(total_time * 60)
stop_token = 0

while (stop_token != 1):
    DATE = datetime.now().strftime("%Y-%m-%d_%H%M")
    os.system('fswebcam -r 1280x720 --no-banner ./captured/' + DATE + '.jpg')

    # create the real path
    rel_path = DATE + ".jpg"

    #  join the absolute path and created file name
    abs_file_path = os.path.join(script_dir + "/captured", rel_path)

    with open(abs_file_path, "rb") as image_contents:

        results = predictor.classify_image(project_id, iteration_name, image_contents)

        # Display the results.
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))

    print("Analyzing...")
    time.sleep(15)

    