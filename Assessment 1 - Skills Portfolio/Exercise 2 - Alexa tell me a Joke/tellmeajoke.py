import tkinter as tk
import random

# Load Jokes From File
def load_jokes():
    jokes = []
    with open("randomJokes.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline))
    return jokes

jokes = load_jokes()


# Main App
def new_joke():
    global current_setup, current_punchline
    current_setup, current_punchline = random.choice(jokes)
    setup_label.config(text=current_setup)
    punchline_label.config(text="")   # hide punchline


def show_punchline():
    punchline_label.config(text=current_punchline)


# Tkinter Window
root = tk.Tk()
root.title("Alexa tell me a Joke")
root.geometry("500x300")

# Widgets
setup_label = tk.Label(root, text="Click the button to hear a joke!", font=("Arial", 14))
setup_label.pack(pady=10)

punchline_label = tk.Label(root, text="", font=("Arial", 14, "italic"))
punchline_label.pack(pady=10)


# Buttons
tell_joke_btn = tk.Button(root, text="Alexa tell me a Joke", command=new_joke)
tell_joke_btn.pack(pady=5)

punchline_btn = tk.Button(root, text="Show Punchline", command=show_punchline)
punchline_btn.pack(pady=5)

next_btn = tk.Button(root, text="Next Joke", command=new_joke)
next_btn.pack(pady=5)

quit_btn = tk.Button(root, text="Quit", command=root.destroy)
quit_btn.pack(pady=10)

# Run
root.mainloop()
