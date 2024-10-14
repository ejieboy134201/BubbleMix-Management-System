# styles.py

import tkinter as tk


class Styles:
    def __init__(self):
        # General styles
        self.main_bg_color = "#FFFFFF"  # Default to white for background
        self.button_bg = "#4CAF50"
        self.button_fg = "#ffffff"
        self.label_fg = "#333333"
        self.font_family = "Arial"

        # Styles for specific widgets
        self.button_style = {
            "bg": self.button_bg,
            "fg": self.button_fg,
            "font": (self.font_family, 14)
        }

        self.label_style = {
            "bg": self.main_bg_color,
            "fg": self.label_fg,
            "font": (self.font_family, 16)
        }

        self.entry_style = {
            "font": (self.font_family, 14),
            "bd": 2,
            "relief": tk.GROOVE
        }

    def create_gradient(self, canvas, width, height):
        """Create a gradient from yellow to white."""
        for i in range(height):
            # Calculate the RGB values for the gradient
            r = int(255 * (i / height) * 0.8) + int(255 * 0.2)  # 20% yellow
            g = int(255 * (i / height) * 0.8)  # 80% white
            b = int(255 * (i / height) * 0.8)  # 80% white
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)

# Example for defining specific styles if needed
styles = Styles()
