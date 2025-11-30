import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Colors and fonts
BG_COLOR = "#0f172a"
CARD_COLOR = "#020617"
TEXT_COLOR = "#e5e7eb"
ACCENT_COLOR = "#22c55e"
FONT_NORMAL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App - BSc IT Project")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        self.root.configure(bg=BG_COLOR)
        
        # Chat history list
        self.messages = []
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=(8, 0))
        
        title_label = tk.Label(
            top_bar,
            text="Chat Application",
            font=FONT_TITLE,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(side="left", padx=16)
        
        subtitle_label = tk.Label(
            top_bar,
            text="Simple Local Chat Demo",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg="#9ca3af"
        )
        subtitle_label.pack(side="left", padx=8)
        
        # Card container
        card_outer = tk.Frame(self.root, bg=BG_COLOR)
        card_outer.pack(fill="both", expand=True, padx=16, pady=12)
        
        card = tk.Frame(
            card_outer,
            bg=CARD_COLOR,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937"
        )
        card.pack(fill="both", expand=True)
        
        # Chat display area
        chat_frame = tk.Frame(card, bg=CARD_COLOR)
        chat_frame.pack(padx=15, pady=15, fill="both", expand=True)
        
        chat_label = tk.Label(
            chat_frame,
            text="Messages:",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        chat_label.pack(anchor="w", pady=(0, 5))
        
        # Text widget for messages (scrollable)
        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.chat_display = tk.Text(
            chat_frame,
            font=FONT_NORMAL,
            bg="#020617",
            fg=TEXT_COLOR,
            height=12,
            width=60,
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        scrollbar.config(command=self.chat_display.yview)
        
        # Input area
        input_frame = tk.Frame(card, bg=CARD_COLOR)
        input_frame.pack(padx=15, pady=(0, 15), fill="x")
        
        input_label = tk.Label(
            input_frame,
            text="Your message:",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        input_label.pack(anchor="w", pady=(0, 5))
        
        # Input entry
        self.message_entry = tk.Entry(
            input_frame,
            font=FONT_NORMAL,
            bg="#1f2937",
            fg=TEXT_COLOR,
            relief="flat"
        )
        self.message_entry.pack(fill="x", pady=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=CARD_COLOR)
        button_frame.pack(fill="x", pady=(0, 5))
        
        send_button = tk.Button(
            button_frame,
            text="Send",
            command=self.send_message,
            font=FONT_NORMAL,
            bg=ACCENT_COLOR,
            fg="white",
            activebackground="#16a34a",
            relief="flat",
            cursor="hand2",
            width=10
        )
        send_button.pack(side="left", padx=(0, 5))
        
        clear_button = tk.Button(
            button_frame,
            text="Clear Chat",
            command=self.clear_chat,
            font=FONT_NORMAL,
            bg="#424242",
            fg="white",
            activebackground="#616161",
            relief="flat",
            cursor="hand2",
            width=10
        )
        clear_button.pack(side="left")
        
        # Add welcome message
        self.display_message("System", "Welcome to Chat App! Start typing to chat.", "system")
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            messagebox.showwarning("Empty Message", "Please type a message.")
            return
        
        # Display user message
        self.display_message("You", message, "user")
        self.message_entry.delete(0, tk.END)
        
        # Simulate bot response (simple echo)
        if message.lower() == "hello":
            self.display_message("Bot", "Hi there! How are you doing?", "bot")
        elif message.lower() == "hi":
            self.display_message("Bot", "Hey! What's up?", "bot")
        elif message.lower() == "how are you":
            self.display_message("Bot", "I'm doing great, thanks for asking!", "bot")
        elif message.lower() == "what is your name":
            self.display_message("Bot", "I'm a Chat Bot created for BSc IT project.", "bot")
        elif message.lower() == "help":
            self.display_message("Bot", "Try saying: hello, hi, how are you, what is your name, or goodbye", "bot")
        elif message.lower() == "goodbye":
            self.display_message("Bot", "Goodbye! Have a nice day!", "bot")
        else:
            self.display_message("Bot", "That's interesting! Tell me more.", "bot")
    
    def display_message(self, sender, message, msg_type):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Enable text widget, add message, disable it
        self.chat_display.config(state="normal")
        
        # Color based on sender
        if msg_type == "user":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n", "user_msg")
        elif msg_type == "bot":
            self.chat_display.insert(tk.END, f"[{timestamp}] Bot: {message}\n", "bot_msg")
        elif msg_type == "system":
            self.chat_display.insert(tk.END, f"{message}\n", "system_msg")
        
        self.chat_display.config(state="disabled")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        
        # Store message
        self.messages.append((sender, message, timestamp))
    
    def clear_chat(self):
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state="disabled")
        self.messages.clear()
        self.display_message("System", "Chat cleared.", "system")

# Create main window
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
