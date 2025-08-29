# AI-Powered Study Assistant - Advanced UI

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import PyPDF2
import openai
import json
import os

# Set your OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Core Functions

def load_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        text = extract_text_from_pdf(file_path)
        pdf_text.delete("1.0", tk.END)
        pdf_text.insert(tk.END, text)

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def summarize_text():
    content = pdf_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "Please load a PDF first!")
        return
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":f"Summarize the following text:\n{content}"}]
    )
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, response['choices'][0]['message']['content'])

def generate_quiz():
    summary = summary_text.get("1.0", tk.END).strip()
    if not summary:
        messagebox.showwarning("Warning", "Please summarize text first!")
        return
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":f"Create 5 multiple-choice questions from the following text:\n{summary}"}]
    )
    quiz_text.delete("1.0", tk.END)
    quiz_text.insert(tk.END, response['choices'][0]['message']['content'])

def save_quiz():
    quiz = quiz_text.get("1.0", tk.END).strip()
    if not quiz:
        messagebox.showwarning("Warning", "No quiz to save!")
        return
    if not os.path.exists("quizzes"):
        os.makedirs("quizzes")
    with open("quizzes/quiz.json", "w") as f:
        json.dump({"quiz": quiz}, f)
    messagebox.showinfo("Saved", "Quiz saved successfully!")

# GUI Setup

root = tk.Tk()
root.title("AI Study Assistant")
root.geometry("1000x750")
root.configure(bg="#1e1e2f")

# Fonts and Styles

TITLE_FONT = ("Helvetica", 16, "bold")
LABEL_FONT = ("Helvetica", 12)
TEXT_FONT = ("Consolas", 11)

BUTTON_STYLE = {
    "bg": "#4e4eff",
    "fg": "white",
    "activebackground": "#6e6eff",
    "activeforeground": "white",
    "bd": 0,
    "font": ("Helvetica", 12, "bold"),
    "cursor": "hand2",
    "relief": "flat",
    "padx": 10,
    "pady": 5
}

# Frames

pdf_frame = tk.LabelFrame(root, text="📄 PDF Content", bg="#2e2e3f", fg="white", font=TITLE_FONT, padx=10, pady=10)
pdf_frame.pack(fill="both", padx=20, pady=10, expand=True)

summary_frame = tk.LabelFrame(root, text="📝 Summary", bg="#2e2e3f", fg="white", font=TITLE_FONT, padx=10, pady=10)
summary_frame.pack(fill="both", padx=20, pady=10, expand=True)

quiz_frame = tk.LabelFrame(root, text="❓ Quiz", bg="#2e2e3f", fg="white", font=TITLE_FONT, padx=10, pady=10)
quiz_frame.pack(fill="both", padx=20, pady=10, expand=True)

# PDF Section

pdf_text = scrolledtext.ScrolledText(pdf_frame, height=10, font=TEXT_FONT, bg="#1e1e2f", fg="white", insertbackground="white")
pdf_text.pack(fill="both", expand=True, pady=5)

tk.Button(pdf_frame, text="Load PDF", command=load_pdf, **BUTTON_STYLE).pack(pady=5)

# Summary Section

summary_text = scrolledtext.ScrolledText(summary_frame, height=8, font=TEXT_FONT, bg="#1e1e2f", fg="white", insertbackground="white")
summary_text.pack(fill="both", expand=True, pady=5)

tk.Button(summary_frame, text="Summarize", command=summarize_text, **BUTTON_STYLE).pack(pady=5)

# Quiz Section

quiz_text = scrolledtext.ScrolledText(quiz_frame, height=8, font=TEXT_FONT, bg="#1e1e2f", fg="white", insertbackground="white")
quiz_text.pack(fill="both", expand=True, pady=5)

tk.Button(quiz_frame, text="Generate Quiz", command=generate_quiz, **BUTTON_STYLE).pack(side="left", padx=10, pady=5)
tk.Button(quiz_frame, text="Save Quiz", command=save_quiz, **BUTTON_STYLE).pack(side="left", padx=10, pady=5)

root.mainloop()
