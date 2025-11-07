import tkinter as tk
import random

# Functions

def displayMenu():
    clear_window()
    tk.Label(root, text="💫 ARITHMETIC CHALLENGE 💫", font=("Orbitron", 24, "bold"),
             bg="#1B0034", fg="#00FFFF").pack(pady=40)
    
    tk.Label(root, text="SELECT DIFFICULTY", font=("Arial", 14, "bold"),
             bg="#1B0034", fg="#FF00FF").pack(pady=10)
    
    tk.Button(root, text="Easy (1-digit)", command=lambda: start_quiz("easy"),
              font=("Arial", 12, "bold"), bg="#00FFFF", fg="#1B0034",
              activebackground="#FF00FF", activeforeground="#fff", width=20, height=2,
              relief="flat").pack(pady=10)
    
    tk.Button(root, text="Moderate (2-digit)", command=lambda: start_quiz("moderate"),
              font=("Arial", 12, "bold"), bg="#FF00FF", fg="#1B0034",
              activebackground="#00FFFF", activeforeground="#fff", width=20, height=2,
              relief="flat").pack(pady=10)
    
    tk.Button(root, text="Advanced (4-digit)", command=lambda: start_quiz("advanced"),
              font=("Arial", 12, "bold"), bg="#FFD700", fg="#1B0034",
              activebackground="#00FFFF", activeforeground="#fff", width=20, height=2,
              relief="flat").pack(pady=10)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def randomInt(difficulty):
    if difficulty == "easy":
        return random.randint(1, 9)
    elif difficulty == "moderate":
        return random.randint(10, 99)
    elif difficulty == "advanced":
        return random.randint(1000, 9999)

def decideOperation():
    return random.choice(['+', '-'])

def displayProblem():
    global current_answer, attempt, feedback_label, answer_entry
    
    clear_window()
    attempt = 1

    num1 = randomInt(selected_difficulty)
    num2 = randomInt(selected_difficulty)
    operation = decideOperation()
    current_answer = num1 + num2 if operation == '+' else num1 - num2

    tk.Label(root, text=f"QUESTION {question_number}/10", font=("Arial", 14, "bold"),
             bg="#1B0034", fg="#FFD700").pack(pady=10)
    tk.Label(root, text=f"{num1} {operation} {num2} =", font=("Orbitron", 36, "bold"),
             bg="#1B0034", fg="#00FFFF").pack(pady=30)
    
    answer_entry = tk.Entry(root, font=("Arial", 22, "bold"), width=8, justify="center",
                            bg="#0D0D0D", fg="#00FFFF", insertbackground="#00FFFF",
                            relief="flat")
    answer_entry.pack(pady=10)
    answer_entry.focus()

    tk.Button(root, text="SUBMIT", font=("Arial", 14, "bold"),
              bg="#FF00FF", fg="#fff", width=12, height=1, relief="flat",
              activebackground="#00FFFF", activeforeground="#1B0034",
              command=lambda: checkAnswer(answer_entry.get())).pack(pady=15)

    feedback_label = tk.Label(root, text="", font=("Arial", 14, "bold"),
                              bg="#1B0034", fg="#FFFFFF")
    feedback_label.pack(pady=10)

    score_label = tk.Label(root, text=f"SCORE: {score}", font=("Arial", 12, "bold"),
                           bg="#1B0034", fg="#FFD700")
    score_label.pack(side="bottom", pady=15)

def checkAnswer(answer):
    global score, question_number, attempt
    try:
        answer = int(answer)
    except ValueError:
        feedback_label.config(text="⚠️ Enter a valid number!", fg="#FF4444")
        return

    if answer == current_answer:
        if attempt == 1:
            score += 10
            feedback_label.config(text="🎉 Correct! +10 pts", fg="#00FF88")
        else:
            score += 5
            feedback_label.config(text="✅ Correct (2nd try)! +5 pts", fg="#66FF99")
        root.after(800, nextQuestion)
    else:
        if attempt == 1:
            attempt += 1
            feedback_label.config(text="❌ Wrong! Try again.", fg="#FF4444")
            answer_entry.delete(0, tk.END)
        else:
            feedback_label.config(text=f"💀 Wrong again! Answer: {current_answer}", fg="#FF4444")
            root.after(1000, nextQuestion)

def nextQuestion():
    global question_number
    question_number += 1
    if question_number > 10:
        displayResults()
    else:
        displayProblem()

def displayResults():
    clear_window()
    grade = calculateGrade(score)
    
    tk.Label(root, text="🏁 GAME OVER 🏁", font=("Orbitron", 26, "bold"),
             bg="#1B0034", fg="#FF00FF").pack(pady=30)
    tk.Label(root, text=f"FINAL SCORE: {score}/100", font=("Arial", 18, "bold"),
             bg="#1B0034", fg="#00FFFF").pack(pady=10)
    tk.Label(root, text=f"RANK: {grade}", font=("Arial", 18, "bold"),
             bg="#1B0034", fg="#FFD700").pack(pady=10)
    
    tk.Button(root, text="PLAY AGAIN 🎮", command=displayMenu, font=("Arial", 14, "bold"),
              bg="#00FFFF", fg="#1B0034", width=15, relief="flat").pack(pady=20)
    tk.Button(root, text="EXIT", command=root.destroy, font=("Arial", 14, "bold"),
              bg="#FF00FF", fg="#fff", width=15, relief="flat").pack()

def calculateGrade(score):
    if score >= 90:
        return "A+ 🌟"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F ❌"

def start_quiz(difficulty):
    global selected_difficulty, score, question_number
    selected_difficulty = difficulty
    score = 0
    question_number = 1
    displayProblem()

# GUI Setup

root = tk.Tk()
root.title("Neon Arcade Arithmetic Quiz")
root.geometry("650x550")
root.config(bg="#1B0034")

displayMenu()
root.mainloop()