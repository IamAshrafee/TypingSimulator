# Importing necessary modules
import pyautogui  # For typing automation
import time  # For delays between typing
from tkinter import (
    filedialog,
    Tk,
    Text,
    Button,
    Label,
    Entry,
    Frame,
    Scale,
    messagebox,
)  # GUI components
import threading  # For running typing in a separate thread
import keyboard  # For detecting keyboard shortcuts
import pygetwindow as gw  # For detecting active window
import sys  # For graceful exit handling

# Initialize flags, variables, and default settings
typing_active = False  # Track whether typing should continue
typing_paused = False  # Track if typing is paused
start_shortcut = "ctrl+alt+1"  # Default start shortcut (changed from ctrl+shift+1)
pause_shortcut = "ctrl+alt+p"  # Default pause shortcut
end_shortcut = "ctrl+alt+e"  # Default end shortcut
typing_speed = 10  # Default typing speed (1-30)
shortcuts_registered = False  # Track if shortcuts have been registered
typing_thread = None  # Store the typing thread for proper cleanup


# Function to validate shortcuts (ensure they are not system-reserved)
def validate_shortcut(shortcut):
    forbidden_combinations = ["ctrl+alt+del", "alt+f4", "ctrl+c", "ctrl+v"]
    if shortcut.lower() in forbidden_combinations:
        messagebox.showerror(
            "Invalid Shortcut", f"{shortcut} is a reserved system shortcut!"
        )
        return False
    return True


# Function to wait for the user to focus on the target window
def wait_for_focus():
    time.sleep(2)  # Give user 2 seconds to switch to the desired window
    initial_window = gw.getActiveWindow()  # Store the initial window

    while typing_active and gw.getActiveWindow().title == root.title:
        time.sleep(0.1)  # Wait until focus is no longer on this app

    return initial_window  # Return the target window for later checks


# Function to pause or resume typing
def toggle_pause_typing():
    global typing_paused
    typing_paused = not typing_paused  # Toggle paused state

    # Update UI to reflect pause/resume state
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


# Function to safely end typing and cleanup
def end_typing():
    global typing_active, typing_paused, typing_thread
    typing_active = False  # Stop typing
    typing_paused = False  # Reset paused state

    # Reset UI elements
    root.after(0, lambda: pause_button.config(text="Pause Typing"))
    root.after(0, lambda: status_label.config(text="Status: Stopped"))

    # Wait for the typing thread to finish (if running)
    if typing_thread and typing_thread.is_alive():
        typing_thread.join(timeout=0.5)


# Function to adjust typing speed (smoothed scaling)
def set_typing_speed(value):
    global typing_speed
    typing_speed = int(value)
    # Smoother speed scaling (avoids extreme delays at low speeds)
    return max(0.03, 0.5 / typing_speed)  # Ensures minimum delay of 0.03s


# Core typing function with window focus checks
def type_text(input_text):
    global typing_active, typing_paused

    typing_active = True
    root.after(0, lambda: status_label.config(text="Status: Typing"))

    initial_window = wait_for_focus()  # Get the target window

    for char in input_text:
        if not typing_active:  # Exit if stopped
            break

        while typing_paused:  # Pause if requested
            time.sleep(0.1)

        # Check if the correct window is focused
        current_window = gw.getActiveWindow()
        if current_window != initial_window:
            root.after(
                0, lambda: status_label.config(text="Status: Paused (Wrong Window)")
            )
            while current_window != initial_window and typing_active:
                time.sleep(0.1)
                current_window = gw.getActiveWindow()
            root.after(0, lambda: status_label.config(text="Status: Typing"))

        pyautogui.write(char)  # Type the character
        time.sleep(set_typing_speed(typing_speed))  # Use smoothed speed

    end_typing()  # Clean up when done


# Wrapper function to start typing in a thread
def start_typing_thread(input_text):
    global typing_thread
    end_typing()  # Stop any existing typing
    typing_thread = threading.Thread(
        target=type_text, args=(input_text,), daemon=True
    )
    typing_thread.start()


# Function to type from a file (with encoding support)
def type_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if content:
                start_typing_thread(content)
            else:
                messagebox.showwarning("Empty File", "The selected file is empty!")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please check the path.")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Could not read file (encoding issue).")


# Get text from GUI and start typing
def get_text_input():
    input_text = text_box.get("1.0", "end-1c").strip()
    if input_text:
        start_typing_thread(input_text)
    else:
        messagebox.showwarning("No Text", "Please enter text to type.")


# Let user select a text file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        type_from_file(file_path)


# Customize and validate shortcuts
def set_shortcuts():
    global start_shortcut, pause_shortcut, end_shortcut

    new_start = start_entry.get().strip()
    new_pause = pause_entry.get().strip()
    new_end = end_entry.get().strip()

    # Validate shortcuts before applying
    if (
        validate_shortcut(new_start)
        and validate_shortcut(new_pause)
        and validate_shortcut(new_end)
    ):
        start_shortcut = new_start
        pause_shortcut = new_pause
        end_shortcut = new_end
        update_shortcuts()
        shortcut_label.config(
            text=f"Start: {start_shortcut} | Pause: {pause_shortcut} | End: {end_shortcut}"
        )
        messagebox.showinfo("Success", "Shortcuts updated successfully!")
    else:
        messagebox.showerror("Error", "Invalid shortcut combination!")


# Register/unregister shortcuts safely
def update_shortcuts():
    keyboard.unhook_all()  # Clear existing shortcuts
    try:
        keyboard.add_hotkey(start_shortcut, get_text_input)
        keyboard.add_hotkey(pause_shortcut, toggle_pause_typing)
        keyboard.add_hotkey(end_shortcut, end_typing)
    except Exception as e:
        messagebox.showerror("Shortcut Error", f"Failed to register shortcuts: {e}")


# Cleanup on window close
def on_close():
    end_typing()
    keyboard.unhook_all()
    root.destroy()
    sys.exit(0)


# ===================== GUI SETUP =====================
root = Tk()
root.title("Enhanced Auto Typer v2.0")
root.configure(bg="#2c2c2c")

# Dark mode color scheme
bg_color = "#2c2c2c"
frame_bg = "#202020"
text_color = "#ffffff"
button_color = "#3a3a3a"
highlight_color = "#4a4a4a"

# Main frame for layout
frame = Frame(root, padx=10, pady=10, bg=frame_bg)
frame.pack()

# Text input box
text_box = Text(
    frame,
    height=10,
    width=60,
    wrap="word",
    padx=5,
    pady=5,
    bg=bg_color,
    fg=text_color,
    insertbackground=text_color,
)
text_box.grid(row=0, column=0, columnspan=3, pady=10)

# Action buttons
Button(
    frame,
    text="Start Typing",
    command=get_text_input,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
).grid(row=1, column=0, sticky="ew", padx=5, pady=5)

Button(
    frame,
    text="Type From File",
    command=select_file,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# Control buttons
pause_button = Button(
    frame,
    text="Pause Typing",
    command=toggle_pause_typing,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
)
pause_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

Button(
    frame,
    text="End Typing",
    command=end_typing,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# Typing speed slider
Label(
    frame,
    text="Typing Speed (1=Slow, 30=Fast):",
    bg=frame_bg,
    fg=text_color,
).grid(row=3, column=0, columnspan=2, sticky="w")
speed_slider = Scale(
    frame,
    from_=1,
    to=30,
    orient="horizontal",
    command=lambda v: set_typing_speed(v),
    bg=bg_color,
    fg=text_color,
    highlightbackground=bg_color,
)
speed_slider.set(typing_speed)
speed_slider.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

# Shortcut customization section
Label(frame, text="Custom Shortcuts", bg=frame_bg, fg=text_color).grid(
    row=4, column=0, columnspan=3, pady=(10, 0)
)

Label(frame, text="Start:", bg=frame_bg, fg=text_color).grid(row=5, column=0, sticky="e")
start_entry = Entry(frame, bg=bg_color, fg=text_color, insertbackground=text_color)
start_entry.insert(0, start_shortcut)
start_entry.grid(row=5, column=1, sticky="ew")

Label(frame, text="Pause:", bg=frame_bg, fg=text_color).grid(row=6, column=0, sticky="e")
pause_entry = Entry(frame, bg=bg_color, fg=text_color, insertbackground=text_color)
pause_entry.insert(0, pause_shortcut)
pause_entry.grid(row=6, column=1, sticky="ew")

Label(frame, text="End:", bg=frame_bg, fg=text_color).grid(row=7, column=0, sticky="e")
end_entry = Entry(frame, bg=bg_color, fg=text_color, insertbackground=text_color)
end_entry.insert(0, end_shortcut)
end_entry.grid(row=7, column=1, sticky="ew")

Button(
    frame,
    text="Update Shortcuts",
    command=set_shortcuts,
    bg=button_color,
    fg=text_color,
    activebackground=highlight_color,
).grid(row=8, column=0, columnspan=3, pady=5)

# Current shortcuts display
shortcut_label = Label(
    frame,
    text=f"Active: Start={start_shortcut} | Pause={pause_shortcut} | End={end_shortcut}",
    bg=frame_bg,
    fg="#aaaaaa",
)
shortcut_label.grid(row=9, column=0, columnspan=3)

# Status indicator
status_label = Label(
    frame, text="Status: Stopped", bg=frame_bg, fg=text_color, font=("Arial", 10, "bold")
)
status_label.grid(row=10, column=0, columnspan=3, pady=(10, 5))

# Initialize and run
update_shortcuts()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
