from guizero import App, Text, TextBox

app = App(title="Facial Expression Recognizer")

welcome_message = Text(app, text="Welcome to Facial Expression Recognizer! :)", size = 30, font = "Times New Roman", color = "darkblue")

my_name = TextBox(app)

def say_my_name():
    welcome_message.value = my_name.value

app.display()