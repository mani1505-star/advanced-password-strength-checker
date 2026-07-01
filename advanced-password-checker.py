import tkinter as tk
from tkinter import ttk
import math
import re

# More advanced charset detection
def get_charset_size(password):
    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"\d", password):
        charset += 10
    if re.search(r"[!@#$%^&*()_\-+=\[{\]};:'\",<.>/?\\|`~]", password):
        charset += 33
    if re.search(r"\s", password):
        charset += 1
    return charset

def calculate_entropy(password):
    charset_size = get_charset_size(password)
    if charset_size == 0 or len(password) == 0:
        return 0, "Too weak to estimate"
    entropy = len(password) * math.log2(charset_size)
    time_to_crack = 2 ** entropy / 1e10  # 10B guesses/sec
    return entropy, convert_seconds_to_time(time_to_crack)

def convert_seconds_to_time(seconds):
    units = [("years", 365*24*60*60), ("days", 24*60*60),
             ("hours", 3600), ("minutes", 60), ("seconds", 1)]
    for name, count in units:
        value = seconds // count
        if value >= 1:
            return f"~ {int(value)} {name}"
    return "Less than a second"

def password_score(password):
    score = 0
    tips = []
    length = len(password)

    if length >= 8:
        score += 25
    else:
        score += int((length / 8) * 25)
        tips.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 20
    else:
        tips.append("Mix upper and lower case letters.")

    if re.search(r"\d", password):
        score += 20
    else:
        tips.append("Include numbers.")

    if re.search(r"[!@#$%^&*()_\-+=\[{\]};:'\",<.>/?\\|`~]", password):
        score += 25
    else:
        tips.append("Use special characters.")

    if length > 12:
        score += 10

    return min(score, 100), tips

def update_ui(event=None):
    pwd = password_entry.get()
    score, tips = password_score(pwd)
    entropy, crack_time = calculate_entropy(pwd)

    strength_label.config(text=f"Strength: {score}%")
    entropy_label.config(text=f"Entropy: {entropy:.2f} bits")
    crack_label.config(text=f"Crack Time: {crack_time}")

    progress['value'] = score
    if score >= 80:
        progress.configure(style="Green.Horizontal.TProgressbar")
    elif score >= 55:
        progress.configure(style="Yellow.Horizontal.TProgressbar")
    else:
        progress.configure(style="Red.Horizontal.TProgressbar")

    suggestions.config(state="normal")
    suggestions.delete(1.0, tk.END)
    if score == 100:
        suggestions.insert(tk.END, "Excellent password! ✅")
    else:
        for tip in tips:
            suggestions.insert(tk.END, f"• {tip}\n")
    suggestions.config(state="disabled")

# GUI setup
root = tk.Tk()
root.title("🔐 Pro-Level Password Strength Checker")
root.geometry("650x520")
root.configure(bg="#1f1f2e")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Red.Horizontal.TProgressbar", troughcolor="#3e3e52", background="#ff4d4d")
style.configure("Yellow.Horizontal.TProgressbar", troughcolor="#3e3e52", background="#ffcc00")
style.configure("Green.Horizontal.TProgressbar", troughcolor="#3e3e52", background="#00e676")

title = tk.Label(root, text="Advanced Password Strength Analyzer", font=("Segoe UI", 20, "bold"),
                 bg="#1f1f2e", fg="#00d7ff")
title.pack(pady=20)

entry_label = tk.Label(root, text="🔑 Enter Your Password", font=("Segoe UI", 12),
                       bg="#1f1f2e", fg="#ffffff")
entry_label.pack()
password_entry = tk.Entry(root, font=("Consolas", 14), width=35, show="*",
                          bg="#2b2b3c", fg="#ffffff", insertbackground="white", relief="flat")
password_entry.pack(pady=10)
password_entry.bind("<KeyRelease>", update_ui)

strength_label = tk.Label(root, text="Strength: 0%", font=("Segoe UI", 12, "bold"),
                          bg="#1f1f2e", fg="#00e676")
strength_label.pack(pady=5)

entropy_label = tk.Label(root, text="Entropy: 0.00 bits", font=("Segoe UI", 11),
                         bg="#1f1f2e", fg="#c1c1c1")
entropy_label.pack()

crack_label = tk.Label(root, text="Crack Time: Too weak to estimate", font=("Segoe UI", 11),
                       bg="#1f1f2e", fg="#ffa726")
crack_label.pack(pady=5)

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=15)

suggest_label = tk.Label(root, text="Suggestions to Improve:", font=("Segoe UI", 12, "underline"),
                         bg="#1f1f2e", fg="#66ffcc")
suggest_label.pack()

suggestions = tk.Text(root, height=6, width=60, wrap="word",
                      bg="#28283b", fg="white", font=("Segoe UI", 10), bd=0)
suggestions.pack(pady=5)
suggestions.config(state="disabled")

footer = tk.Label(root, text="© 2025 | Cybersecurity Project by [Mani Singh]",
                  font=("Poppins", 9), bg="#1f1f2e", fg="#777")
footer.pack(side="bottom", pady=10)

import random
import string
def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        show_button.config(text="🙈 Hide")
    else:
        password_entry.config(show='*')
        show_button.config(text="👁️ Show")

def generate_password():
    length = 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_-=+[]{};:,.<>?/\\|`~"
    password = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    update_ui()
password_entry.pack(pady=10)
# Buttons for show/hide and generate
button_frame = tk.Frame(root, bg="#1f1f2e")
button_frame.pack()

show_button = tk.Button(button_frame, text="👁️ Show", command=toggle_password,
                        font=("Segoe UI", 10), bg="#3b3b4f", fg="white", relief="flat", width=10)
show_button.pack(side="left", padx=5)

generate_button = tk.Button(button_frame, text="🎲 Generate", command=generate_password,
                            font=("Segoe UI", 10), bg="#3b3b4f", fg="white", relief="flat", width=20)
generate_button.pack(side="left", padx=5)

root.mainloop()