from guizero import App, Text, TextBox, PushButton, Slider

def check():
    print("yyoyo")

def pause():
    return check()

def output():
    app = App(title="Emotion Recognizer", height = 500, width = 500)
    working_message = Text(app, text="Analyzing...", size = 20, font = "Noto Sans", color = "darkblue")
    stop = PushButton(app, image = "stop.png", command = pause)
    while True:
        print("A picture button was pressed")


app = App(title="Emotion Recognizer", height = 150, width = 500)
welcome_message = Text(app, text="Welcome to Emotion Recognizer! :)", size = 20, font = "Noto Sans", color = "darkblue")
run = PushButton(app, image = "start.jpg", command = output)
app.display()