import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Inizializza pyttsx3
listening = True
engine = pyttsx3.init()

# Crea un'istanza del client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [{"role": "system", "content": "Il tuo nome è Jarvis e fornisci risposte in 2 righe"}]

# Personalizzazione della voce di output
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

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
        print(f"Errore durante la chiamata API: {e}")
        return "Mi dispiace, si è verificato un errore nel recupero della risposta."

while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Ascoltando...")
            audio = recognizer.listen(source, timeout=5.0)
            response = recognizer.recognize_google(audio, language='it-IT')
            print(response)

            response_from_openai = get_response(response)
            engine.setProperty('rate', 120)
            engine.setProperty('volume', volume)
            engine.say(response_from_openai)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Non ho riconosciuto nulla.")
        except sr.RequestError:
            print("Errore di richiesta; controlla la tua connessione internet.")
