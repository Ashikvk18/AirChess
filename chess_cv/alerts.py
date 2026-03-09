"""
Alert system for check, checkmate, and other game events with visual animations.
"""
import cv2
import numpy as np
import chess
import time
from .theme import UITheme
from .animations import ParticleEffect

class GameAlertSystem:
    def __init__(self, width=960, height=720):
        self.width = width
        self.height = height
        self.theme = UITheme()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.alerts = []
        self.particle_effects = []
        self.flash_effect = {'active': False, 'start_time': 0, 'duration': 1.0, 'color': (255, 0, 0)}
        
    def add_check_alert(self, king_square):
        """Add check alert with visual effects."""
        colors = self.theme.get_colors()
        
        # Add alert message
        alert = {
            'type': 'check',
            'message': 'CHECK!',
            'start_time': time.time(),
            'duration': 3.0,
            'color': colors['check_color'],
            'king_square': king_square
        }
        self.alerts.append(alert)
        
        # Add flash effect
        self.flash_effect = {
            'active': True,
            'start_time': time.time(),
            'duration': 0.8,
            'color': colors['check_color']
        }
        
        # Add particle effects around king
        x, y = king_square
        for _ in range(3):
            effect = ParticleEffect(x, y, colors['check_color'], 8)
            self.particle_effects.append(effect)
    
    def add_checkmate_alert(self, winner_color):
        """Add checkmate alert with celebration effects."""
        colors = self.theme.get_colors()
        
        winner_text = "WHITE WINS!" if winner_color == chess.WHITE else "BLACK WINS!"
        
        alert = {
            'type': 'checkmate',
            'message': winner_text,
            'start_time': time.time(),
            'duration': 5.0,
            'color': colors['accent_color']
        }
        self.alerts.append(alert)
        
        # Add celebration flash
        self.flash_effect = {
            'active': True,
            'start_time': time.time(),
            'duration': 2.0,
            'color': colors['accent_color']
        }
        
        # Add celebration particles across screen
        for _ in range(5):
            x = np.random.randint(100, self.width - 100)
            y = np.random.randint(100, self.height - 100)
            effect = ParticleEffect(x, y, colors['accent_color'], 15)
            self.particle_effects.append(effect)
    
    def add_stalemate_alert(self):
        """Add stalemate alert."""
        colors = self.theme.get_colors()
        
        alert = {
            'type': 'stalemate',
            'message': 'STALEMATE - DRAW!',
            'start_time': time.time(),
            'duration': 3.0,
            'color': colors['hover_color']
        }
        self.alerts.append(alert)
    
    def add_move_notification(self, move_notation):
        """Add move notification."""
        colors = self.theme.get_colors()
        
        alert = {
            'type': 'move',
            'message': f'Move: {move_notation}',
            'start_time': time.time(),
            'duration': 2.0,
            'color': colors['text_color']
        }
        self.alerts.append(alert)
    
    def update(self):
        """Update alerts and effects."""
        current_time = time.time()
        
        # Update alerts
        self.alerts = [alert for alert in self.alerts 
                      if current_time - alert['start_time'] < alert['duration']]
        
        # Update flash effect
        if self.flash_effect['active']:
            if current_time - self.flash_effect['start_time'] > self.flash_effect['duration']:
                self.flash_effect['active'] = False
        
        # Update particle effects
        for effect in self.particle_effects:
            effect.update()
        self.particle_effects = [effect for effect in self.particle_effects if effect.active]
    
    def draw_flash_effect(self, img):
        """Draw screen flash effect."""
        if not self.flash_effect['active']:
            return img
        
        current_time = time.time()
        elapsed = current_time - self.flash_effect['start_time']
        
        if elapsed < self.flash_effect['duration']:
            # Calculate flash intensity
            intensity = 1.0 - (elapsed / self.flash_effect['duration'])
            intensity = max(0, intensity)
            
            # Create flash overlay
            overlay = img.copy()
            color = tuple(int(c * intensity * 0.3) for c in self.flash_effect['color'])
            cv2.rectangle(overlay, (0, 0), (self.width, self.height), color, -1)
            
            # Blend with original
            img = cv2.addWeighted(img, 1.0, overlay, 0.5, 0)
        
        return img
    
    def draw_alerts(self, img):
        """Draw alert messages."""
        current_time = time.time()
        
        for alert in self.alerts:
            elapsed = current_time - alert['start_time']
            alpha = 1.0 - (elapsed / alert['duration'])
            
            if alpha > 0:
                # Calculate position and size
                if alert['type'] == 'checkmate':
                    font_scale = 1.5
                    thickness = 3
                    y_offset = 100
                elif alert['type'] == 'check':
                    font_scale = 1.2
                    thickness = 2
                    y_offset = 150
                else:
                    font_scale = 0.8
                    thickness = 2
                    y_offset = 200
                
                # Add pulsing effect for important alerts
                if alert['type'] in ['check', 'checkmate']:
                    pulse = abs(np.sin(elapsed * 8))
                    font_scale *= (1.0 + pulse * 0.1)
                
                # Calculate text position
                text_size = cv2.getTextSize(alert['message'], self.font, font_scale, thickness)[0]
                text_x = (self.width - text_size[0]) // 2
                text_y = y_offset
                
                # Draw text with shadow
                shadow_color = (0, 0, 0)
                text_color = tuple(int(c * alpha) for c in alert['color'])
                
                # Shadow
                cv2.putText(img, alert['message'], 
                          (text_x + 2, text_y + 2), 
                          self.font, font_scale, shadow_color, thickness + 1, cv2.LINE_AA)
                
                # Main text
                cv2.putText(img, alert['message'], 
                          (text_x, text_y), 
                          self.font, font_scale, text_color, thickness, cv2.LINE_AA)
        
        return img
    
    def draw_king_highlight(self, img, board):
        """Draw highlight on king in check."""
        for alert in self.alerts:
            if alert['type'] == 'check' and 'king_square' in alert:
                king_square = alert['king_square']
                
                # Find king position on board
                # This would need the chessboard_ui reference for proper coordinates
                # For now, we'll add a pulsing border effect
                
                elapsed = time.time() - alert['start_time']
                pulse = abs(np.sin(elapsed * 6))
                
                colors = self.theme.get_colors()
                border_color = tuple(int(c * (0.5 + pulse * 0.5)) for c in colors['check_color'])
                
                # Draw pulsing border around entire board area
                board_margin = 20
                cv2.rectangle(img, (board_margin, board_margin), 
                            (self.width - board_margin, self.height - board_margin), 
                            border_color, 5)
        
        return img
    
    def draw(self, img, board=None):
        """Draw all alert effects."""
        # Update effects
        self.update()
        
        # Draw effects in order
        img = self.draw_flash_effect(img)
        img = self.draw_alerts(img)
        
        if board:
            img = self.draw_king_highlight(img, board)
        
        # Draw particle effects
        for effect in self.particle_effects:
            effect.draw(img)
        
        return img
