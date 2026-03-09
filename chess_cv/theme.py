"""
Theme system for modern UI with multiple visual styles.
"""
import numpy as np
import cv2
from enum import Enum

class Theme(Enum):
    CLASSIC_WOOD = "classic_wood"
    MARBLE = "marble"
    MODERN = "modern"
    DARK = "dark"

class UITheme:
    def __init__(self, theme=Theme.CLASSIC_WOOD):
        self.current_theme = theme
        self.themes = {
            Theme.CLASSIC_WOOD: {
                'board_colors': [(222, 202, 163), (139, 108, 66)],
                'border_color': (92, 64, 31),
                'highlight_color': (255, 223, 0),
                'selected_color': (0, 128, 255),
                'legal_color': (0, 255, 0),
                'illegal_color': (255, 0, 0),
                'hover_color': (255, 255, 0),
                'check_color': (255, 0, 0),
                'background': (45, 45, 48),
                'panel_bg': (60, 60, 63),
                'text_color': (255, 255, 255),
                'accent_color': (0, 122, 255)
            },
            Theme.MARBLE: {
                'board_colors': [(245, 245, 245), (52, 52, 52)],
                'border_color': (180, 180, 180),
                'highlight_color': (100, 200, 255),
                'selected_color': (0, 150, 255),
                'legal_color': (0, 255, 150),
                'illegal_color': (255, 100, 100),
                'hover_color': (150, 200, 255),
                'check_color': (255, 50, 50),
                'background': (30, 30, 35),
                'panel_bg': (40, 40, 45),
                'text_color': (255, 255, 255),
                'accent_color': (100, 200, 255)
            },
            Theme.MODERN: {
                'board_colors': [(255, 248, 220), (70, 130, 180)],
                'border_color': (50, 100, 150),
                'highlight_color': (255, 200, 0),
                'selected_color': (255, 100, 0),
                'legal_color': (0, 255, 100),
                'illegal_color': (255, 50, 50),
                'hover_color': (255, 180, 0),
                'check_color': (255, 0, 100),
                'background': (20, 25, 40),
                'panel_bg': (30, 35, 50),
                'text_color': (255, 255, 255),
                'accent_color': (0, 200, 255)
            },
            Theme.DARK: {
                'board_colors': [(80, 80, 80), (20, 20, 20)],
                'border_color': (60, 60, 60),
                'highlight_color': (150, 150, 255),
                'selected_color': (100, 100, 255),
                'legal_color': (100, 255, 100),
                'illegal_color': (255, 100, 100),
                'hover_color': (200, 200, 150),
                'check_color': (255, 100, 100),
                'background': (10, 10, 15),
                'panel_bg': (20, 20, 25),
                'text_color': (255, 255, 255),
                'accent_color': (150, 150, 255)
            }
        }
    
    def get_colors(self):
        return self.themes[self.current_theme]
    
    def set_theme(self, theme):
        if isinstance(theme, str):
            theme = Theme(theme)
        self.current_theme = theme
    
    def draw_gradient_border(self, img, x, y, w, h, thickness=3, color=None):
        """Draw a gradient border around a rectangle."""
        if color is None:
            color = self.get_colors()['border_color']
        
        # Create gradient effect
        for i in range(thickness):
            alpha = 1.0 - (i / thickness) * 0.5
            current_color = tuple(int(c * alpha) for c in color)
            cv2.rectangle(img, (x + i, y + i), (x + w - i, y + h - i), current_color, 1)
    
    def draw_shadow(self, img, x, y, w, h, offset=5, blur=3):
        """Draw a soft shadow effect."""
        shadow_color = (0, 0, 0)
        
        # Create shadow rectangle
        shadow_img = img.copy()
        cv2.rectangle(shadow_img, (x + offset, y + offset), (x + w + offset, y + h + offset), shadow_color, -1)
        
        # Apply blur for soft shadow
        shadow_blurred = cv2.GaussianBlur(shadow_img, (blur * 2 + 1, blur * 2 + 1), 0)
        
        # Blend shadow back to original image
        alpha = 0.3
        img = cv2.addWeighted(img, 1 - alpha, shadow_blurred, alpha, 0)
        
        return img
    
    def draw_rounded_rectangle(self, img, x, y, w, h, radius, color, thickness=-1):
        """Draw a rounded rectangle."""
        if radius > min(w, h) // 2:
            radius = min(w, h) // 2
        
        # Draw the main rectangle
        if thickness == -1:
            cv2.rectangle(img, (x + radius, y), (x + w - radius, y + h), color, -1)
            cv2.rectangle(img, (x, y + radius), (x + w, y + h - radius), color, -1)
        else:
            cv2.rectangle(img, (x + radius, y), (x + w - radius, y + h), color, thickness)
            cv2.rectangle(img, (x, y + radius), (x + w, y + h - radius), color, thickness)
        
        # Draw the corners
        cv2.circle(img, (x + radius, y + radius), radius, color, thickness)
        cv2.circle(img, (x + w - radius, y + radius), radius, color, thickness)
        cv2.circle(img, (x + radius, y + h - radius), radius, color, thickness)
        cv2.circle(img, (x + w - radius, y + h - radius), radius, color, thickness)
    
    def draw_panel(self, img, x, y, w, h, title="", content=""):
        """Draw a modern UI panel with shadow and rounded corners."""
        colors = self.get_colors()
        
        # Draw shadow
        img = self.draw_shadow(img, x, y, w, h)
        
        # Draw panel background
        self.draw_rounded_rectangle(img, x, y, w, h, 10, colors['panel_bg'], -1)
        
        # Draw border
        self.draw_gradient_border(img, x, y, w, h, 2, colors['accent_color'])
        
        # Draw title
        if title:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + 25
            cv2.putText(img, title, (text_x, text_y), font, font_scale, colors['text_color'], thickness, cv2.LINE_AA)
        
        # Draw content
        if content:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            lines = content.split('\n')
            for i, line in enumerate(lines):
                text_y = y + 50 + (i * 20)
                cv2.putText(img, line, (x + 10, text_y), font, font_scale, colors['text_color'], thickness, cv2.LINE_AA)
        
        return img
