# Keyboard Smasher

A lightweight Python script that tracks your keyboard key presses and displays a floating counter window with a cool combo effect.

## Features

- Counts your key presses globally on macOS.

- Shows a floating window with the current combo count.

- Stylish pink and outlined labels for the counter and "HITS" text.

- Automatically resets count after inactivity.

## Requirements

- macOS

- Python 3.6+

- `pyobjc` package (for macOS GUI and event tapping)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/key-smasher.git
cd key-smasher
```

2. Install the required Python package:

```bash
python3 -m pip install pyobjc
```

## Usage

Run the script directly from the terminal:

```bash
python3 keytracker.py
```

## Important Notes

- The script requires **Accessibility permissions** to monitor keyboard events on macOS.

To enable:

1. Open **System Preferences → Security & Privacy → Privacy** tab.

2. Select **Accessibility** from the sidebar.

3. Click the + button and add your terminal app (e.g., Terminal or iTerm) or the Python interpreter you use.

4. Restart the terminal and run the script again.

- The floating window starts hidden and appears only after you press keys.

## Troubleshooting

- If you don't see the floating window after running, make sure Accessibility permissions are granted.

- Run the script from Terminal and watch for error messages.
