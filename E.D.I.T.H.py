import speech_recognition as sr
from gtts import gTTS
import os
from openai import OpenAI
import pyttsx3
client = OpenAI(api_key="YOUR_OPENAPI_KEY", )

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to convert speech to text
def speech_to_text():
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

def generate_chat_response(text):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": text},
    ]
    )
    return str(response.choices[0].message.content)

def text_to_speech(text):
    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # print(voices)
    # engine.setProperty('voice', voices[0].id)
    # engine.say(text)
    # engine.runAndWait()
    tts = gTTS(text, lang='en-uk', slow=False)
    tts.save("output.mp3")
    os.system("mpg123 output.mp3")  # Linux command for playing audio (You may need to install mpg123)

while True:
    choice = input("Choose an option (1 - Speech to Text, 2 - Text to Speech, q - Quit): ")
    
    if choice == '1':
        text = speech_to_text()
        response = generate_chat_response(text)
        print("ChatGPT Response: " + response)
        text_to_speech(response)
    elif choice == '2':
        text = input("Enter the text to convert to speech: ")
        text_to_speech(text)
    elif choice.lower() == 'q':
        break
    else:
        print("Invalid choice. Please try again.")
