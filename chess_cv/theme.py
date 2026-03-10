"""
Theme system for modern UI with multiple visual styles.
"""
import numpy as np
import cv2
from enum import Enum

class Theme(Enum):
    NEON_CYBER = "neon_cyber"
    SUNSET_VIBRANT = "sunset_vibrant"
    OCEAN_BREEZE = "ocean_breeze"
    FOREST_EMERALD = "forest_emerald"
    GALAXY_PURPLE = "galaxy_purple"
    FIRE_OPAL = "fire_opal"

class UITheme:
    def __init__(self, theme=Theme.NEON_CYBER):
        self.current_theme = theme
        self.themes = {
            Theme.NEON_CYBER: {
                'board_colors': [(15, 15, 35), (255, 20, 147)],
                'border_color': (0, 255, 255),
                'highlight_color': (255, 255, 0),
                'selected_color': (0, 255, 127),
                'legal_color': (255, 105, 180),
                'illegal_color': (255, 69, 0),
                'hover_color': (138, 43, 226),
                'check_color': (255, 0, 255),
                'background': (5, 5, 15),
                'panel_bg': (10, 10, 25),
                'text_color': (0, 255, 255),
                'accent_color': (0, 255, 255)
            },
            Theme.SUNSET_VIBRANT: {
                'board_colors': [(255, 94, 77), (255, 206, 84)],
                'border_color': (255, 157, 77),
                'highlight_color': (255, 255, 255),
                'selected_color': (255, 0, 128),
                'legal_color': (128, 255, 0),
                'illegal_color': (255, 0, 64),
                'hover_color': (255, 128, 0),
                'check_color': (255, 0, 255),
                'background': (25, 25, 35),
                'panel_bg': (45, 25, 35),
                'text_color': (255, 255, 255),
                'accent_color': (255, 94, 77)
            },
            Theme.OCEAN_BREEZE: {
                'board_colors': [(0, 119, 190), (144, 224, 239)],
                'border_color': (0, 180, 216),
                'highlight_color': (255, 255, 0),
                'selected_color': (0, 255, 127),
                'legal_color': (72, 209, 204),
                'illegal_color': (255, 99, 71),
                'hover_color': (64, 224, 208),
                'check_color': (255, 20, 147),
                'background': (10, 20, 30),
                'panel_bg': (20, 40, 60),
                'text_color': (255, 255, 255),
                'accent_color': (0, 191, 255)
            },
            Theme.FOREST_EMERALD: {
                'board_colors': [(34, 139, 34), (144, 238, 144)],
                'border_color': (0, 100, 0),
                'highlight_color': (255, 215, 0),
                'selected_color': (50, 205, 50),
                'legal_color': (0, 255, 127),
                'illegal_color': (220, 20, 60),
                'hover_color': (173, 255, 47),
                'check_color': (255, 69, 0),
                'background': (15, 25, 15),
                'panel_bg': (25, 45, 25),
                'text_color': (255, 255, 255),
                'accent_color': (50, 205, 50)
            },
            Theme.GALAXY_PURPLE: {
                'board_colors': [(75, 0, 130), (138, 43, 226)],
                'border_color': (186, 85, 211),
                'highlight_color': (255, 215, 0),
                'selected_color': (255, 0, 255),
                'legal_color': (147, 112, 219),
                'illegal_color': (255, 0, 128),
                'hover_color': (218, 112, 214),
                'check_color': (255, 105, 180),
                'background': (20, 10, 30),
                'panel_bg': (40, 20, 60),
                'text_color': (255, 255, 255),
                'accent_color': (186, 85, 211)
            },
            Theme.FIRE_OPAL: {
                'board_colors': [(255, 69, 0), (255, 140, 0)],
                'border_color': (255, 165, 0),
                'highlight_color': (255, 255, 0),
                'selected_color': (255, 20, 147),
                'legal_color': (255, 215, 0),
                'illegal_color': (139, 0, 0),
                'hover_color': (255, 99, 71),
                'check_color': (255, 0, 0),
                'background': (30, 15, 10),
                'panel_bg': (50, 25, 20),
                'text_color': (255, 255, 255),
                'accent_color': (255, 140, 0)
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
        """Draw a modern UI panel with enhanced visual design."""
        colors = self.get_colors()
        
        # Draw enhanced shadow with blur effect
        shadow_img = img.copy()
        shadow_offset = 12
        shadow_alpha = 0.4
        
        # Create shadow with gradient
        for i in range(8):
            alpha = shadow_alpha * (1 - i/8)
            shadow_color = (0, 0, 0)
            offset = shadow_offset - i
            cv2.rectangle(shadow_img, (x + offset, y + offset), 
                         (x + w + offset, y + h + offset), shadow_color, -1)
        
        # Blend shadow back
        img = cv2.addWeighted(img, 1.0, shadow_img, 0.3, 0)
        
        # Draw main panel background with gradient
        panel_bg = colors['panel_bg']
        cv2.rectangle(img, (x, y), (x + w, y + h), panel_bg, -1)
        
        # Add gradient overlay for depth
        gradient = img.copy()
        for i in range(min(h//4, 20)):
            alpha = 1.0 - (i / (h//4))
            gradient_color = tuple(int(c * alpha) for c in colors['accent_color'])
            cv2.line(gradient, (x, y + i), (x + w, y + i), gradient_color, 1)
        
        img = cv2.addWeighted(img, 0.85, gradient, 0.15, 0)
        
        # Draw modern border with rounded corners effect
        border_color = colors['accent_color']
        cv2.rectangle(img, (x, y), (x + w, y + h), border_color, 2)
        
        # Draw inner highlight
        inner_highlight = tuple(min(255, c + 30) for c in colors['accent_color'])
        cv2.rectangle(img, (x + 2, y + 2), (x + w - 2, y + h - 2), inner_highlight, 1)
        
        # Draw title with enhanced styling
        if title:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + 30
            
            # Draw text shadow
            cv2.putText(img, title, (text_x + 1, text_y + 1), font, font_scale, 
                       (0, 0, 0), thickness + 1, cv2.LINE_AA)
            
            # Draw main text
            cv2.putText(img, title, (text_x, text_y), font, font_scale, 
                       colors['text_color'], thickness, cv2.LINE_AA)
            
            # Draw title underline
            underline_y = text_y + 8
            cv2.line(img, (text_x - 5, underline_y), 
                    (text_x + text_size[0] + 5, underline_y), 
                    colors['accent_color'], 2)
        
        # Draw content with better formatting
        if content:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            lines = content.split('\n')
            for i, line in enumerate(lines):
                text_y = y + 55 + (i * 22)
                
                # Draw text shadow for better readability
                cv2.putText(img, line, (x + 15, text_y + 1), font, font_scale, 
                           (0, 0, 0), thickness + 1, cv2.LINE_AA)
                
                # Draw main text
                cv2.putText(img, line, (x + 15, text_y), font, font_scale, 
                           colors['text_color'], thickness, cv2.LINE_AA)
        
        return img
