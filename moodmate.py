import customtkinter as ctk
from tkinter import font
from datetime import datetime

# App Config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

main = ctk.CTk()
main.geometry("800x800")
main.title("MoodMate - Your Daily Mood Companion")

# Fonts
font_heading = ctk.CTkFont(family="Coolvetica", size=65)
font_date = ctk.CTkFont(family="Coolvetica", size=20)
font_normal = ctk.CTkFont(family="EastmanRomanTrial-Medium", size=18)
font_small = ctk.CTkFont(family="EastmanRomanTrial-Medium", size=14)

# --- UI Layout ---

# Heading
heading = ctk.CTkLabel(main, text="MoodMate", font=font_heading, text_color="#096fb3")
heading.place(x=250, y=20)

# Date
current_date = datetime.today().strftime('%A, %d %B %Y')
date_label = ctk.CTkLabel(main, text=f"📅 {current_date}", font=font_date)
date_label.place(x=270, y=100)

# Welcome Text
welcome_label = ctk.CTkLabel(main, text="Hello User! Hope you're having a GREAT day 🎉", font=font_normal)
welcome_label.place(x=170, y=160)

# --- Mood Start Prompt ---
prompt_label = ctk.CTkLabel(main, text="Shall we begin tracking your mood now?", font=font_normal)
prompt_label.place(x=230, y=200)

def start_mood_tracking():
    prompt_label.destroy()
    yes_button.destroy()
    no_button.destroy()
    show_mood_section()

def decline_mood_tracking():
    prompt_label.configure(text="No worries! Come back whenever you're ready 😊")
    yes_button.destroy()
    no_button.destroy()

yes_button = ctk.CTkButton(main, text="Yes", command=start_mood_tracking, width=80)
yes_button.place(x=310, y=240)

no_button = ctk.CTkButton(main, text="No", command=decline_mood_tracking, width=80)
no_button.place(x=410, y=240)

# Function to Create Mood Section (Only when "Yes" is clicked)
def show_mood_section():
    mood_frame = ctk.CTkFrame(main, width=600, height=300, corner_radius=20)
    mood_frame.place(x=100, y=300)

    mood_heading = ctk.CTkLabel(mood_frame, text="How are you feeling today?", font=font_normal)
    mood_heading.place(x=180, y=20)

    moods = ["😊 Happy", "😢 Sad", "😐 Neutral", "😡 Angry", "😨 Anxious"]
    mood_var = ctk.StringVar(value="")

    def set_mood(choice):
        mood_var.set(choice)
        if "Happy" in choice:
            mood_frame.configure(fg_color="#d4edda")
            mood_heading.configure(text_color="#0C3D18")
        elif "Sad" in choice:
            mood_frame.configure(fg_color="#f8d7da")
            mood_heading.configure(text_color="#861420")
        elif "Neutral" in choice:
            mood_frame.configure(fg_color="#d6d8db")
            mood_heading.configure(text_color="#3e454a")
        elif "Angry" in choice:
            mood_frame.configure(fg_color="#f5c6cb")
            mood_heading.configure(text_color="#a71d2a")
        elif "Anxious" in choice:
            mood_frame.configure(fg_color="#d1ecf1")
            mood_heading.configure(text_color="#06515e")
        else:
            mood_frame.configure(fg_color="default")
            mood_heading.configure(text_color="default")

    for index, mood in enumerate(moods):
        btn = ctk.CTkButton(mood_frame, text=mood, width=120, command=lambda m=mood: set_mood(m))
        btn.place(x=40 + (index % 3) * 180, y=70 + (index // 3) * 60)

    notes_label = ctk.CTkLabel(mood_frame, text="Want to share more?", font=font_small)
    notes_label.place(x=30, y=200)

    notes_input = ctk.CTkEntry(mood_frame, width=500, height=30, placeholder_text="Write here...")
    notes_input.place(x=30, y=230)

    def save_mood():
        mood = mood_var.get()
        notes = notes_input.get()
        print(f"Saved: Mood = {mood}, Notes = {notes}")

    save_button = ctk.CTkButton(main, text="Save Mood Log", width=200, height=40, command=save_mood, fg_color="#096fb3")
    save_button.place(x=300, y=650)

# Run App
main.mainloop()
