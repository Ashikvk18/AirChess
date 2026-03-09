"""
HUD overlay system for displaying game information and modern UI elements.
"""
import cv2
import numpy as np
import chess
from .theme import UITheme

class HUDOverlay:
    def __init__(self, width=960, height=720):
        self.width = width
        self.height = height
        self.theme = UITheme()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.small_font = cv2.FONT_HERSHEY_SIMPLEX
        
    def draw_turn_indicator(self, img, board, human_turn=True):
        """Draw turn indicator with modern styling."""
        colors = self.theme.get_colors()
        
        # Panel dimensions
        panel_w, panel_h = 200, 60
        panel_x = self.width - panel_w - 20
        panel_y = 20
        
        # Draw panel
        img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h)
        
        # Turn text
        turn_text = "YOUR TURN" if human_turn else "COMPUTER"
        turn_color = colors['legal_color'] if human_turn else colors['illegal_color']
        
        text_size = cv2.getTextSize(turn_text, self.font, 0.7, 2)[0]
        text_x = panel_x + (panel_w - text_size[0]) // 2
        text_y = panel_y + 35
        
        cv2.putText(img, turn_text, (text_x, text_y), self.font, 0.7, turn_color, 2, cv2.LINE_AA)
        
        return img
    
    def draw_game_status(self, img, board):
        """Draw game status (check, checkmate, stalemate)."""
        colors = self.theme.get_colors()
        
        status_text = ""
        status_color = colors['text_color']
        
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                status_text = "BLACK WINS!"
            else:
                status_text = "WHITE WINS!"
            status_color = colors['check_color']
        elif board.is_stalemate():
            status_text = "STALEMATE"
            status_color = colors['hover_color']
        elif board.is_check():
            status_text = "CHECK!"
            status_color = colors['check_color']
        elif board.is_insufficient_material():
            status_text = "DRAW (INSUFFICIENT)"
            status_color = colors['hover_color']
        
        if status_text:
            # Draw status panel
            panel_w, panel_h = 250, 50
            panel_x = (self.width - panel_w) // 2
            panel_y = 20
            
            img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h, "GAME STATUS", status_text)
            
            # Pulsing effect for check/checkmate
            if "CHECK" in status_text:
                import time
                pulse = abs(np.sin(time.time() * 3))
                border_color = tuple(int(c * pulse) for c in status_color)
                cv2.rectangle(img, (panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h), border_color, 3)
        
        return img
    
    def draw_move_history(self, img, move_history, max_moves=5):
        """Draw recent move history."""
        colors = self.theme.get_colors()
        
        if not move_history:
            return img
        
        # Panel dimensions
        panel_w, panel_h = 180, 150
        panel_x = 20
        panel_y = 20
        
        # Draw panel
        img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h, "RECENT MOVES")
        
        # Draw moves
        recent_moves = move_history[-max_moves:] if len(move_history) > max_moves else move_history
        for i, move in enumerate(recent_moves):
            move_text = str(move)
            text_y = panel_y + 50 + (i * 20)
            cv2.putText(img, move_text, (panel_x + 10, text_y), self.small_font, 0.5, colors['text_color'], 1, cv2.LINE_AA)
        
        return img
    
    def draw_controls_help(self, img):
        """Draw control instructions."""
        colors = self.theme.get_colors()
        
        # Panel dimensions
        panel_w, panel_h = 200, 120
        panel_x = 20
        panel_y = self.height - panel_h - 20
        
        help_text = "Pinch to select\nDrag to move\nRelease to drop\nESC to quit"
        
        img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h, "CONTROLS", help_text)
        
        return img
    
    def draw_fps_counter(self, img, fps):
        """Draw FPS counter."""
        colors = self.theme.get_colors()
        
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(img, fps_text, (self.width - 80, self.height - 10), self.small_font, 0.4, colors['text_color'], 1, cv2.LINE_AA)
        
        return img
    
    def draw_theme_indicator(self, img, theme_name):
        """Draw current theme indicator."""
        colors = self.theme.get_colors()
        
        theme_text = f"Theme: {theme_name.replace('_', ' ').title()}"
        cv2.putText(img, theme_text, (20, self.height - 10), self.small_font, 0.4, colors['accent_color'], 1, cv2.LINE_AA)
        
        return img
    
    def draw_captured_pieces(self, img, white_captured, black_captured):
        """Draw captured pieces display."""
        colors = self.theme.get_colors()
        
        # White captured pieces panel
        if white_captured:
            panel_w, panel_h = 200, 80
            panel_x = self.width - panel_w - 20
            panel_y = self.height - panel_h - 20
            
            captured_text = "Lost by White: " + " ".join(white_captured)
            img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h, "CAPTURED", captured_text)
        
        # Black captured pieces panel
        if black_captured:
            panel_w, panel_h = 200, 80
            panel_x = self.width - panel_w - 20
            panel_y = self.height - panel_h - 110
            
            captured_text = "Lost by Black: " + " ".join(black_captured)
            img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h, "CAPTURED", captured_text)
        
        return img
    
    def draw_settings_hint(self, img):
        """Draw settings hint."""
        colors = self.theme.get_colors()
        
        hint_text = "Press 'T' to change theme"
        cv2.putText(img, hint_text, (self.width // 2 - 100, self.height - 10), self.small_font, 0.4, colors['accent_color'], 1, cv2.LINE_AA)
        
        return img
