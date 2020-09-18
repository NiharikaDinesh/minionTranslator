
from flask import Flask, render_template
import speech_recognition as sr
import pyttsx3
from words import words
minionese_to_english = {v: k for k, v in words.items()}
app = Flask(__name__)

r = sr.Recognizer()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/trans')
def translator(command):
    engine = pyttsx3.init()
    engine.setProperty('rate', 145)
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.say(command)
    engine.runAndWait()


@app.route('/home')
def meaning():
    while (1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                mytext = r.recognize_google(audio2)
                mytext = mytext.lower()
                print(mytext)
                mytext=translate(mytext, False)
                print(mytext)
                translator(mytext)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")


def translate(sentence, minionese=False):
    dictionary = words if not minionese else minionese_to_english
    result = ""
    for word in sentence.split(" "):
        if word in dictionary.keys():
            result += dictionary[word] + " "
        else:
            result += word + " "

    return result[:-1]


if __name__ == '__main__':
    app.run(debug=True)
