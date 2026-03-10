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
        # Use standard English letters instead of Unicode symbols for better compatibility
        self.piece_symbols = {
            chess.PAWN: 'P', chess.KNIGHT: 'N', chess.BISHOP: 'B',
            chess.ROOK: 'R', chess.QUEEN: 'Q', chess.KING: 'K'
        }
        
        # Enhanced color schemes for pieces - HIGH CONTRAST for visibility
        self.white_piece_colors = {
            'classic_wood': (255, 255, 255),      # Pure White
            'pure_white': (255, 255, 255),         # Pure White
            'high_contrast': (255, 255, 255),      # Pure White
            'ocean_blue': (255, 255, 255),         # Pure White
            'forest_green': (255, 255, 255),       # Pure White
            'royal_purple': (255, 255, 255)        # Pure White
        }
        
        self.black_piece_colors = {
            'classic_wood': (0, 0, 0),             # Pure Black
            'pure_white': (0, 0, 0),               # Pure Black
            'high_contrast': (0, 0, 0),            # Pure Black
            'ocean_blue': (0, 0, 0),               # Pure Black
            'forest_green': (0, 0, 0),             # Pure Black
            'royal_purple': (0, 0, 0)              # Pure Black
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
            # Add white border for extra visibility
            border_color = (0, 0, 0)
        else:
            piece_color = self.black_piece_colors.get(theme_name, (0, 0, 0))
            # Add black border for extra visibility
            border_color = (255, 255, 255)
        
        # Calculate font settings for maximum visibility
        font_scale = self.calculate_font_scale(size)
        thickness = self.calculate_thickness(size)
        
        # Draw shadow for depth
        shadow_offset = 4
        shadow_x = x + shadow_offset
        shadow_y = y + shadow_offset
        
        # Draw shadow text
        cv2.putText(img, symbol, (shadow_x, shadow_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, 
                   (0, 0, 0), thickness + 2, cv2.LINE_AA)
        
        # Draw border/outline for extra visibility
        cv2.putText(img, symbol, (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, 
                   border_color, thickness + 3, cv2.LINE_AA)
        
        # Draw main piece
        cv2.putText(img, symbol, (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, 
                   piece_color, thickness, cv2.LINE_AA)
        
        # Add inner highlight for depth
        if piece.color == chess.WHITE:
            highlight_color = (200, 200, 200)
        else:
            highlight_color = (100, 100, 100)
            
        cv2.putText(img, symbol, (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, 
                   highlight_color, 1, cv2.LINE_AA)
        
        return img
    
    def calculate_font_scale(self, size):
        """Calculate appropriate font scale based on piece size - MASSIVE for maximum visibility."""
        # Make pieces HUGE for better visibility
        base_size = 20  # Even smaller base for much larger scaling
        return max(2.5, min(5.0, size / base_size))  # MASSIVE scale
    
    def calculate_thickness(self, size):
        """Calculate appropriate line thickness based on piece size - VERY THICK for visibility."""
        # Make lines very thick for better visibility
        base_size = 20
        return max(5, min(12, int(size / base_size * 5)))  # VERY THICK
    
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
