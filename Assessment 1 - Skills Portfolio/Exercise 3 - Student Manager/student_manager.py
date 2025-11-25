import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
from PIL import Image, ImageTk
import os

FILE = "studentMarks.txt"

# ---------- Data handling ----------
def load_data():
    students = []
    if not os.path.exists(FILE):
        # Custom messagebox with icon
        show_custom_message("File missing", f"'{FILE}' not found.", "error")
        return students
    with open(FILE, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines() if ln.strip() != ""]
    if not lines:
        return students
    for line in lines[1:]:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 6:
            continue
        code = parts[0]
        name = parts[1]
        try:
            c1, c2, c3 = int(parts[2]), int(parts[3]), int(parts[4])
            exam = int(parts[5])
        except ValueError:
            continue
        coursework_total = c1 + c2 + c3
        overall_total = coursework_total + exam
        percentage = (overall_total / 160) * 100
        grade = calc_grade(percentage)
        students.append({
            "code": code,
            "name": name,
            "c1": c1,
            "c2": c2,
            "c3": c3,
            "coursework": coursework_total,
            "exam": exam,
            "total": overall_total,
            "percentage": percentage,
            "grade": grade
        })
    return students

def save_data(students):
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

def calc_grade(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

def format_student(s, header=""):
    lines = []
    if header:
        lines.append(header)
    lines.append(f"Name: {s['name']}")
    lines.append(f"Student Number: {s['code']}")
    lines.append(f"Coursework Marks: {s['c1']}, {s['c2']}, {s['c3']}  (Total: {s['coursework']}/60)")
    lines.append(f"Exam Mark: {s['exam']}/100")
    lines.append(f"Overall Percentage: {s['percentage']:.2f}%")
    lines.append(f"Grade: {s['grade']}")
    lines.append("-" * 48)
    return "\n".join(lines) + "\n"

# ---------- Custom dialog functions with icons ----------
def show_custom_message(title, message, msg_type="info"):
    """Custom messagebox with icon"""
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("400x150")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    # Set icon
    try:
        dialog.iconbitmap("student_manager.ico")
    except:
        pass
    
    # Center dialog
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - dialog.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")
    
    # Message
    tk.Label(dialog, text=message, font=("Segoe UI", 10), wraplength=350, pady=15).pack()
    
    # OK button
    tk.Button(dialog, text="OK", command=dialog.destroy, 
              bg="#007acc", fg="white", font=("Segoe UI", 10), width=10).pack(pady=10)
    
    root.wait_window(dialog)

def ask_custom_yesno(title, question):
    """Custom yes/no dialog with icon"""
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("450x150")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    # Set icon
    try:
        dialog.iconbitmap("student_manager.ico")
    except:
        pass
    
    # Center dialog
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - dialog.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")
    
    result = {"value": None}
    
    def set_result(value):
        result["value"] = value
        dialog.destroy()
    
    # Question
    tk.Label(dialog, text=question, font=("Segoe UI", 10), wraplength=400, pady=15).pack()
    
    # Buttons
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Yes", command=lambda: set_result(True),
              bg="#4CAF50", fg="white", font=("Segoe UI", 10), width=8).pack(side="left", padx=10)
    tk.Button(btn_frame, text="No", command=lambda: set_result(False),
              bg="#f44336", fg="white", font=("Segoe UI", 10), width=8).pack(side="left", padx=10)
    
    root.wait_window(dialog)
    return result["value"]

def custom_askstring(title, prompt):
    """Custom string input dialog with icon"""
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("400x150")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    # Set icon
    try:
        dialog.iconbitmap("student_manager.ico")
    except:
        pass
    
    # Center dialog
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - dialog.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")
    
    result = {"value": None}
    
    def submit():
        result["value"] = entry.get()
        dialog.destroy()
    
    # Prompt
    tk.Label(dialog, text=prompt, font=("Segoe UI", 10), pady=10).pack()
    
    # Entry field
    entry = tk.Entry(dialog, font=("Segoe UI", 10), width=40)
    entry.pack(pady=10)
    entry.focus_set()
    
    # Buttons
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="OK", command=submit,
              bg="#007acc", fg="white", font=("Segoe UI", 10), width=8).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
              bg="#666", fg="white", font=("Segoe UI", 10), width=8).pack(side="left", padx=5)
    
    # Bind Enter key to submit
    entry.bind('<Return>', lambda e: submit())
    
    root.wait_window(dialog)
    return result["value"]

def custom_askinteger(title, prompt, **kwargs):
    """Custom integer input dialog with icon"""
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("450x180")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    # Set icon
    try:
        dialog.iconbitmap("student_manager.ico")
    except:
        pass
    
    # Center dialog
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - dialog.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")
    
    result = {"value": None}
    
    def submit():
        try:
            value = int(entry.get())
            if 'minvalue' in kwargs and value < kwargs['minvalue']:
                show_custom_message("Invalid Input", f"Value must be at least {kwargs['minvalue']}", "error")
                return
            if 'maxvalue' in kwargs and value > kwargs['maxvalue']:
                show_custom_message("Invalid Input", f"Value must be at most {kwargs['maxvalue']}", "error")
                return
            result["value"] = value
            dialog.destroy()
        except ValueError:
            show_custom_message("Invalid Input", "Please enter a valid number", "error")
            entry.focus_set()
    
    # Prompt with range info
    range_text = ""
    if 'minvalue' in kwargs and 'maxvalue' in kwargs:
        range_text = f" ({kwargs['minvalue']}-{kwargs['maxvalue']})"
    
    tk.Label(dialog, text=prompt + range_text, font=("Segoe UI", 10), pady=10).pack()
    
    # Entry field
    entry = tk.Entry(dialog, font=("Segoe UI", 10), width=20)
    entry.pack(pady=10)
    entry.focus_set()
    
    # Buttons
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="OK", command=submit,
              bg="#007acc", fg="white", font=("Segoe UI", 10), width=8).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
              bg="#666", fg="white", font=("Segoe UI", 10), width=8).pack(side="left", padx=5)
    
    # Bind Enter key to submit
    entry.bind('<Return>', lambda e: submit())
    
    root.wait_window(dialog)
    return result["value"]

# ---------- UI actions ----------
def set_output(text):
    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", text)
    output_text.config(state="disabled")

def view_all():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    out = []
    total_pct = 0
    for s in students:
        out.append(format_student(s))
        total_pct += s["percentage"]
    avg = total_pct / len(students)
    out.append(f"\nTotal students: {len(students)}")
    out.append(f"Class Average Percentage: {avg:.2f}%")
    set_output("\n".join(out))

def view_individual():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    key = custom_askstring("Find student", "Enter student number or name (partial ok):")
    if not key:
        return
    keyl = key.strip().lower()
    for s in students:
        if keyl == s["code"].lower() or keyl in s["name"].lower():
            set_output(format_student(s, header="Student Record:"))
            return
    show_custom_message("Not found", "No matching student found.")

def highest_score():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    best = max(students, key=lambda x: x["percentage"])
    set_output(format_student(best, header="Highest Scoring Student:"))

def lowest_score():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    worst = min(students, key=lambda x: x["percentage"])
    set_output(format_student(worst, header="Lowest Scoring Student:"))

def sort_records():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    
    # Create custom dialog for sort order
    dialog = tk.Toplevel(root)
    dialog.title("Sort Order")
    dialog.geometry("400x150")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    # Set icon
    try:
        dialog.iconbitmap("student_manager.ico")
    except:
        pass
    
    # Center dialog
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - dialog.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")
    
    result = {"ascending": None}
    
    def set_ascending(value):
        result["ascending"] = value
        dialog.destroy()
    
    # Dialog content
    tk.Label(dialog, text="Choose sort order:", font=("Segoe UI", 11), pady=15).pack()
    
    # Button frame
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    
    # Custom buttons with blue and grey styling to match other popups
    ascending_btn = tk.Button(btn_frame, text="Ascending", command=lambda: set_ascending(True),
                             bg="#007acc", fg="white", font=("Segoe UI", 10), width=10, padx=10)
    ascending_btn.pack(side="left", padx=10)
    
    descending_btn = tk.Button(btn_frame, text="Descending", command=lambda: set_ascending(False),
                              bg="#666", fg="white", font=("Segoe UI", 10), width=10, padx=10)
    descending_btn.pack(side="left", padx=10)
    
    # Wait for dialog to close
    root.wait_window(dialog)
    
    # Check if user closed dialog without choosing
    if result["ascending"] is None:
        return
    
    # Sort records
    students.sort(key=lambda x: x["percentage"], reverse=not result["ascending"])
    out = ["Sorted Student Records:\n"]
    for s in students:
        out.append(format_student(s))
    set_output("\n".join(out))

def add_student():
    students = load_data()
    code = custom_askstring("Add student", "Student code (1000-9999):")
    if not code:
        return
    if any(s["code"] == code for s in students):
        show_custom_message("Duplicate", "Student code already exists.", "error")
        return
    name = custom_askstring("Add student", "Full name:")
    if not name:
        return
    
    try:
        c1 = custom_askinteger("Add student", "Coursework mark 1:", minvalue=0, maxvalue=20)
        c2 = custom_askinteger("Add student", "Coursework mark 2:", minvalue=0, maxvalue=20)
        c3 = custom_askinteger("Add student", "Coursework mark 3:", minvalue=0, maxvalue=20)
        exam = custom_askinteger("Add student", "Exam mark:", minvalue=0, maxvalue=100)
    except Exception:
        show_custom_message("Input error", "Invalid marks.", "error")
        return
    
    if None in (c1, c2, c3, exam):
        return
    
    coursework_total = c1 + c2 + c3
    total = coursework_total + exam
    pct = (total / 160) * 100
    new = {
        "code": code, "name": name,
        "c1": c1, "c2": c2, "c3": c3,
        "coursework": coursework_total, "exam": exam,
        "total": total, "percentage": pct, "grade": calc_grade(pct)
    }
    students.append(new)
    save_data(students)
    show_custom_message("Added", "Student record added.")
    view_all()

def delete_student():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    key = custom_askstring("Delete student", "Enter student number or name:")
    if not key:
        return
    keyl = key.strip().lower()
    for i, s in enumerate(students):
        if keyl == s["code"].lower() or keyl in s["name"].lower():
            confirm = ask_custom_yesno("Confirm delete", f"Delete {s['name']} ({s['code']})?")
            if confirm:
                students.pop(i)
                save_data(students)
                show_custom_message("Deleted", "Student removed.")
                view_all()
            return
    show_custom_message("Not found", "No matching student found.")

def update_student():
    students = load_data()
    if not students:
        set_output("No student records found.")
        return
    key = custom_askstring("Update student", "Enter student number or name:")
    if not key:
        return
    keyl = key.strip().lower()
    for s in students:
        if keyl == s["code"].lower() or keyl in s["name"].lower():
            choice = custom_askstring("Update", "Which field to update? (name / c1 / c2 / c3 / exam)")
            if not choice:
                return
            choice = choice.strip().lower()
            fields = ["name", "c1", "c2", "c3", "exam"]
            if choice not in fields:
                show_custom_message("Invalid", "Field not recognised.", "error")
                return
            if choice == "name":
                newv = custom_askstring("Update", "Enter new full name:")
                if newv:
                    s["name"] = newv
            else:
                try:
                    if choice in ("c1","c2","c3"):
                        newv = custom_askinteger("Update", f"Enter new value for {choice}:", minvalue=0, maxvalue=20)
                    else:
                        newv = custom_askinteger("Update", "Enter new exam mark:", minvalue=0, maxvalue=100)
                except Exception:
                    show_custom_message("Input error", "Invalid mark.", "error")
                    return
                if newv is None:
                    return
                s[choice] = newv
            
            s["coursework"] = s["c1"] + s["c2"] + s["c3"]
            s["total"] = s["coursework"] + s["exam"]
            s["percentage"] = (s["total"] / 160) * 100
            s["grade"] = calc_grade(s["percentage"])
            save_data(students)
            show_custom_message("Updated", "Student record updated.")
            view_all()
            return
    show_custom_message("Not found", "No matching student found.")

# ---------- GUI layout ----------
root = tk.Tk()
root.title("Student Manager")
root.geometry("1080x620")
root.minsize(960, 560)

# Set window icon
try:
    root.iconbitmap("student_manager.ico")
except:
    print("Icon file 'student_manager.ico' not found. Using default icon.")

sidebar_bg = "#1e1e1e"
btn_bg = "#333333"
btn_hover = "#4d4d4d"
text_color = "#f5f5f5"
content_bg = "#f4f4f4"
border_color = "#c4c4c4"

title_font = font.Font(family="Segoe UI", size=15, weight="bold")
btn_font = font.Font(family="Segoe UI", size=10)
text_font = font.Font(family="Consolas", size=11)

# ---------- Frames ----------
sidebar = tk.Frame(root, bg=sidebar_bg, width=250)
sidebar.pack(side="left", fill="y")
content = tk.Frame(root, bg=content_bg)
content.pack(side="right", fill="both", expand=True)

header = tk.Frame(content, bg=content_bg)
header.pack(fill="x", pady=(15, 8))
title_lbl = tk.Label(header, text="Grades", bg=content_bg, fg="#111", font=title_font)
title_lbl.pack(anchor="w", padx=20)
subtitle = tk.Label(header, text="Manage coursework and exam scores", bg=content_bg, fg="#555")
subtitle.pack(anchor="w", padx=20)

# Output area
out_frame = tk.Frame(content, bg="#ffffff", bd=1, relief="solid")
out_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
output_text = tk.Text(out_frame, font=text_font, wrap="word", state="disabled", bd=0, padx=10, pady=10)
output_text.pack(side="left", fill="both", expand=True)
scroll = tk.Scrollbar(out_frame, command=output_text.yview)
scroll.pack(side="right", fill="y")
output_text.config(yscrollcommand=scroll.set)

# ---------- Sidebar logo (image placeholder) ----------
logo_frame = tk.Frame(sidebar, bg=sidebar_bg)
logo_frame.pack(pady=20,padx=20)
# placeholder logo.png
try:
    img = Image.open("logo.png")
    img = img.resize((50, 50))
    logo_img = ImageTk.PhotoImage(img)
    logo_lbl = tk.Label(logo_frame, image=logo_img, bg=sidebar_bg)
    logo_lbl.image = logo_img
    logo_lbl.pack(side="left", padx=10)
except:
    # Fallback if logo not found
    logo_lbl = tk.Label(logo_frame, text="LOGO", bg=sidebar_bg, fg=text_color, font=("Segoe UI", 12, "bold"))
    logo_lbl.pack(side="left", padx=10)
appname = tk.Label(logo_frame, text="Student\nManager", bg=sidebar_bg, fg=text_color, font=("Segoe UI", 16, "bold"))
appname.pack(side="left")

# ---------- Sidebar buttons ----------
def make_sidebar_button(parent, text, command):
    b = tk.Button(parent, text=text, command=command, bg=btn_bg, fg=text_color,
                  activebackground=btn_hover, relief="flat", bd=0, font=btn_font,
                  padx=18, pady=12, anchor="w")
    b.pack(fill="x", padx=18, pady=6)
    b.bind("<Enter>", lambda e: b.config(bg=btn_hover))
    b.bind("<Leave>", lambda e: b.config(bg=btn_bg))
    return b

make_sidebar_button(sidebar, "View All Students", view_all)
make_sidebar_button(sidebar, "View Individual", view_individual)
make_sidebar_button(sidebar, "Highest Score", highest_score)
make_sidebar_button(sidebar, "Lowest Score", lowest_score)
tk.Frame(sidebar, bg="#555", height=1).pack(fill="x", padx=18, pady=10)
make_sidebar_button(sidebar, "Sort Records", sort_records)
make_sidebar_button(sidebar, "Add Student", add_student)
make_sidebar_button(sidebar, "Delete Student", delete_student)
make_sidebar_button(sidebar, "Update Student", update_student)

# ---------- Welcome text ----------
set_output(
    "Welcome to Student Manager!\n\n"
    "Use the left menu to select an option.\n"
    "All output will appear here.\n"
)

root.mainloop()
