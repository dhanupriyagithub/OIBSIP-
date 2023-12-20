import random
import string
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


def generate_secure_password(length, use_letters=True, use_numbers=True, use_symbols=True):
    characters = ""
    if use_letters:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return None

    # Ensure at least one character from each selected category
    password = random.choice(string.ascii_uppercase) if use_letters else ''
    password += random.choice(string.ascii_lowercase) if use_letters else ''
    password += random.choice(string.digits) if use_numbers else ''
    password += random.choice(string.punctuation) if use_symbols else ''

    # Add the remaining characters randomly
    password += ''.join(random.choice(characters) for _ in range(length - len(password)))

    # Shuffle the password to randomize the order
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

def generate_custom_password(length, use_letters=True, use_numbers=True, use_symbols=True, excluded_chars=""):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    characters = ''.join(char for char in characters if char not in excluded_chars)

    if not characters:
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_button_clicked():
    try:
        length = int(length_var.get())
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        password = generate_secure_password(length, use_letters, use_numbers, use_symbols)

        if password:
            result_label.config(text=f"Generated Password: {password}")
            copy_to_clipboard_button.config(state=tk.NORMAL)
        else:
            result_label.config(text="Error: At least one character type must be selected.")
    except ValueError:
        result_label.config(text="Error: Please enter a valid number for password length.")

def copy_to_clipboard_button_clicked():
    label_text = result_label.cget("text")
    try:
        password = label_text.split(": ")[1]
        copy_to_clipboard(password)
        result_label.config(text="Password copied to clipboard!")
    except IndexError:
        result_label.config(text="Error: No password generated.")

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")

style = ttk.Style()
style.map("TButton", background=[("disabled", "#A9A9A9")])
style.configure("TLabel", padding=5, background="#f0f0f0")
style.configure("TCheckbutton", padding=5)

length_label = ttk.Label(root, text="Password Length:")
length_var = tk.StringVar(value="")
length_entry = ttk.Entry(root, textvariable=length_var)

letters_var = tk.BooleanVar(value=True)
letters_checkbox = ttk.Checkbutton(root, text="Include Letters", variable=letters_var)

numbers_var = tk.BooleanVar(value=True)
numbers_checkbox = ttk.Checkbutton(root, text="Include Numbers", variable=numbers_var)

symbols_var = tk.BooleanVar(value=True)
symbols_checkbox = ttk.Checkbutton(root, text="Include Symbols", variable=symbols_var)

generate_button = ttk.Button(root, text="Generate Password", command=generate_button_clicked)
copy_to_clipboard_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard_button_clicked, state=tk.DISABLED)

result_label = ttk.Label(root, text="")

length_label.grid(row=0, column=0, pady=5, padx=10, sticky="e")
length_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

letters_checkbox.grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky="ew")
numbers_checkbox.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="ew")
symbols_checkbox.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

generate_button.grid(row=4, column=0, columnspan=2, pady=20)
copy_to_clipboard_button.grid(row=5, column=0, columnspan=2, pady=10)
result_label.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

root.mainloop()

