import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize pyttsx3
engine = pyttsx3.init()

# Configure the voice
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name} - Language: {voice.languages}")
engine.setProperty('voice', voices[0].id)  # Select a voice (change the index to switch voice)
engine.setProperty('rate', 135)  # Moderate speed
engine.setProperty('volume', 0.9)  # High volume

# Introductory part
intro_text = (
    "Hello! I am Jarvis, your virtual assistant. "
    "I am ready to assist you with anything you need. "
    "You can talk to me anytime."
)
print("Jarvis: " + intro_text)
engine.say(intro_text)
engine.runAndWait()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
messages = [{"role": "system", "content": "Your name is Jarvis and you provide answers in 2 lines"}]

def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        chatgpt_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": chatgpt_reply})
        return chatgpt_reply
    except Exception as e:
        print(f"Error during API call: {e}")
        return "I'm sorry, an error occurred while retrieving the response."

def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5.0)
                user_input = recognizer.recognize_google(audio, language='it-IT')
                print(f"User: {user_input}")
                response_from_openai = get_response(user_input)
                print(f"Jarvis: {response_from_openai}")
                engine.say(response_from_openai)
                engine.runAndWait()
            except sr.UnknownValueError:
                print("I didn't recognize anything.")
            except sr.RequestError:
                print("Request error; check your internet connection.")
            except KeyboardInterrupt:
                print("Manual program interruption.")
                break

if __name__ == "__main__":
    main()
