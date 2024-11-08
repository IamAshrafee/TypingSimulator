# Importing necessary modules
import pyautogui  # For typing automation
import time  # To introduce delays between typing
from tkinter import filedialog, Tk, Text, Button, Label, Entry, Frame, Scale  # GUI components
import threading  # For running typing in a separate thread
import keyboard  # For detecting keyboard shortcuts

# Initialize flags, variables, and default settings
typing_active = False  # Track whether typing should continue
typing_paused = False  # Track if typing is paused
start_shortcut = "ctrl+shift+1"
pause_shortcut = "ctrl+shift+p"
end_shortcut = "ctrl+shift+e"
typing_speed = 10  # Default typing speed

# Function to allow setting the typing window focus
def wait_for_focus():
    time.sleep(2)  # Give user 2 seconds to switch to desired typing window
    while typing_active and pyautogui.getActiveWindow().title == root.title:
        time.sleep(0.1)  # Wait until the focus is no longer on this app

# Function to pause or resume typing
def toggle_pause_typing():
    global typing_paused
    typing_paused = not typing_paused  # Toggle paused state
    pause_button.config(text="Resume Typing" if typing_paused else "Pause Typing")
    status_label.config(text="Status: Paused" if typing_paused else "Status: Typing")  # Update status label

# Function to end typing and reset
def end_typing():
    global typing_active, typing_paused
    typing_active = False  # Stop typing
    typing_paused = False  # Reset paused state
    pause_button.config(text="Pause Typing")  # Reset button label
    status_label.config(text="Status: Stopped")  # Update status label

# Function to adjust typing speed from the slider
def set_typing_speed(value):
    global typing_speed
    typing_speed = int(value)  # Update typing speed from slider value

# Function to type the given input (word, sentence, or paragraph)
def type_text(input_text):
    global typing_active, typing_paused
    typing_active = True  # Allow typing
    status_label.config(text="Status: Typing")  # Update status to Typing
    wait_for_focus()  # Wait for user to set the focus to a typing area
    for char in input_text:
        if not typing_active:  # Stop typing if ended
            break
        while typing_paused:  # Pause typing if paused
            time.sleep(0.1)  # Small delay to avoid high CPU usage
        pyautogui.write(char)  # Type each character where the cursor is focused
        time.sleep(min(0.03, 0.01 / typing_speed))  # Adjust typing speed with smoother limits
    status_label.config(text="Status: Stopped")  # Update status when done

# Wrapper function to start typing in a new thread
def start_typing_thread(input_text):
    threading.Thread(target=type_text, args=(input_text,), daemon=True).start()

# Function to type contents of the text file
def type_from_file(file_path):
    try:
        with open(file_path, 'r') as file:  # Open the file in read mode
            content = file.read()  # Read the entire file content
            start_typing_thread(content)  # Start typing in a new thread
    except FileNotFoundError:
        print("File not found. Please check the path.")
        status_label.config(text="Status: File Not Found")  # Update status on error

# Function to get text input from user and start typing
def get_text_input():
    input_text = text_box.get("1.0", "end-1c").strip()  # Get text from text box
    if input_text:  # Check if text is present
        start_typing_thread(input_text)  # Start typing in a new thread

# Function to let user select a file and start typing its content
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])  # Limit to text files only
    if file_path:  # Check if a file was selected
        type_from_file(file_path)  # Start typing in a new thread

# Function to customize shortcuts
def set_shortcuts():
    global start_shortcut, pause_shortcut, end_shortcut
    start_shortcut = start_entry.get().strip()
    pause_shortcut = pause_entry.get().strip()
    end_shortcut = end_entry.get().strip()
    shortcut_label.config(text=f"Start: {start_shortcut} | Pause: {pause_shortcut} | End: {end_shortcut}")

# Setting up keyboard shortcuts
def register_shortcuts():
    keyboard.add_hotkey(start_shortcut, get_text_input)  # Start typing with shortcut
    keyboard.add_hotkey(pause_shortcut, toggle_pause_typing)  # Pause/resume with shortcut
    keyboard.add_hotkey(end_shortcut, end_typing)  # End typing with shortcut

# Tkinter GUI setup
root = Tk()
root.title("Enhanced Auto Typer")

# Align UI elements with a Frame for better structure and spacing
frame = Frame(root, padx=10, pady=10)
frame.pack()

# Text box for inputting text
text_box = Text(frame, height=10, width=50, wrap="word", padx=5, pady=5)
text_box.grid(row=0, column=0, columnspan=3, pady=10)

# Button to start typing the text entered in the text box
type_button = Button(frame, text="Start Typing", command=get_text_input)
type_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

# Button to select a file and start typing its content
file_button = Button(frame, text="Type From File", command=select_file)
file_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# Pause/Resume button for toggling typing state
pause_button = Button(frame, text="Pause Typing", command=toggle_pause_typing)
pause_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

# Button to end typing
end_button = Button(frame, text="End Typing", command=end_typing)
end_button.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# Typing speed adjustment with a slider
Label(frame, text="Typing Speed (10 = Fast, 1 = Slow):").grid(row=3, column=0, columnspan=2)
speed_slider = Scale(frame, from_=1, to=30, orient="horizontal", command=set_typing_speed)
speed_slider.set(typing_speed)
speed_slider.grid(row=3, column=2, padx=5, pady=5)

# Shortcut customization
Label(frame, text="Customize Shortcuts").grid(row=4, column=0, columnspan=3, pady=10)
Label(frame, text="Start Typing Shortcut:").grid(row=5, column=0)
start_entry = Entry(frame)
start_entry.insert(0, start_shortcut)
start_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=2)

Label(frame, text="Pause Typing Shortcut:").grid(row=6, column=0)
pause_entry = Entry(frame)
pause_entry.insert(0, pause_shortcut)
pause_entry.grid(row=6, column=1, columnspan=2, padx=5, pady=2)

Label(frame, text="End Typing Shortcut:").grid(row=7, column=0)
end_entry = Entry(frame)
end_entry.insert(0, end_shortcut)
end_entry.grid(row=7, column=1, columnspan=2, padx=5, pady=2)

shortcut_button = Button(frame, text="Set Shortcuts", command=set_shortcuts)
shortcut_button.grid(row=8, column=1, columnspan=2, pady=5)

# Display current shortcuts
shortcut_label = Label(frame, text=f"Start: {start_shortcut} | Pause: {pause_shortcut} | End: {end_shortcut}")
shortcut_label.grid(row=9, column=0, columnspan=3, pady=10)

# Status label to indicate current typing state
status_label = Label(frame, text="Status: Ready", fg="blue")
status_label.grid(row=10, column=0, columnspan=3, pady=10)

# Register initial shortcuts
register_shortcuts()

# Start Tkinter GUI loop
root.mainloop()
