import tkinter as tk
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText

class StudentManager:
    def __init__(self):
        self.data = []

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                lines = f.read().strip().split("\n")
                for row in lines[1:]:
                    parts = row.split(",")
                    sid = parts[0]
                    name = parts[1]
                    m1, m2, m3 = map(int, parts[2:5])
                    exam = int(parts[5])

                    cw = m1 + m2 + m3
                    total = cw + exam
                    pct = (total / 160) * 100
                    grade = self.grade_for(pct)

                    self.data.append({
                        "id": sid,
                        "name": name,
                        "cw": cw,
                        "exam": exam,
                        "total": total,
                        "pct": pct,
                        "grade": grade
                    })
        except:
            pass

    def grade_for(self, p):
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("900x600")
        self.root.config(bg="#1e1e2f")

        self.manager = StudentManager()
        self.manager.load("studentMarks.txt")

        self.sidebar = tk.Frame(root, bg="#2b2b3c", width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="Student Manager", bg="#2b2b3c", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        btn = {
            "bg": "#4f5b93",
            "fg": "white",
            "activebackground": "#6573b4",
            "font": ("Arial", 12),
            "width": 20,
            "bd": 0,
            "height": 2
        }

        tk.Button(self.sidebar, text="View All Records", command=self.show_all, **btn).pack(pady=10)
        tk.Button(self.sidebar, text="View Individual", command=self.show_one, **btn).pack(pady=10)
        tk.Button(self.sidebar, text="Highest Score", command=self.show_max, **btn).pack(pady=10)
        tk.Button(self.sidebar, text="Lowest Score", command=self.show_min, **btn).pack(pady=10)

        self.output = ScrolledText(root, font=("Consolas", 12), bg="#f5f5f5",
                                   width=70, height=30)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def block(self, s):
        return (
            f"Name: {s['name']}\n"
            f"Student Number: {s['id']}\n"
            f"Coursework Total: {s['cw']} / 60\n"
            f"Exam Mark: {s['exam']} / 100\n"
            f"Overall %: {s['pct']:.2f}%\n"
            f"Grade: {s['grade']}\n"
            f"{'-'*50}\n"
        )

    def show_all(self):
        self.output.delete("1.0", tk.END)
        total_pct = 0

        for s in self.manager.data:
            self.output.insert(tk.END, self.block(s))
            total_pct += s["pct"]

        avg = total_pct / len(self.manager.data)
        self.output.insert(tk.END, f"\nTotal Students: {len(self.manager.data)}")
        self.output.insert(tk.END, f"\nAverage Percentage: {avg:.2f}%")

    def show_one(self):
        query = simpledialog.askstring("Search Student", "Enter name or ID:")
        if not query:
            return

        query = query.lower()
        target = None

        for s in self.manager.data:
            if query in s["name"].lower() or query == s["id"]:
                target = s
                break

        self.output.delete("1.0", tk.END)

        if target:
            self.output.insert(tk.END, self.block(target))
        else:
            self.output.insert(tk.END, "Student not found.")

    def show_max(self):
        if not self.manager.data:
            return
        best = max(self.manager.data, key=lambda x: x["total"])
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Highest Scorer\n\n")
        self.output.insert(tk.END, self.block(best))

    def show_min(self):
        if not self.manager.data:
            return
        worst = min(self.manager.data, key=lambda x: x["total"])
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Lowest Scorer\n\n")
        self.output.insert(tk.END, self.block(worst))


root = tk.Tk()
app = StudentApp(root)
root.mainloop()
