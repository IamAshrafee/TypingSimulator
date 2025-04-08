# 🔠 Enhanced Auto Typer

A powerful, feature-rich typing automation tool with customizable speed, keyboard shortcuts, and window focus awareness. Perfect for automating repetitive typing tasks efficiently.

![image](https://github.com/user-attachments/assets/42257175-421c-406b-a67d-545f619d89bc) *(Example screenshot)*


## ✨ Features

- 🚀 **Text & File Typing** - Type from direct input or text files
- ⚡ **Adjustable Speed** - Control typing speed from 1 (slow) to 30 (fast)
- ⌨️ **Custom Shortcuts** - Configure your own keyboard combinations
- 🖥️ **Window Awareness** - Auto-pauses when window focus changes
- ⏯️ **Pause/Resume** - Full control during typing sessions
- 🎨 **Dark Mode UI** - Easy on the eyes during extended use

## 📦 Installation

1. **Prerequisites**:
   - Python 3.6+
   - Required packages:
   

   ```bash
   pip install pyautogui keyboard pygetwindow

   ```

2. **Download**:
   ```bash
   git clone https://github.com/yourusername/enhanced-auto-typer.git
   cd enhanced-auto-typer
   ```

3. **Run the Script**:
   ```bash
   python auto_typer.py
   ```
   
---

**Basic Controls**:
- `Start Typing`: Types text from the input box
- `Type From File`: Loads text from a .txt file
- `Pause/Resume`: Toggles typing pause state
- `End Typing`: Stops current typing session

**Default Shortcuts**:
- Start: `Ctrl+Alt+1`
- Pause: `Ctrl+Alt+P`
- Stop: `Ctrl+Alt+E`

## ⚙️ Customization

Modify `auto_typer.py` to:
- Change default shortcuts (lines 12-14)
- Adjust UI colors (search for `bg_color`, `text_color`)
- Modify typing speed calculation (function `set_typing_speed`)

## 🤝 Contributing

Pull requests welcome! For major changes, please open an issue first.

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)

---

💡 **Pro Tip**: Run as Administrator on Windows for best shortcut reliability.
