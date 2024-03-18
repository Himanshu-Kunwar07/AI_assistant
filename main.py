import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np


speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatStr  = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Himanshu: {query}\n Jarvis:"
    response = openai.Completion.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = chatStr,
        temperature = 0.7,
        max_tokens = 256,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    #todo: Wrap tis inside of  a try catch block
    try:
        say(response["choices"][0]["text"])
        chatStr += f"{response['choice'][0]['text']}\n"
        return response["choices"][0]["text"]
    except Exception as e:
        return "some error Occure"


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        temperature = 0.7,
        max_tokens = 256,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    try:
        text += response["choice"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        with open(f"Openai/{''.join(prompt.spilt('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print("File not found")
def say(text):
    speaker.speak(text)
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language = "en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    print('Welome to Jarvis A.I')
    say("Jarvis AI")

    while True:

        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["Twitter", "https://www.twitter.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # say(query)
        if "open music" in query:
            musicPath = "G:\himanshu\Songs\download\Adele_Hello.mp3"
            os.system(f"start {musicPath}")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

        elif "open pass".lower() in query.lower():
            os.system(f"open /")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)

