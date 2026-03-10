"""
Enhanced piece rendering system with vibrant colors and improved visibility.
"""
import cv2
import numpy as np
import chess
from .theme import UITheme

class PieceRenderer:
    def __init__(self, chessboard_ui):
        self.chessboard_ui = chessboard_ui
        self.theme = UITheme()
        self.piece_symbols = {
            chess.PAWN: '♟', chess.KNIGHT: '♞', chess.BISHOP: '♝',
            chess.ROOK: '♜', chess.QUEEN: '♛', chess.KING: '♚'
        }
        
        # Enhanced color schemes for pieces
        self.white_piece_colors = {
            'neon_cyber': (0, 255, 255),      # Cyan
            'sunset_vibrant': (255, 255, 255), # White
            'ocean_breeze': (255, 255, 255),  # White
            'forest_emerald': (255, 255, 255), # White
            'galaxy_purple': (255, 255, 255), # White
            'fire_opal': (255, 255, 255)      # White
        }
        
        self.black_piece_colors = {
            'neon_cyber': (255, 20, 147),     # Hot Pink
            'sunset_vibrant': (139, 0, 0),    # Dark Red
            'ocean_breeze': (0, 0, 139),      # Dark Blue
            'forest_emerald': (0, 100, 0),    # Dark Green
            'galaxy_purple': (75, 0, 130),    # Indigo
            'fire_opal': (139, 69, 19)        # Saddle Brown
        }
        
        self.piece_shadow_color = (0, 0, 0)
        self.piece_glow_color = (255, 255, 255)
        
    def draw_enhanced_piece(self, img, piece, x, y, size=None):
        """Draw an enhanced chess piece with vibrant colors and effects."""
        if size is None:
            size = self.chessboard_ui.square_size
            
        colors = self.theme.get_colors()
        theme_name = self.theme.current_theme.value
        
        # Get piece symbol
        symbol = self.piece_symbols.get(piece.piece_type, '?')
        
        # Determine piece color
        if piece.color == chess.WHITE:
            piece_color = self.white_piece_colors.get(theme_name, (255, 255, 255))
        else:
            piece_color = self.black_piece_colors.get(theme_name, (0, 0, 0))
        
        # Draw shadow for depth
        shadow_offset = 3
        shadow_x = x + shadow_offset
        shadow_y = y + shadow_offset
        
        # Create shadow with transparency
        shadow_alpha = 0.6
        shadow_img = np.zeros_like(img)
        
        # Draw shadow text
        font_scale = self.calculate_font_scale(size)
        thickness = self.calculate_thickness(size)
        
        cv2.putText(shadow_img, symbol, (shadow_x, shadow_y), 
                   cv2.FONT_HERSHEY_COMPLEX, font_scale, 
                   self.piece_shadow_color, thickness * 2, cv2.LINE_AA)
        
        # Apply shadow with transparency
        img[y-size//2:y+size//2, x-size//2:x+size//2] = cv2.addWeighted(
            img[y-size//2:y+size//2, x-size//2:x+size//2], 
            1.0, shadow_img[y-size//2:y+size//2, x-size//2:x+size//2], 
            shadow_alpha, 0
        )
        
        # Draw glow effect for selected/hovered pieces
        glow_radius = size // 2 + 5
        glow_alpha = 0.3
        
        # Create glow effect
        for i in range(3):
            glow_size = glow_radius - i * 2
            if glow_size > 0:
                glow_color = tuple(int(c * glow_alpha * (1 - i/3)) for c in piece_color)
                cv2.circle(img, (x, y), glow_size, glow_color, 2)
        
        # Draw main piece with enhanced rendering
        # Draw outline first for better contrast
        outline_color = tuple(max(0, c - 50) for c in piece_color)
        cv2.putText(img, symbol, (x, y), 
                   cv2.FONT_HERSHEY_COMPLEX, font_scale, 
                   outline_color, thickness + 2, cv2.LINE_AA)
        
        # Draw main piece
        cv2.putText(img, symbol, (x, y), 
                   cv2.FONT_HERSHEY_COMPLEX, font_scale, 
                   piece_color, thickness, cv2.LINE_AA)
        
        # Add inner highlight for depth
        highlight_color = tuple(min(255, c + 100) for c in piece_color)
        cv2.putText(img, symbol, (x, y), 
                   cv2.FONT_HERSHEY_COMPLEX, font_scale, 
                   highlight_color, 1, cv2.LINE_AA)
        
        return img
    
    def calculate_font_scale(self, size):
        """Calculate appropriate font scale based on piece size."""
        # Scale font based on square size
        base_size = 50  # Base size for scaling
        return max(0.5, min(2.0, size / base_size))
    
    def calculate_thickness(self, size):
        """Calculate appropriate line thickness based on piece size."""
        # Scale thickness based on square size
        base_size = 50
        return max(1, min(4, int(size / base_size * 2)))
    
    def draw_piece_with_effects(self, img, piece, x, y, size=None, 
                               is_hovering=False, is_selected=False):
        """Draw piece with special effects for hover/selection."""
        img = self.draw_enhanced_piece(img, piece, x, y, size)
        
        if is_hovering or is_selected:
            colors = self.theme.get_colors()
            
            # Add pulsing glow effect
            import time
            pulse = abs(np.sin(time.time() * 3))
            
            if is_selected:
                glow_color = colors['selected_color']
                glow_intensity = 0.5 + pulse * 0.3
            else:
                glow_color = colors['hover_color']
                glow_intensity = 0.3 + pulse * 0.2
            
            # Draw pulsing glow
            glow_radius = int(self.chessboard_ui.square_size * 0.6)
            for i in range(5):
                alpha = glow_intensity * (1 - i/5)
                current_radius = glow_radius + i * 3
                glow_color_alpha = tuple(int(c * alpha) for c in glow_color)
                cv2.circle(img, (x, y), current_radius, glow_color_alpha, 2)
        
        return img
    
    def create_piece_image(self, piece, size):
        """Create a standalone piece image for animations."""
        # Create transparent image
        img = np.zeros((size * 2, size * 2, 4), dtype=np.uint8)
        img[:, :, 3] = 0  # Set alpha channel to transparent
        
        # Draw piece on transparent background
        self.draw_enhanced_piece(img, piece, size, size, size)
        
        return img
    
    def get_piece_color(self, piece):
        """Get the color for a piece based on current theme."""
        theme_name = self.theme.current_theme.value
        
        if piece.color == chess.WHITE:
            return self.white_piece_colors.get(theme_name, (255, 255, 255))
        else:
            return self.black_piece_colors.get(theme_name, (0, 0, 0))
