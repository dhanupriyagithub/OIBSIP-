import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import speech_recognition as sr
import yagmail
import spacy
import requests
import smtplib

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        Listening='Listening'
        speak(Listening)
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        Recognizing='Recognizing'
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def respond_to_greeting(query):
    greetings = ["hello", "hi", "hey"]
    response = "Hello! How can I help you today?"

    if any(greeting in query for greeting in greetings):
        speak(response)
    else:
        speak("I'm sorry, I didn't catch that.")

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    print(f"The current time is {current_time}")
    speak(f"The current time is {current_time}")

def tell_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"Today's date is {current_date}")
    speak(f"Today's date is {current_date}")

def search_web(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Here are the search results for {query}")

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # You can change this to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {city} is {description} with a temperature of {temperature} degrees Celsius."
        else:
            return f"Unable to fetch weather data. Error: {data['message']}"

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def handle_voice_command(command,city_name):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(command)

    if not city_name:
        for ent in doc.ents:
            if ent.label_ == "GPE":
                city_name = ent.text
                break

    if city_name:
        weather_info = get_weather("26da47f536ad060fb62d3bde1ddb3e35", city_name)
        print(weather_info)
        speak(weather_info)
    else:
        speak("Please specify a valid city for the weather.")



def process_voice_message():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print('Say something....')
            recorded_audio = recognizer.listen(source)
            print('Done...')
        
        text = recognizer.recognize_google(recorded_audio, language='en-US')
        print('Message: {}'.format(text))
        print('Voice message received')

        if text:
            receiver = 'dhanupriyaworkid@gmail.com'
            email_content = {
                'subject': 'Message sent from VoiceAssistant',
                'contents': [{'type': 'text/plain', 'content': text}]
            }
            sender = yagmail.SMTP('dhanupriyademootk@gmail.com', password='pabu ueui iyom knab')
            sender.send(to=receiver, **email_content)
            mail='Mail sent successfully'
            speak(mail)
            print('Mail sent successfully!')
        else:
            print('No text to send in the email.')

    except sr.UnknownValueError:
        print('Speech recognition could not understand audio')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))
    except Exception as ex:
        print('An error occurred during speech recognition: {0}'.format(ex))


if __name__ == "__main__":
    speak("Hello! I am your voice assistant.")

    while True:
        command = listen().lower()

        if any(greeting in command for greeting in ["hello", "hi", "hey"]):
            respond_to_greeting(command)
        elif "time" in command or "tell me the time" in command:
            tell_time()
        elif "date" in command or "tell me the date" in command:
            tell_date()
        elif "email" in command or "send email" in command:
            process_voice_message()
        elif "search" in command:
            search_query = command.replace("search", "").strip()
            search_web(search_query)
        elif "weather" in command:
            city_index = command.find("in") + 2
            city_name = command[city_index:].strip() if city_index > 1 else None
            handle_voice_command(command, city_name)
        elif "exit" in command:
            speak("Goodbye! Have a great day.")
            exit()



