# Importing necessary modules
import pyautogui  # For typing automation
import time  # To introduce delays between typing
from tkinter import (
    filedialog,
    Tk,
    Text,
    Button,
    Label,
    Entry,
    Frame,
    Scale,
)  # GUI components
import threading  # For running typing in a separate thread
import keyboard  # For detecting keyboard shortcuts
import pygetwindow as gw  # For detecting active window

# Initialize flags, variables, and default settings
typing_active = False  # Track whether typing should continue
typing_paused = False  # Track if typing is paused
start_shortcut = "ctrl+shift+1"
pause_shortcut = "ctrl+shift+p"
end_shortcut = "ctrl+shift+e"
typing_speed = 10  # Default typing speed
shortcuts_registered = False  # Track if shortcuts have been registered


# Function to allow setting the typing window focus
def wait_for_focus():
    time.sleep(5)  # Give user 2 seconds to switch to desired typing window
    while typing_active and gw.getActiveWindow().title == root.title:
        time.sleep(0.1)  # Wait until the focus is no longer on this app


# Function to pause or resume typing
def toggle_pause_typing():
    global typing_paused
    typing_paused = not typing_paused  # Toggle paused state
    root.after(
        0,
        lambda: pause_button.config(
            text="Resume Typing" if typing_paused else "Pause Typing"
        ),
    )
    root.after(
        0,
        lambda: status_label.config(
            text="Status: Paused" if typing_paused else "Status: Typing"
        ),
    )


# Function to end typing and reset
def end_typing():
    global typing_active, typing_paused
    typing_active = False  # Stop typing
    typing_paused = False  # Reset paused state
    root.after(
        0, lambda: pause_button.config(text="Pause Typing")
    )  # Reset button label
    root.after(
        0, lambda: status_label.config(text="Status: Stopped")
    )  # Update status label


# Function to adjust typing speed from the slider
def set_typing_speed(value):
    global typing_speed
    typing_speed = int(value)  # Update typing speed from slider value


# Function to type the given input (word, sentence, or paragraph) with window locking
def type_text(input_text):
    global typing_active, typing_paused
    typing_active = True  # Allow typing
    root.after(
        0, lambda: status_label.config(text="Status: Typing")
    )  # Update status to Typing

    # Capture the initial target window where typing begins
    initial_window = gw.getActiveWindow()  # Get the current active window

    wait_for_focus()  # Wait for user to set the focus to a typing area

    for char in input_text:
        if not typing_active:  # Stop typing if ended
            break
        while typing_paused:  # Pause typing if paused
            time.sleep(0.1)  # Small delay to avoid high CPU usage

        # Check if the active window is still the initial window
        current_window = gw.getActiveWindow()
        if current_window != initial_window:  # If user switches to another window
            root.after(
                0, lambda: status_label.config(text="Status: Paused (Wrong Window)")
            )
            while (
                current_window != initial_window
            ):  # Wait until the user returns to the original window
                time.sleep(0.1)  # Poll every 0.1 seconds to check the window
                current_window = gw.getActiveWindow()
            root.after(
                0, lambda: status_label.config(text="Status: Typing")
            )  # Resume typing once back in the target window

        pyautogui.write(char)  # Type each character where the cursor is focused
        time.sleep(
            max(0.02, 0.1 / typing_speed)
        )  # Adjust typing speed with minimum threshold

    root.after(
        0, lambda: status_label.config(text="Status: Stopped")
    )  # Update status when done


# Wrapper function to start typing in a new thread
def start_typing_thread(input_text):
    threading.Thread(target=type_text, args=(input_text,), daemon=True).start()


# Function to type contents of the text file
def type_from_file(file_path):
    try:
        with open(file_path, "r") as file:  # Open the file in read mode
            content = file.read()  # Read the entire file content
            start_typing_thread(content)  # Start typing in a new thread
    except FileNotFoundError:
        print("File not found. Please check the path.")
        root.after(
            0, lambda: status_label.config(text="Status: File Not Found")
        )  # Update status on error


# Function to get text input from user and start typing
def get_text_input():
    input_text = text_box.get("1.0", "end-1c").strip()  # Get text from text box
    if input_text:  # Check if text is present
        start_typing_thread(input_text)  # Start typing in a new thread


# Function to let user select a file and start typing its content
def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )  # Limit to text files only
    if file_path:  # Check if a file was selected
        type_from_file(file_path)  # Start typing in a new thread


# Function to customize shortcuts
def set_shortcuts():
    global start_shortcut, pause_shortcut, end_shortcut
    start_shortcut = start_entry.get().strip()
    pause_shortcut = pause_entry.get().strip()
    end_shortcut = end_entry.get().strip()
    shortcut_label.config(
        text=f"Start: {start_shortcut} | Pause: {pause_shortcut} | End: {end_shortcut}"
    )


# Setting up keyboard shortcuts with a check to prevent duplicate registrations
def register_shortcuts():
    global shortcuts_registered
    if not shortcuts_registered:
        keyboard.add_hotkey(
            start_shortcut, get_text_input
        )  # Start typing with shortcut
        keyboard.add_hotkey(
            pause_shortcut, toggle_pause_typing
        )  # Pause/resume with shortcut
        keyboard.add_hotkey(end_shortcut, end_typing)  # End typing with shortcut
        shortcuts_registered = True


# Tkinter GUI setup with dark mode
root = Tk()
root.title("Enhanced Auto Typer")
root.configure(bg="#2c2c2c")

# Define color scheme for dark mode
bg_color = "#2c2c2c"
frame_bg = "#202020"
text_color = "#ffffff"
button_color = "#2c2c2c"
highlight_color = "#383838"

# Align UI elements with a Frame for better structure and spacing
frame = Frame(root, padx=10, pady=10, bg=frame_bg)
frame.pack()

# Text box for inputting text
text_box = Text(
    frame,
    height=10,
    width=50,
    wrap="word",
    padx=5,
    pady=5,
    bg=bg_color,
    fg=text_color,
    insertbackground=text_color,
)
text_box.grid(row=0, column=0, columnspan=3, pady=10)

# Button to start typing the text entered in the text box
type_button = Button(
    frame,
    text="Start Typing",
    command=get_text_input,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
)
type_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

# Button to select a file and start typing its content
file_button = Button(
    frame,
    text="Type From File",
    command=select_file,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
)
file_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# Pause/Resume button for toggling typing state
pause_button = Button(
    frame,
    text="Pause Typing",
    command=toggle_pause_typing,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
)
pause_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

# Button to end typing
end_button = Button(
    frame,
    text="End Typing",
    command=end_typing,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
)
end_button.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# Typing speed adjustment with a slider
Label(
    frame, text="Typing Speed (10 = Fast, 1 = Slow):", bg=frame_bg, fg=text_color
).grid(row=3, column=0, columnspan=2)
speed_slider = Scale(
    frame,
    from_=1,
    to=30,
    orient="horizontal",
    command=set_typing_speed,
    bg=bg_color,
    fg=text_color,
    highlightbackground=bg_color,
)
speed_slider.set(typing_speed)
speed_slider.grid(row=3, column=2, padx=5, pady=5)

# Shortcut customization
Label(frame, text="Customize Shortcuts", bg=frame_bg, fg=text_color).grid(
    row=4, column=0, columnspan=3, pady=10
)
Label(frame, text="Start Typing Shortcut:", bg=frame_bg, fg=text_color).grid(
    row=5, column=0
)
start_entry = Entry(frame, bg=bg_color, fg=text_color, insertbackground=text_color)
start_entry.insert(0, start_shortcut)
start_entry.grid(row=5, column=1)

Label(frame, text="Pause Typing Shortcut:", bg=frame_bg, fg=text_color).grid(
    row=6, column=0
)
pause_entry = Entry(frame, bg=bg_color, fg=text_color, insertbackground=text_color)
pause_entry.insert(0, pause_shortcut)
pause_entry.grid(row=6, column=1)

Label(frame, text="End Typing Shortcut:", bg=frame_bg, fg=text_color).grid(
    row=7, column=0
)
end_entry = Entry(frame, bg=bg_color, fg=text_color, insertbackground=text_color)
end_entry.insert(0, end_shortcut)
end_entry.grid(row=7, column=1)

# Button to save and set the shortcuts
shortcut_button = Button(
    frame,
    text="Set Shortcuts",
    command=set_shortcuts,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
)
shortcut_button.grid(row=8, column=0, columnspan=3, pady=5)

# Label to show the currently set shortcuts
shortcut_label = Label(
    frame,
    text=f"Start: {start_shortcut} | Pause: {pause_shortcut} | End: {end_shortcut}",
    bg=frame_bg,
    fg=text_color,
)
shortcut_label.grid(row=9, column=0, columnspan=3)

# Status label to show current status (Typing, Paused, Stopped, etc.)
status_label = Label(frame, text="Status: Stopped", bg=frame_bg, fg=text_color)
status_label.grid(row=10, column=0, columnspan=3, pady=10)

# Register the shortcuts and start the Tkinter main loop
register_shortcuts()
root.mainloop()
