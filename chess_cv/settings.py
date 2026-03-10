"""
Settings panel for in-game configuration.
"""
import cv2
import numpy as np
from .theme import UITheme, Theme

class SettingsPanel:
    def __init__(self, width=960, height=720):
        self.width = width
        self.height = height
        self.theme = UITheme()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.visible = False
        self.selected_option = 0
        self.options = [
            ("Theme", [
                ("Classic Wood", "classic_wood"),
                ("Pure White", "pure_white"),
                ("High Contrast", "high_contrast"),
                ("Ocean Blue", "ocean_blue"),
                ("Forest Green", "forest_green"),
                ("Royal Purple", "royal_purple")
            ]),
            ("Animations", ["ON", "OFF"]),
            ("Reset Game", ["CONFIRM", "CANCEL"]),
            "Close Settings"
        ]
        self.themes = [Theme.CLASSIC_WOOD, Theme.PURE_WHITE, Theme.HIGH_CONTRAST, Theme.OCEAN_BLUE, Theme.FOREST_GREEN, Theme.ROYAL_PURPLE]
        
    def toggle_visibility(self):
        """Toggle settings panel visibility."""
        self.visible = not self.visible
        return self.visible
    
    def move_selection(self, direction):
        """Move selection up/down."""
        if direction == "up":
            self.selected_option = (self.selected_option - 1) % len(self.options)
        else:
            self.selected_option = (self.selected_option + 1) % len(self.options)
    
    def select_option(self):
        """Execute selected option."""
        if self.selected_option < 4:  # Theme options
            return self.themes[self.selected_option]
        elif self.selected_option == 4:  # Toggle animations
            return "toggle_animations"
        elif self.selected_option == 5:  # Reset game
            return "reset_game"
        else:  # Close settings
            self.visible = False
            return None
    
    def draw(self, img):
        """Draw settings panel."""
        if not self.visible:
            return img
        
        colors = self.theme.get_colors()
        
        # Panel dimensions
        panel_w, panel_h = 400, 350
        panel_x = (self.width - panel_w) // 2
        panel_y = (self.height - panel_h) // 2
        
        # Draw main panel with shadow
        img = self.theme.draw_shadow(img, panel_x, panel_y, panel_w, panel_h)
        self.theme.draw_rounded_rectangle(img, panel_x, panel_y, panel_w, panel_h, 15, colors['panel_bg'], -1)
        self.theme.draw_gradient_border(img, panel_x, panel_y, panel_w, panel_h, 3, colors['accent_color'])
        
        # Draw title
        title_text = "SETTINGS"
        title_size = cv2.getTextSize(title_text, self.font, 0.8, 2)[0]
        title_x = panel_x + (panel_w - title_size[0]) // 2
        title_y = panel_y + 40
        cv2.putText(img, title_text, (title_x, title_y), self.font, 0.8, colors['text_color'], 2, cv2.LINE_AA)
        
        # Draw options
        option_y_start = panel_y + 80
        option_height = 35
        
        for i, option in enumerate(self.options):
            option_y = option_y_start + (i * option_height)
            
            # Highlight selected option
            if i == self.selected_option:
                highlight_color = colors['accent_color']
                self.theme.draw_rounded_rectangle(
                    img, panel_x + 20, option_y - 15, panel_w - 40, 30, 
                    5, highlight_color, -1
                )
                text_color = colors['background']
            else:
                text_color = colors['text_color']
            
            # Draw option text
            text_size = cv2.getTextSize(option, self.font, 0.6, 1)[0]
            text_x = panel_x + (panel_w - text_size[0]) // 2
            cv2.putText(img, option, (text_x, option_y), self.font, 0.6, text_color, 1, cv2.LINE_AA)
        
        # Draw instructions
        instructions = "Use UP/DOWN arrows to navigate, ENTER to select"
        inst_size = cv2.getTextSize(instructions, self.font, 0.5, 1)[0]
        inst_x = panel_x + (panel_w - inst_size[0]) // 2
        inst_y = panel_y + panel_h - 20
        cv2.putText(img, instructions, (inst_x, inst_y), self.font, 0.5, colors['hover_color'], 1, cv2.LINE_AA)
        
        return img
