import speech_recognition as sr
import pyttsx3
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['contact']  # Replace with your database name

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Could not request results; check your network connection.")
        return ""

def add_contact(name, phone):
    """Add a contact to the MongoDB database."""
    db.contacts.insert_one({"name": name, "phone": phone})
    speak(f"Contact {name} added successfully.")

def list_contacts():
    """List all contacts from the MongoDB database."""
    contacts = db.contacts.find()
    if contacts.count() == 0:
        speak("No contacts found.")
    else:
        for contact in contacts:
            print(f"Name: {contact['name']}, Phone: {contact['phone']}")
            speak(f"Name: {contact['name']}, Phone: {contact['phone']}")

def main():
    speak("Welcome to the contact book.")
    while True:
        speak("Please say a command: add contact, list contacts, or exit. Or type your command.")
        
        command = listen() or input("Type your command: ").strip().lower()

        if "add contact" in command:
            speak("Please say the name of the contact or type it.")
            name = listen() or input("Type the name of the contact: ").strip()
            speak("Please say the phone number or type it.")
            phone = listen() or input("Type the phone number: ").strip()
            add_contact(name, phone)
        elif "list contacts" in command:
            list_contacts()
        elif "exit" in command:
            speak("Exiting the contact book.")
            break
        else:
            speak("Sorry, I did not understand the command.")

if __name__ == "__main__":
    main()
