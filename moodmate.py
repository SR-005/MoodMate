import customtkinter as ctk
from tkinter import font
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("950x800")
app.title("MoodMate - Your Daily Mood Companion")

# Fonts
font_heading = ctk.CTkFont(family="Coolvetica", size=60)
font_date = ctk.CTkFont(family="Coolvetica", size=18)
font_normal = ctk.CTkFont(family="EastmanRomanTrial-Medium", size=18)
font_small = ctk.CTkFont(family="EastmanRomanTrial-Medium", size=14)

# Scrollable Frame
scroll_frame = ctk.CTkScrollableFrame(app, width=900, height=780, corner_radius=20)
scroll_frame.pack(pady=10)

# --- Heading ---
heading = ctk.CTkLabel(scroll_frame, text="MoodMate", font=font_heading, text_color="#096fb3")
heading.pack(pady=(30, 10))

# --- Date ---
current_date = datetime.today().strftime('%A, %d %B %Y')
date_label = ctk.CTkLabel(scroll_frame, text=f"🗕️ {current_date}", font=font_date)
date_label.pack(pady=(0, 10))

# --- Welcome & Prompt ---
welcome_label = ctk.CTkLabel(scroll_frame, text="Hello User! Hope you're having a GREAT day 🎉", font=font_normal)
welcome_label.pack(pady=(10, 0))

prompt_label = ctk.CTkLabel(scroll_frame, text="Shall we start tracking your mood today?", font=font_normal)
prompt_label.pack(pady=(10, 20))

# --- Mood Section ---
moods = ["😊 Happy", "😢 Sad", "😐 Neutral", "😡 Angry", "😨 Anxious"]
mood_var = ctk.StringVar(value="")
mood_buttons = []

# WIDER mood frame
mood_frame = ctk.CTkFrame(scroll_frame, width=700, height=400, corner_radius=20, fg_color="#222222")

mood_heading = ctk.CTkLabel(mood_frame, text="How are you feeling today?", font=font_normal, text_color="#CCCCCC")
mood_heading.pack(pady=(20, 15))  # Padding top and bottom

notes_label = ctk.CTkLabel(mood_frame, text="Write more about your day (optional):", font=font_small, text_color="#CCCCCC")
notes_label.pack(pady=(10, 5))

# Slightly smaller Textbox width for padding
notes_input = ctk.CTkTextbox(mood_frame, width=580, height=100, corner_radius=10)
notes_input.pack(pady=(0, 40))

# Mood Buttons Frame
button_row = ctk.CTkFrame(mood_frame)
button_row.pack(pady=(0, 25))


def set_mood(choice):
    mood_var.set(choice)
    mood_heading.configure(text=f"You selected: {choice}")

    # Reset button styles
    for btn in mood_buttons:
        btn.configure(fg_color="#3a3b3c", text_color="#FFFFFF")

    # Highlight selected button
    for btn in mood_buttons:
        if btn.cget("text") == choice:
            btn.configure(fg_color="#096fb3", text_color="white")

    # Change mood frame color and adjust text colors accordingly
    colors = {
        "Happy": ("#d4edda", "#0C3D18", "#0C3D18"),
        "Sad": ("#f8d7da", "#861420", "#861420"),
        "Neutral": ("#d6d8db", "#3e454a", "#3e454a"),
        "Angry": ("#f5c6cb", "#a71d2a", "#a71d2a"),
        "Anxious": ("#d1ecf1", "#06515e", "#06515e"),
    }

    for mood in colors:
        if mood in choice:
            bg, fg_heading, fg_notes = colors[mood]
            mood_frame.configure(fg_color=bg)
            mood_heading.configure(text_color=fg_heading)
            notes_label.configure(text_color=fg_notes)
            break
    else:
        mood_frame.configure(fg_color="#222222")
        mood_heading.configure(text_color="#CCCCCC")
        notes_label.configure(text_color="#CCCCCC")


for i, mood in enumerate(moods):
    btn = ctk.CTkButton(button_row, text=mood, width=110, command=lambda m=mood: set_mood(m))
    btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
    mood_buttons.append(btn)


# --- Save Mood ---
mood_log = pd.DataFrame(columns=["Date", "Mood", "Notes"])

def save_mood():
    global mood_log
    mood = mood_var.get()
    notes = notes_input.get("1.0", "end-1c")

    if not mood:
        print("No mood selected")
        return

    mood_log.loc[len(mood_log)] = [datetime.today().strftime('%Y-%m-%d'), mood, notes]
    print(f"Saved: Mood = {mood}, Notes = {notes}")

    # Reset UI
    mood_var.set("")
    notes_input.delete("1.0", "end")
    mood_frame.configure(fg_color="#2a2d2e")
    mood_heading.configure(text="How are you feeling today?", text_color="#CCCCCC")
    notes_label.configure(text_color="#CCCCCC")
    for btn in mood_buttons:
        btn.configure(fg_color="#3a3b3c", text_color="#FFFFFF")

    # Update chart
    show_mood_chart(mood_log)


# --- Start Button ---
def start_mood_tracking():
    mood_frame.pack(pady=20)
    save_button.pack(pady=(10, 30))
    analyze_frame.pack(pady=40)
    prompt_label.configure(text="Let's go!")
    start_button.pack_forget()

start_button = ctk.CTkButton(scroll_frame, text="Yes, Let's Go!", command=start_mood_tracking, width=200)
start_button.pack()

# --- Save Button ---
save_button = ctk.CTkButton(scroll_frame, text="Save Mood Log", width=180, height=40, command=save_mood, fg_color="#096fb3")
save_button.pack_forget()

# --- Analysis Frame ---
analyze_frame = ctk.CTkFrame(scroll_frame, width=700, height=350, corner_radius=20)
analyze_frame.pack_forget()

def show_mood_chart(df):
    # Define all possible moods
    mood_labels = ["😊 Happy", "😢 Sad", "😐 Neutral", "😡 Angry", "😨 Anxious"]
    mood_counts = pd.Series(0, index=mood_labels)

    # Count actual moods
    actual_counts = df["Mood"].value_counts()
    mood_counts.update(actual_counts)

    # Clear previous widgets
    for widget in analyze_frame.winfo_children():
        widget.destroy()

    # Title
    chart_label = ctk.CTkLabel(analyze_frame, text="📊 Mood Overview", font=font_normal)
    chart_label.pack(pady=10)

    # Create bigger chart
    fig, ax = plt.subplots(figsize=(8, 6))  # Increased height from 5 to 6
    bars = mood_counts.plot(kind='bar', ax=ax, color="#096fb3", edgecolor='black')

    # Labels and formatting
    ax.set_ylabel("Count")
    ax.set_xlabel("Mood")
    ax.set_title("Mood Frequency")
    ax.set_ylim(0, max(mood_counts.max(), 1) + 1)
    plt.xticks(rotation=0, ha='center')  # Keep labels horizontal and centered
    fig.tight_layout(pad=2.0)  # Adds padding to prevent clipping

    # Embed chart in UI
    canvas = FigureCanvasTkAgg(fig, master=analyze_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Add Exit Button after mood chart (or at the very bottom)
exit_button = ctk.CTkButton(scroll_frame, text="Exit", width=180, height=40, fg_color="red", command=app.destroy)
exit_button.pack(pady=(10, 30))


app.mainloop()
