import os
import shlex
import speech_recognition as sr
import webbrowser
import datetime
import google.generativeai as genai  # Import Google Gemini SDK
from config import gemini_api_key  # Store API key in config.py

# Configure the Gemini API
genai.configure(api_key=gemini_api_key)

def chat(query, chat_session):
    try:
        # Send the query to Gemini and get the response
        print(f"Sending query: {query}")
        response = chat_session.send_message(query)

        # Check and return the response text
        if response.text:
            print(f"Gemini says: {response.text}")
            say(response.text)  # Optional: Use text-to-speech for the response
            return response.text
        else:
            print("No response received from Gemini.")
            say("I couldn't understand that. Please try again.")
            return None

    except Exception as e:
        print("Error communicating with Gemini:", e)
        say("There was an error communicating with Gemini. Please try again later.")
        return None

def say(text):
    try:
        # Use shlex.quote() to properly escape the text for shell execution
        safe_text = shlex.quote(text)
        os.system(f"/usr/bin/say {safe_text}")
    except Exception as e:
        print(f"Error in say function: {e}")

# def say(text):
#     os.system(f"/usr/bin/say {text}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing..")
            query = r.recognize_google(audio, language="en-US")
            print(f"user said: {query}")
            return query
        except Exception as e:
            print("Error:", e)
            say("Sorry, I couldn't understand that. Please try again.")
            return None

if __name__ == '__main__':
    print('Pycharm')
    say("Hello, I am your personal assistant. Let's chat!")

    # Start a new chat session with Gemini
    model = genai.GenerativeModel("gemini-pro")
    chat_session = model.start_chat(history=[])  # Starting with an empty history

    while True:
        print("Listening...")
        query = takeCommand()

        # Check if query is None before proceeding
        if query is not None:
            # Add user input to the conversation history
            chat_session.history.append({
                "role": "user",
                "parts": [query],
            })

            if "exit" in query.lower():
                say("Goodbye! Ending the conversation.")
                print("Exiting conversation.")
                break  # Exit the loop and end the conversation

            # Process commands like opening websites or apps
            sites = [
                ["youtube", "https://www.youtube.com"],
                ["linkedin", "https://www.linkedin.com"],
                ["google", "https://www.google.com"],
                ["gmail", "https://www.gmail.com"],
            ]

            for site in sites:
                if f"open {site[0]}" in query.lower():
                    say(f"Opening {site[0]} for you..")
                    webbrowser.open(site[1])

            if "open music" in query:
                musicPath = "/Users/samakshgupta/Downloads/music.mp3"
                os.system(f"open {musicPath}")

            if "what's the time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"The time is {strfTime}")

            if "open zoom" in query.lower():
                os.system(f"open /Applications/Zoom.us.app")

            # If the user wants to use Gemini AI for general conversation
            elif "using gemini" in query.lower():
                say("Sure, let me assist you with Gemini.")
                chat(query, chat_session)  # Send the query to Gemini

            else:
                # Otherwise, continue general conversation with Gemini
                # say("Let's talk!")
                chat(query, chat_session)  # Send the query to Gemini
        else:
            print("No query recognized. Retrying...")
