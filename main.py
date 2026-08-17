import os
import webbrowser
import urllib.parse
from datetime import datetime
from getpass import getpass

CORRECT_NAME = "Aman"
CORRECT_PASSWORD = "aman ji"

name = input("Enter your name: ").strip()

if name.lower() != CORRECT_NAME.lower():
    print("Jarvis: Wrong name. Access denied.")
    raise SystemExit

password = getpass("Enter password: ")

if password != CORRECT_PASSWORD:
    print("Jarvis: Wrong password. Access denied.")
    raise SystemExit

print("Jarvis: Login successful!")

print("================================")
print("        JARVIS AI")
print("================================")
print("Type a command. Type 'help' for commands.")
print()

while True:
    command = input("You: ").strip()

    if not command:
        continue

    cmd = command.lower()


    # Exit
    if cmd in ["exit", "quit", "bye"]:
        print("Jarvis: Goodbye!")
        break

    # Help
    elif cmd == "help":
        print("""
Jarvis commands:

open notepad
open calculator
open youtube
open google
open gmail
search <your question>
time
date
clear
exit
""")

    # Apps
    elif cmd == "open notepad":
        os.system("notepad")
        print("Jarvis: Opening Notepad...")

    elif cmd == "open calculator":
        os.system("start calc")
        print("Jarvis: Opening Calculator...")

    # Websites
    elif cmd == "open youtube":
        webbrowser.open("https://www.youtube.com")
        print("Jarvis: Opening YouTube...")

    elif cmd == "open google":
        webbrowser.open("https://www.google.com")
        print("Jarvis: Opening Google...")

    elif cmd == "open gmail":
        webbrowser.open("https://mail.google.com")
        print("Jarvis: Opening Gmail...")

    elif cmd == "open instagram":
        webbrowser.open("https://www.instagram.com")
        print("Jarvis: Opening Instagram...")

    elif cmd == "open youtube music":
        webbrowser.open("https://music.youtube.com")
        print("Jarvis: Opening YouTube Music...")

    elif cmd == "open jiohotstar":
        webbrowser.open("https://www.hotstar.com")
        print("Jarvis: Opening JioHotstar...")

    elif cmd == "open spotify":
        webbrowser.open("https://open.spotify.com")
        print("Jarvis: Opening Spotify...")

    elif cmd == "open whatsapp":
        webbrowser.open("https://web.whatsapp.com")
        print("Jarvis: Opening WhatsApp...")

    elif cmd == "open chrome":
        os.system("start chrome")
        print("Jarvis: Opening Chrome...")
       
    # Search
    elif cmd.startswith("search "):
        query = command[7:].strip()

        if query:
            url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
            webbrowser.open(url)
            print("Jarvis: Searching for " + query)
        else:
            print("Jarvis: Tell me what to search.")

    # Time
    elif cmd == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        print("Jarvis: The time is " + current_time)

    # Date
    elif cmd == "date":
        current_date = datetime.now().strftime("%d %B %Y")
        print("Jarvis: Today is " + current_date)

    # Clear terminal
    elif cmd == "clear":
        os.system("cls")
        print("Jarvis: Terminal cleared.")

    # Unknown command
    else:
        print("Jarvis: I don't know that command yet.")
        print("Jarvis: Type 'help' to see what I can do.")
        