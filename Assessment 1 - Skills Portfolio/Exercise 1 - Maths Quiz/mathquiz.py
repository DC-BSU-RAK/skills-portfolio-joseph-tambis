import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import pygame

WINDOW_W, WINDOW_H = 650, 550
BG_FILE = "mathquiz_bg.png"  # Background image for the quiz
BTN_FILE = "button_retro.png"  # Button image (retro style)

selected_difficulty = None
score = 0
question_number = 1
attempt = 1
current_answer = None

# 🎵 Set up pygame to handle music and sound effects
pygame.mixer.init()

# Load background music and set it to loop forever
pygame.mixer.music.load("mathquiz_bg_music.wav")  # Background music file
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load sound effects for feedback
sfx_correct = pygame.mixer.Sound("correct.wav")
sfx_wrong = pygame.mixer.Sound("wrong.wav")
sfx_finish = pygame.mixer.Sound("finish.wav")

# Create main window
root = tk.Tk()
root.title("Retro Math Quiz")
root.geometry(f"{WINDOW_W}x{WINDOW_H}")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')
root.iconbitmap("mathquiz.ico")  # Window icon

# Canvas to handle all drawing
canvas = tk.Canvas(root, width=WINDOW_W, height=WINDOW_H, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

# Load images
bg_img = Image.open(BG_FILE).resize((WINDOW_W, WINDOW_H))
bg_photo = ImageTk.PhotoImage(bg_img)

btn_img = Image.open(BTN_FILE)
BTN_W, BTN_H = 220, 44
btn_photo = ImageTk.PhotoImage(btn_img.resize((BTN_W, BTN_H)))

# Draw the background image on the canvas
bg_id = canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Keep track of all items drawn on canvas so we can clear them easily
screen_items = []
feedback_text_id = None  # Track the feedback text for easy deletion

# Function to clear the screen and remove any active widgets
def clear_screen():
    global screen_items, feedback_text_id
    for item in screen_items:
        canvas.delete(item)
    screen_items = []
    
    # Remove entry widgets and unbind the Enter key
    for win_id in canvas.find_withtag("entry_widget"):
        entry_widget = canvas.itemcget(win_id, "window")
        if entry_widget:
            widget = root.nametowidget(entry_widget)
            widget.unbind("<Return>")
        canvas.delete(win_id)

    feedback_text_id = None

# Utility to create buttons on canvas with image + text
def create_canvas_button(text, x, y, command, font=("Segoe UI", 10, "bold")):
    img_id = canvas.create_image(x, y, image=btn_photo)
    text_id = canvas.create_text(x, y, text=text, font=font, fill="#1B0034")
    screen_items.extend([img_id, text_id])

    # Bind the mouse click to the button image and text
    def click(event):
        command()
    canvas.tag_bind(img_id, "<Button-1>", click)
    canvas.tag_bind(text_id, "<Button-1>", click)

    return img_id, text_id

# Generate a random number based on difficulty
def randomInt(d):
    if d == "easy":
        return random.randint(1, 9)
    if d == "moderate":
        return random.randint(10, 99)
    return random.randint(1000, 9999)

# Randomly choose + or - for the problem
def decideOperation():
    return random.choice(['+', '-'])

# Display the main menu with difficulty options
def displayMenu():
    clear_screen()
    t1 = canvas.create_text(WINDOW_W//2, 140, text="💫 RETRO MATH QUIZ 💫",
                             font=("Orbitron", 28, "bold"), fill="#00FFFF")
    t2 = canvas.create_text(WINDOW_W//2, 200, text="SELECT DIFFICULTY",
                             font=("Arial", 14, "bold"), fill="#FF00FF")
    screen_items.extend([t1, t2])

    y = 230
    create_canvas_button("Easy (1-digit)", WINDOW_W//2, y+40, lambda: start_quiz("easy"))
    create_canvas_button("Moderate (2-digit)", WINDOW_W//2, y+90, lambda: start_quiz("moderate"))
    create_canvas_button("Advanced (4-digit)", WINDOW_W//2, y+140, lambda: start_quiz("advanced"))
    create_canvas_button("QUIT", WINDOW_W//2, y+190, lambda: root.destroy())

# Display a temporary feedback message (correct/wrong)
def show_feedback(msg, color="#FFFFFF"):
    global feedback_text_id
    if feedback_text_id is not None:
        canvas.delete(feedback_text_id)
    feedback_text_id = canvas.create_text(WINDOW_W//2, 370, text=msg, font=("Arial", 14, "bold"), fill=color)
    screen_items.append(feedback_text_id)

# IDs to keep track of current question, score, and entry widget
question_text_id = None
score_text_id = None
entry_window_id = None

# Display a math problem based on selected difficulty
def displayProblem():
    global question_text_id, score_text_id, entry_window_id, attempt, current_answer
    clear_screen()
    attempt = 1

    num1 = randomInt(selected_difficulty)
    num2 = randomInt(selected_difficulty)
    op = decideOperation()
    current_answer = num1 + num2 if op == '+' else num1 - num2

    # Show question number
    h = canvas.create_text(WINDOW_W//2, 70, text=f"QUESTION {question_number}/10",
                           font=("Arial", 16, "bold"), fill="#FFD700")
    # Show the math problem
    q = canvas.create_text(WINDOW_W//2, 170, text=f"{num1} {op} {num2} =",
                           font=("Orbitron", 40, "bold"), fill="#00FFFF")
    screen_items.extend([h, q])
    question_text_id = q

    # Create entry for user answer
    entry = tk.Entry(root, font=("Arial", 20, "bold"), width=8,
                 justify="center", bg="#2A0033", fg="#00FFFF",
                 insertbackground="#00FFFF", relief="flat",
                 highlightthickness=2, highlightbackground="#2A0033",
                 highlightcolor="#2A0033", bd=5)
    entry_window_id = canvas.create_window(WINDOW_W//2, 260, window=entry, width=180, height=40)
    canvas.addtag_withtag("entry_widget", entry_window_id)

    # Submit button for the answer
    create_canvas_button("SUBMIT", WINDOW_W//2, 320,
                         lambda e=entry: checkAnswer(e.get()))

    # Show current score at the bottom
    score_text_id = canvas.create_text(WINDOW_W//2, WINDOW_H-30,
                                       text=f"SCORE: {score}",
                                       font=("Arial", 12, "bold"), fill="#FFD700")
    screen_items.append(score_text_id)

    # Focus the entry field and allow Enter key
    entry.focus()
    entry.bind("<Return>", lambda event: checkAnswer(entry.get()))

# Check if the answer is correct
def checkAnswer(a):
    global score, question_number, attempt

    try:
        val = int(a)
    except:
        show_feedback("⚠ Enter a valid number!", "#FF4444")
        sfx_wrong.play()
        return

    if val == current_answer:
        if attempt == 1:
            score += 10
            show_feedback("🎉 Correct! +10", "#00FF88")
        else:
            score += 5
            show_feedback("✅ Correct! +5", "#66FF99")
        sfx_correct.play()

        # Update score display
        canvas.delete(score_text_id)
        new_scr = canvas.create_text(WINDOW_W//2, WINDOW_H-30,
                                     text=f"SCORE: {score}",
                                     font=("Arial", 12, "bold"), fill="#FFD700")
        screen_items.append(new_scr)

        # Move to next question after a short delay
        root.after(800, nextQuestion)
        return

    # First wrong attempt
    if attempt == 1:
        attempt += 1
        show_feedback("❌ Wrong! Try again.", "#FF4444")
        sfx_wrong.play()
        for child in root.winfo_children():
            if isinstance(child, tk.Entry):
                child.delete(0, tk.END)
                child.focus()
        return

    # Second wrong attempt, show correct answer
    show_feedback(f"💀 Wrong again! {current_answer}", "#FF4444")
    sfx_wrong.play()
    root.after(1000, nextQuestion)

# Move to the next question or end quiz
def nextQuestion():
    global question_number
    question_number += 1
    if question_number > 10:
        displayResults()
    else:
        displayProblem()

# Display final score and rank
def displayResults():
    clear_screen()
    show_feedback("")  # Remove any lingering messages
    t = canvas.create_text(WINDOW_W//2, 110, text="QUIZ OVER",
                           font=("Orbitron", 30, "bold"), fill="#FF00FF")
    s = canvas.create_text(WINDOW_W//2, 190, text=f"FINAL SCORE: {score}/100",
                           font=("Arial", 20, "bold"), fill="#00FFFF")
    g = canvas.create_text(WINDOW_W//2, 240, text=f"RANK: {calculateGrade(score)}",
                           font=("Arial", 20, "bold"), fill="#FFD700")
    screen_items.extend([t, s, g])

    sfx_finish.play()

    create_canvas_button("PLAY AGAIN", WINDOW_W//2, 340, displayMenu)
    create_canvas_button("EXIT", WINDOW_W//2, 400, root.destroy)

# Calculate letter grade based on score
def calculateGrade(s):
    if s >= 90: return "A+ 🌟"
    if s >= 80: return "A"
    if s >= 70: return "B"
    if s >= 60: return "C"
    if s >= 50: return "D"
    return "F ❌"

# Start the quiz with chosen difficulty
def start_quiz(d):
    global selected_difficulty, score, question_number
    selected_difficulty = d
    score = 0
    question_number = 1
    displayProblem()

# Launch the main menu
displayMenu()
root.mainloop()
