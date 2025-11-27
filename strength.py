import tkinter as tk
from tkinter import messagebox
import re

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("400x500")
        self.root.configure(bg="black")

        # Red and black theme
        self.bg_color = "black"
        self.fg_color = "red"
        self.button_bg = "red"
        self.button_fg = "black"

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(self.main_frame, text="Password Strength Checker", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Password entry
        tk.Label(self.main_frame, text="Enter Password:", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*", bg="#333333", fg=self.fg_color,
                                      insertbackground=self.fg_color, font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<KeyRelease>", self.check_password)  # Real-time checking

        # Show/hide password checkbox
        self.show_password = tk.BooleanVar()
        tk.Checkbutton(self.main_frame, text="Show Password", variable=self.show_password,
                       bg=self.bg_color, fg=self.fg_color, selectcolor="#333333",
                       command=self.toggle_password).pack(pady=5)

        # Strength label
        self.strength_label = tk.Label(self.main_frame, text="Strength: None", bg=self.bg_color,
                                      fg=self.fg_color, font=("Arial", 12, "bold"))
        self.strength_label.pack(pady=10)

        # Suggestions text
        self.suggestions_text = tk.Text(self.main_frame, height=10, width=35, bg="#333333",
                                        fg=self.fg_color, insertbackground=self.fg_color,
                                        font=("Arial", 10), wrap="word")
        self.suggestions_text.pack(pady=10)
        self.suggestions_text.config(state="disabled")  # Make read-only

        # Check button (optional, since real-time checking is enabled)
        tk.Button(self.main_frame, text="Check Password", bg=self.button_bg, fg=self.button_fg,
                  font=("Arial", 12, "bold"), command=self.check_password).pack(pady=10)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def check_password(self, event=None):
        password = self.password_entry.get()
        strength, suggestions = self.evaluate_password(password)

        # Update strength label with color coding
        strength_colors = {"Weak": "#ff3333", "Moderate": "#ffa500", "Strong": "#00ff00"}
        self.strength_label.config(text=f"Strength: {strength}", fg=strength_colors[strength])

        # Update suggestions
        self.suggestions_text.config(state="normal")
        self.suggestions_text.delete("1.0", tk.END)
        if suggestions:
            self.suggestions_text.insert(tk.END, "Suggestions to improve your password:\n\n")
            for suggestion in suggestions:
                self.suggestions_text.insert(tk.END, f"- {suggestion}\n")
        else:
            self.suggestions_text.insert(tk.END, "Your password is strong!")
        self.suggestions_text.config(state="disabled")

    def evaluate_password(self, password):
        suggestions = []
        score = 0

        # Check length
        if len(password) < 8:
            suggestions.append("Make the password at least 8 characters long")
        elif len(password) >= 12:
            score += 2
        else:
            score += 1

        # Check for uppercase letters
        if not re.search(r"[A-Z]", password):
            suggestions.append("Add at least one uppercase letter (A-Z)")
        else:
            score += 1

        # Check for lowercase letters
        if not re.search(r"[a-z]", password):
            suggestions.append("Add at least one lowercase letter (a-z)")
        else:
            score += 1

        # Check for digits
        if not re.search(r"\d", password):
            suggestions.append("Add at least one number (0-9)")
        else:
            score += 1

        # Check for special characters
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            suggestions.append("Add at least one special character (e.g., !, @, #, $)")
        else:
            score += 1

        # Determine strength
        if score <= 2 or len(password) < 8:
            strength = "Weak"
        elif score <= 4:
            strength = "Moderate"
        else:
            strength = "Strong"

        return strength, suggestions

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()