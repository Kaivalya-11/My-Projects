import tkinter as tk
from tkinter import messagebox

# Colors and fonts (for better UI)
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#2b2b40"
ACCENT_COLOR = "#4caf50"
TEXT_COLOR = "#ffffff"
FONT_NORMAL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_RESULT = ("Segoe UI", 12, "bold")

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if weight <= 0 or height_cm <= 0:
            raise ValueError

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        bmi_value_label.config(text=f"{bmi:.2f}")

        if bmi < 18.5:
            category = "Underweight"
            color = "#03a9f4"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            color = "#4caf50"
        elif 25 <= bmi < 30:
            category = "Overweight"
            color = "#ff9800"
        else:
            category = "Obese"
            color = "#f44336"

        bmi_category_label.config(text=category, fg=color)

    except ValueError:
        messagebox.showerror("Invalid Input",
                             "Please enter valid positive numbers for weight and height.")

def reset_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    bmi_value_label.config(text="--")
    bmi_category_label.config(text="--", fg=TEXT_COLOR)

# Main window
root = tk.Tk()
root.title("BMI Calculator - BSc IT Project")
root.geometry("420x320")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Title
title_label = tk.Label(
    root,
    text="Body Mass Index (BMI) Calculator",
    font=FONT_TITLE,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=(15, 5))

subtitle_label = tk.Label(
    root,
    text="Enter your weight and height to check your BMI",
    font=FONT_NORMAL,
    bg=BG_COLOR,
    fg="#cccccc"
)
subtitle_label.pack(pady=(0, 10))

# Card frame for form
card_frame = tk.Frame(root, bg=CARD_COLOR, bd=0, highlightthickness=0)
card_frame.pack(padx=20, pady=5, fill="both")

# Form area
form_frame = tk.Frame(card_frame, bg=CARD_COLOR)
form_frame.pack(padx=15, pady=15, fill="x")

weight_label = tk.Label(form_frame, text="Weight (kg):", font=FONT_NORMAL,
                        bg=CARD_COLOR, fg=TEXT_COLOR)
weight_label.grid(row=0, column=0, padx=5, pady=8, sticky="e")

weight_entry = tk.Entry(form_frame, width=18, font=FONT_NORMAL, relief="flat")
weight_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")

height_label = tk.Label(form_frame, text="Height (cm):", font=FONT_NORMAL,
                        bg=CARD_COLOR, fg=TEXT_COLOR)
height_label.grid(row=1, column=0, padx=5, pady=8, sticky="e")

height_entry = tk.Entry(form_frame, width=18, font=FONT_NORMAL, relief="flat")
height_entry.grid(row=1, column=1, padx=5, pady=8, sticky="w")

# Button row
button_frame = tk.Frame(card_frame, bg=CARD_COLOR)
button_frame.pack(pady=(0, 10))

calculate_button = tk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi,
    width=14,
    font=FONT_NORMAL,
    bg=ACCENT_COLOR,
    fg="white",
    activebackground="#43a047",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
calculate_button.grid(row=0, column=0, padx=8, pady=5)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    command=reset_fields,
    width=10,
    font=FONT_NORMAL,
    bg="#424242",
    fg="white",
    activebackground="#616161",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
reset_button.grid(row=0, column=1, padx=8, pady=5)

# Result area
result_frame = tk.Frame(card_frame, bg=CARD_COLOR)
result_frame.pack(padx=15, pady=(0, 15), fill="x")

bmi_label = tk.Label(result_frame, text="Your BMI:", font=FONT_RESULT,
                     bg=CARD_COLOR, fg=TEXT_COLOR)
bmi_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

bmi_value_label = tk.Label(result_frame, text="--", font=FONT_RESULT,
                           bg=CARD_COLOR, fg=TEXT_COLOR)
bmi_value_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

category_label = tk.Label(result_frame, text="Category:", font=FONT_RESULT,
                          bg=CARD_COLOR, fg=TEXT_COLOR)
category_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

bmi_category_label = tk.Label(result_frame, text="--", font=FONT_RESULT,
                              bg=CARD_COLOR, fg=TEXT_COLOR)
bmi_category_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

root.mainloop()
