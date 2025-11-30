import tkinter as tk
from tkinter import messagebox
import string
import random

# Colors and fonts
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#2b2b40"
ACCENT_COLOR = "#4caf50"
TEXT_COLOR = "#ffffff"
FONT_NORMAL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_RESULT = ("Segoe UI", 11, "bold")

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError

        # Character set: letters, digits, and punctuation
        characters = string.ascii_letters + string.digits + string.punctuation

        password = "".join(random.choice(characters) for _ in range(length))
        password_entry.config(state="normal")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        password_entry.config(state="readonly")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive integer for length.")

def copy_to_clipboard():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("No Password", "Generate a password first.")
    else:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard.")

# Main window
root = tk.Tk()
root.title("Password Generator - BSc IT Project")
root.geometry("430x260")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Title
title_label = tk.Label(
    root,
    text="Random Password Generator",
    font=FONT_TITLE,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=(15, 5))

subtitle_label = tk.Label(
    root,
    text="Enter length and generate a secure random password",
    font=FONT_NORMAL,
    bg=BG_COLOR,
    fg="#cccccc"
)
subtitle_label.pack(pady=(0, 10))

# Card frame
card_frame = tk.Frame(root, bg=CARD_COLOR)
card_frame.pack(padx=20, pady=5, fill="both")

# Length input
form_frame = tk.Frame(card_frame, bg=CARD_COLOR)
form_frame.pack(padx=15, pady=15, fill="x")

length_label = tk.Label(
    form_frame,
    text="Password length:",
    font=FONT_NORMAL,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)
length_label.grid(row=0, column=0, padx=5, pady=8, sticky="e")

length_entry = tk.Entry(form_frame, width=10, font=FONT_NORMAL, relief="flat")
length_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")
length_entry.insert(0, "12")  # default length

# Buttons
button_frame = tk.Frame(card_frame, bg=CARD_COLOR)
button_frame.pack(pady=(0, 10))

generate_button = tk.Button(
    button_frame,
    text="Generate",
    command=generate_password,
    width=12,
    font=FONT_NORMAL,
    bg=ACCENT_COLOR,
    fg="white",
    activebackground="#43a047",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
generate_button.grid(row=0, column=0, padx=8, pady=5)

copy_button = tk.Button(
    button_frame,
    text="Copy",
    command=copy_to_clipboard,
    width=10,
    font=FONT_NORMAL,
    bg="#424242",
    fg="white",
    activebackground="#616161",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
copy_button.grid(row=0, column=1, padx=8, pady=5)

# Password output
result_frame = tk.Frame(card_frame, bg=CARD_COLOR)
result_frame.pack(padx=15, pady=(0, 15), fill="x")

password_label = tk.Label(
    result_frame,
    text="Generated password:",
    font=FONT_RESULT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)
password_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

password_entry = tk.Entry(
    result_frame,
    font=FONT_RESULT,
    width=28,
    relief="flat"
)
password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
password_entry.config(state="readonly")

root.mainloop()
