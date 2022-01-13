import os
from datetime import datetime
import time

from numpy import asarray
import numpy as np
import pandas as pd
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
prediction_key = "ad86ccf83b41417a8aab841ee87b6654"
project_id = "5dc3b0ae-b36d-4cc5-ac3c-b3e45b9f4dbe"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# read the absolute path
script_dir = os.path.dirname(os.path.realpath(__file__))

#ask the user for the total time to observe
total_time = int(input("Hi there :) Please enter the total observation time (minutes): "))
num_of_secs = total_time * 60

# output = [2000000][1]
output = []

epoch = 0

while (num_of_secs > 0):

    start = time.time()

    DATE = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    os.system('fswebcam -r 1280x720 --no-banner ./captured/' + DATE + '.jpg')

    # create the real path
    rel_path = DATE + ".jpg"

    #  join the absolute path and created file name
    abs_file_path = os.path.join(script_dir + "/captured", rel_path)

    with open(abs_file_path, "rb") as image_contents:

        results = predictor.classify_image(project_id, iteration_name, image_contents)

        # Display the results.
        count = 0
        for prediction in results.predictions:
            if count < 1:
                print(prediction.tag_name)
                print(prediction.probability * 100)
                output.append([(prediction.tag_name),(prediction.probability * 100)])
                # output[epoch][0] = prediction.tag_name
                # output[epoch][1] = int(prediction.probability * 100)
                print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
            else:
                break
            count = count + 1

    print("Analyzing...")

    end = time.time()
    passed_time = float(end - start)
    num_of_secs = num_of_secs - passed_time
    print("remaining time: ", num_of_secs)

    epoch = epoch + 1

print("The time of detection process has expired.")
print("All output: ")
print(output)

    