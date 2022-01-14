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

from guizero import App, Text, TextBox, PushButton, Slider

# Replace with valid values
ENDPOINT = "https://jonathanazureraspiproject-prediction.cognitiveservices.azure.com/"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/GPS-Intern-Jonathan-RaspixAzure-Project/providers/Microsoft.CognitiveServices/accounts/JonathanAzureRaspiProject-Prediction"
iteration_name = "FacialExpression"
prediction_key = "62375fe7e72e48aaaa9290a62c02f86f"
project_id = "cf9c1adc-0a51-42b0-b7a1-ae75e01b698c"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# read the absolute path
script_dir = os.path.dirname(os.path.realpath(__file__))

output = []

def change():
    working_message = Text(app2, text="Analyzing...", size = 20, font = "Noto Sans", color = "darkblue")
    stop = PushButton(app2, image = "stop.png", command = pause)
    app2.show()
    return analyze()

def check():
    print("yyoyo")
    print("All output: ")
    print(output)

def pause():
    return check()

def analyze():

    while True:

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
                    print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
                else:
                    break
                count = count + 1

        print("Analyzing...")

app = App(title="Emotion Recognizer", height = 150, width = 500)
welcome_message = Text(app, text="Welcome to Emotion Recognizer! :)", size = 20, font = "Noto Sans", color = "darkblue")
run = PushButton(app, image = "start.jpg", command = change)

app2 = App(title="Analyzing...", height = 500, width = 500)
app2.hide()

app.display()