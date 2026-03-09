"""
Gesture guide overlay for showing hand gesture instructions.
"""
import cv2
import numpy as np
from .theme import UITheme

class GestureGuide:
    def __init__(self, width=960, height=720):
        self.width = width
        self.height = height
        self.theme = UITheme()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.visible = False
        self.animation_frame = 0
        
    def toggle_visibility(self):
        """Toggle gesture guide visibility."""
        self.visible = not self.visible
        return self.visible
    
    def draw_hand_illustration(self, img, x, y, gesture_type):
        """Draw simple hand illustration for gesture."""
        colors = self.theme.get_colors()
        
        if gesture_type == "pinch":
            # Draw pinching hand (thumb and index finger together)
            # Palm
            cv2.circle(img, (x, y + 20), 15, colors['text_color'], -1)
            # Thumb
            cv2.circle(img, (x - 8, y + 10), 6, colors['text_color'], -1)
            # Index finger
            cv2.circle(img, (x - 5, y + 5), 6, colors['text_color'], -1)
            # Other fingers
            cv2.circle(img, (x + 8, y + 5), 4, colors['text_color'], -1)
            cv2.circle(img, (x + 12, y), 4, colors['text_color'], -1)
            cv2.circle(img, (x + 10, y - 5), 4, colors['text_color'], -1)
            
        elif gesture_type == "drag":
            # Draw dragging hand (pinch with motion lines)
            cv2.circle(img, (x, y + 20), 15, colors['text_color'], -1)
            cv2.circle(img, (x - 8, y + 10), 6, colors['text_color'], -1)
            cv2.circle(img, (x - 5, y + 5), 6, colors['text_color'], -1)
            # Motion lines
            for i in range(3):
                line_x = x - 20 - (i * 8)
                cv2.line(img, (line_x, y), (line_x + 5, y), colors['accent_color'], 2)
                
        elif gesture_type == "release":
            # Draw releasing hand (open fingers)
            cv2.circle(img, (x, y + 20), 15, colors['text_color'], -1)
            cv2.circle(img, (x - 12, y + 15), 5, colors['text_color'], -1)  # Thumb
            cv2.circle(img, (x - 8, y), 5, colors['text_color'], -1)      # Index
            cv2.circle(img, (x, y - 5), 5, colors['text_color'], -1)      # Middle
            cv2.circle(img, (x + 8, y), 5, colors['text_color'], -1)       # Ring
            cv2.circle(img, (x + 10, y + 5), 5, colors['text_color'], -1)  # Pinky
    
    def draw(self, img):
        """Draw gesture guide overlay."""
        if not self.visible:
            return img
        
        colors = self.theme.get_colors()
        
        # Semi-transparent overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (0, 0, 0), -1)
        img = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
        
        # Main panel
        panel_w, panel_h = 600, 400
        panel_x = (self.width - panel_w) // 2
        panel_y = (self.height - panel_h) // 2
        
        img = self.theme.draw_shadow(img, panel_x, panel_y, panel_w, panel_h)
        self.theme.draw_rounded_rectangle(img, panel_x, panel_y, panel_w, panel_h, 20, colors['panel_bg'], -1)
        self.theme.draw_gradient_border(img, panel_x, panel_y, panel_w, panel_h, 4, colors['accent_color'])
        
        # Title
        title_text = "GESTURE CONTROLS"
        title_size = cv2.getTextSize(title_text, self.font, 0.9, 2)[0]
        title_x = panel_x + (panel_w - title_size[0]) // 2
        title_y = panel_y + 50
        cv2.putText(img, title_text, (title_x, title_y), self.font, 0.9, colors['text_color'], 2, cv2.LINE_AA)
        
        # Gesture instructions
        gestures = [
            {
                "title": "SELECT PIECE",
                "description": "Pinch thumb and index finger together",
                "gesture": "pinch",
                "y": panel_y + 120
            },
            {
                "title": "MOVE PIECE", 
                "description": "Drag while maintaining pinch",
                "gesture": "drag",
                "y": panel_y + 220
            },
            {
                "title": "DROP PIECE",
                "description": "Release fingers to place piece",
                "gesture": "release", 
                "y": panel_y + 320
            }
        ]
        
        for i, gesture in enumerate(gestures):
            # Draw hand illustration
            hand_x = panel_x + 80
            hand_y = gesture["y"]
            self.draw_hand_illustration(img, hand_x, hand_y, gesture["gesture"])
            
            # Draw title
            title_x = panel_x + 150
            title_y = gesture["y"] - 10
            cv2.putText(img, gesture["title"], (title_x, title_y), self.font, 0.7, colors['accent_color'], 2, cv2.LINE_AA)
            
            # Draw description
            desc_x = panel_x + 150
            desc_y = gesture["y"] + 15
            cv2.putText(img, gesture["description"], (desc_x, desc_y), self.font, 0.5, colors['text_color'], 1, cv2.LINE_AA)
        
        # Close instruction
        close_text = "Press 'G' to close guide"
        close_size = cv2.getTextSize(close_text, self.font, 0.6, 1)[0]
        close_x = panel_x + (panel_w - close_size[0]) // 2
        close_y = panel_y + panel_h - 30
        cv2.putText(img, close_text, (close_x, close_y), self.font, 0.6, colors['hover_color'], 1, cv2.LINE_AA)
        
        # Animated indicator
        self.animation_frame = (self.animation_frame + 1) % 60
        if self.animation_frame < 30:
            pulse_color = colors['legal_color']
        else:
            pulse_color = colors['hover_color']
        
        cv2.circle(img, (panel_x + panel_w - 30, panel_y + 30), 8, pulse_color, -1)
        
        return img
