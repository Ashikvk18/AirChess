"""
Real chess piece renderer that draws traditional chess piece shapes.
"""
import cv2
import numpy as np
import chess
from .theme import UITheme

class RealPieceRenderer:
    def __init__(self, chessboard_ui):
        self.chessboard_ui = chessboard_ui
        self.theme = UITheme()
        
        # Piece colors
        self.white_piece_colors = {
            'classic_wood': (255, 255, 255),
            'pure_white': (255, 255, 255),
            'high_contrast': (255, 255, 255),
            'ocean_blue': (255, 255, 255),
            'forest_green': (255, 255, 255),
            'royal_purple': (255, 255, 255)
        }
        
        self.black_piece_colors = {
            'classic_wood': (0, 0, 0),
            'pure_white': (0, 0, 0),
            'high_contrast': (0, 0, 0),
            'ocean_blue': (0, 0, 0),
            'forest_green': (0, 0, 0),
            'royal_purple': (0, 0, 0)
        }
    
    def draw_real_piece(self, img, piece, x, y, size=None):
        """Draw a real chess piece shape."""
        if size is None:
            size = self.chessboard_ui.square_size
            
        theme_name = self.theme.current_theme.value
        
        # Get piece color
        if piece.color == chess.WHITE:
            piece_color = self.white_piece_colors.get(theme_name, (255, 255, 255))
            border_color = (0, 0, 0)
        else:
            piece_color = self.black_piece_colors.get(theme_name, (0, 0, 0))
            border_color = (255, 255, 255)
        
        # Draw shadow
        shadow_offset = 3
        self._draw_piece_shadow(img, x + shadow_offset, y + shadow_offset, size, piece.piece_type)
        
        # Draw the actual piece shape
        if piece.piece_type == chess.PAWN:
            self._draw_pawn(img, x, y, size, piece_color, border_color)
        elif piece.piece_type == chess.KNIGHT:
            self._draw_knight(img, x, y, size, piece_color, border_color)
        elif piece.piece_type == chess.BISHOP:
            self._draw_bishop(img, x, y, size, piece_color, border_color)
        elif piece.piece_type == chess.ROOK:
            self._draw_rook(img, x, y, size, piece_color, border_color)
        elif piece.piece_type == chess.QUEEN:
            self._draw_queen(img, x, y, size, piece_color, border_color)
        elif piece.piece_type == chess.KING:
            self._draw_king(img, x, y, size, piece_color, border_color)
        
        return img
    
    def _draw_piece_shadow(self, img, x, y, size, piece_type):
        """Draw shadow for the piece."""
        shadow_color = (50, 50, 50)
        shadow_size = size * 0.8
        
        # Create simple shadow shape
        if piece_type == chess.PAWN:
            cv2.circle(img, (x, y), int(shadow_size * 0.3), shadow_color, -1)
        elif piece_type in [chess.BISHOP, chess.QUEEN, chess.KING]:
            # Tall pieces shadow
            points = np.array([
                (x - shadow_size * 0.3, y + shadow_size * 0.4),
                (x + shadow_size * 0.3, y + shadow_size * 0.4),
                (x + shadow_size * 0.2, y - shadow_size * 0.3),
                (x - shadow_size * 0.2, y - shadow_size * 0.3)
            ], np.int32)
            cv2.fillPoly(img, [points], shadow_color)
        else:
            # Other pieces shadow
            cv2.rectangle(img, (int(x - shadow_size * 0.3), int(y - shadow_size * 0.4)), 
                        (int(x + shadow_size * 0.3), int(y + shadow_size * 0.4)), shadow_color, -1)
    
    def _draw_pawn(self, img, x, y, size, color, border_color):
        """Draw a pawn shape."""
        s = size * 0.8
        
        # Base
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), border_color, 2)
        
        # Body (narrowing)
        points = np.array([
            (x - s * 0.25, y + s * 0.2),
            (x + s * 0.25, y + s * 0.2),
            (x + s * 0.15, y - s * 0.1),
            (x - s * 0.15, y - s * 0.1)
        ], np.int32)
        cv2.fillPoly(img, [points], color)
        cv2.polylines(img, [points], True, border_color, 2)
        
        # Head (round)
        cv2.circle(img, (int(x), int(y - s * 0.1)), int(s * 0.2), color, -1)
        cv2.circle(img, (int(x), int(y - s * 0.1)), int(s * 0.2), border_color, 2)
    
    def _draw_knight(self, img, x, y, size, color, border_color):
        """Draw a knight shape."""
        s = size * 0.8
        
        # Base
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), border_color, 2)
        
        # Knight head (L-shape)
        points = np.array([
            (x - s * 0.25, y + s * 0.2),
            (x + s * 0.1, y + s * 0.2),
            (x + s * 0.1, y - s * 0.1),
            (x + s * 0.25, y - s * 0.1),
            (x + s * 0.25, y - s * 0.3),
            (x + s * 0.05, y - s * 0.4),
            (x - s * 0.15, y - s * 0.3),
            (x - s * 0.25, y - s * 0.1)
        ], np.int32)
        cv2.fillPoly(img, [points], color)
        cv2.polylines(img, [points], True, border_color, 2)
        
        # Ear
        cv2.circle(img, (int(x + s * 0.15), int(y - s * 0.4)), int(s * 0.08), color, -1)
        cv2.circle(img, (int(x + s * 0.15), int(y - s * 0.4)), int(s * 0.08), border_color, 2)
    
    def _draw_bishop(self, img, x, y, size, color, border_color):
        """Draw a bishop shape."""
        s = size * 0.8
        
        # Base
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), border_color, 2)
        
        # Body (triangle)
        points = np.array([
            (x - s * 0.25, y + s * 0.2),
            (x + s * 0.25, y + s * 0.2),
            (x, y - s * 0.2)
        ], np.int32)
        cv2.fillPoly(img, [points], color)
        cv2.polylines(img, [points], True, border_color, 2)
        
        # Hat (round top)
        cv2.circle(img, (int(x), int(y - s * 0.25)), int(s * 0.15), color, -1)
        cv2.circle(img, (int(x), int(y - s * 0.25)), int(s * 0.15), border_color, 2)
        
        # Cross on top
        cv2.line(img, (int(x), int(y - s * 0.35)), (int(x), int(y - s * 0.15)), border_color, 3)
        cv2.line(img, (int(x - s * 0.08), int(y - s * 0.25)), (int(x + s * 0.08), int(y - s * 0.25)), border_color, 3)
    
    def _draw_rook(self, img, x, y, size, color, border_color):
        """Draw a rook shape."""
        s = size * 0.8
        
        # Base
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), border_color, 2)
        
        # Tower body
        cv2.rectangle(img, (int(x - s * 0.2), int(y - s * 0.1)), 
                     (int(x + s * 0.2), int(y + s * 0.2)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.2), int(y - s * 0.1)), 
                     (int(x + s * 0.2), int(y + s * 0.2)), border_color, 2)
        
        # Battlements (top)
        tooth_width = s * 0.15
        tooth_height = s * 0.15
        
        # Left tooth
        cv2.rectangle(img, (int(x - s * 0.2), int(y - s * 0.1 - tooth_height)), 
                     (int(x - s * 0.2 + tooth_width), int(y - s * 0.1)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.2), int(y - s * 0.1 - tooth_height)), 
                     (int(x - s * 0.2 + tooth_width), int(y - s * 0.1)), border_color, 2)
        
        # Middle left tooth
        cv2.rectangle(img, (int(x - tooth_width * 0.5), int(y - s * 0.1 - tooth_height)), 
                     (int(x + tooth_width * 0.5), int(y - s * 0.1)), color, -1)
        cv2.rectangle(img, (int(x - tooth_width * 0.5), int(y - s * 0.1 - tooth_height)), 
                     (int(x + tooth_width * 0.5), int(y - s * 0.1)), border_color, 2)
        
        # Middle right tooth
        cv2.rectangle(img, (int(x + tooth_width * 0.5), int(y - s * 0.1 - tooth_height)), 
                     (int(x + s * 0.2 - tooth_width), int(y - s * 0.1)), color, -1)
        cv2.rectangle(img, (int(x + tooth_width * 0.5), int(y - s * 0.1 - tooth_height)), 
                     (int(x + s * 0.2 - tooth_width), int(y - s * 0.1)), border_color, 2)
        
        # Right tooth
        cv2.rectangle(img, (int(x + s * 0.2 - tooth_width), int(y - s * 0.1 - tooth_height)), 
                     (int(x + s * 0.2), int(y - s * 0.1)), color, -1)
        cv2.rectangle(img, (int(x + s * 0.2 - tooth_width), int(y - s * 0.1 - tooth_height)), 
                     (int(x + s * 0.2), int(y - s * 0.1)), border_color, 2)
    
    def _draw_queen(self, img, x, y, size, color, border_color):
        """Draw a queen shape."""
        s = size * 0.8
        
        # Base
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), border_color, 2)
        
        # Body (cone shape)
        points = np.array([
            (x - s * 0.25, y + s * 0.2),
            (x + s * 0.25, y + s * 0.2),
            (x + s * 0.15, y - s * 0.1),
            (x - s * 0.15, y - s * 0.1)
        ], np.int32)
        cv2.fillPoly(img, [points], color)
        cv2.polylines(img, [points], True, border_color, 2)
        
        # Crown points (5 points)
        crown_points = 5
        for i in range(crown_points):
            angle = (i * 2 * 3.14159) / crown_points - 3.14159 / 2
            px = x + s * 0.3 * np.cos(angle)
            py = y - s * 0.1 + s * 0.2 * np.sin(angle)
            
            # Draw crown point
            tip_points = np.array([
                (px - s * 0.08, py + s * 0.05),
                (px + s * 0.08, py + s * 0.05),
                (px, py - s * 0.15)
            ], np.int32)
            cv2.fillPoly(img, [tip_points], color)
            cv2.polylines(img, [tip_points], True, border_color, 2)
        
        # Center orb
        cv2.circle(img, (int(x), int(y - s * 0.1)), int(s * 0.08), color, -1)
        cv2.circle(img, (int(x), int(y - s * 0.1)), int(s * 0.08), border_color, 2)
    
    def _draw_king(self, img, x, y, size, color, border_color):
        """Draw a king shape."""
        s = size * 0.8
        
        # Base
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.3), int(y + s * 0.2)), 
                     (int(x + s * 0.3), int(y + s * 0.4)), border_color, 2)
        
        # Body (wide)
        cv2.rectangle(img, (int(x - s * 0.25), int(y - s * 0.1)), 
                     (int(x + s * 0.25), int(y + s * 0.2)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.25), int(y - s * 0.1)), 
                     (int(x + s * 0.25), int(y + s * 0.2)), border_color, 2)
        
        # Cross on top
        cross_width = s * 0.4
        cross_height = s * 0.3
        
        # Vertical part of cross
        cv2.rectangle(img, (int(x - s * 0.05), int(y - s * 0.1 - cross_height)), 
                     (int(x + s * 0.05), int(y - s * 0.1)), color, -1)
        cv2.rectangle(img, (int(x - s * 0.05), int(y - s * 0.1 - cross_height)), 
                     (int(x + s * 0.05), int(y - s * 0.1)), border_color, 2)
        
        # Horizontal part of cross
        cv2.rectangle(img, (int(x - cross_width * 0.5), int(y - s * 0.1 - cross_height * 0.6)), 
                     (int(x + cross_width * 0.5), int(y - s * 0.1 - cross_height * 0.4)), color, -1)
        cv2.rectangle(img, (int(x - cross_width * 0.5), int(y - s * 0.1 - cross_height * 0.6)), 
                     (int(x + cross_width * 0.5), int(y - s * 0.1 - cross_height * 0.4)), border_color, 2)
    
    def get_piece_color(self, piece):
        """Get the color for a piece based on current theme."""
        theme_name = self.theme.current_theme.value
        
        if piece.color == chess.WHITE:
            return self.white_piece_colors.get(theme_name, (255, 255, 255))
        else:
            return self.black_piece_colors.get(theme_name, (0, 0, 0))
