"""
Captured pieces display system.
"""
import cv2
import numpy as np
import chess
from .theme import UITheme

class CapturedPiecesDisplay:
    def __init__(self, width=960, height=720, chessboard_ui=None):
        self.width = width
        self.height = height
        self.chessboard_ui = chessboard_ui
        self.theme = UITheme()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.captured_by_white = []
        self.captured_by_black = []
        self.piece_symbols = {
            chess.PAWN: 'P',
            chess.KNIGHT: 'N',
            chess.BISHOP: 'B',
            chess.ROOK: 'R',
            chess.QUEEN: 'Q',
            chess.KING: 'K'
        }
        
    def update_captured_pieces(self, board):
        """Update captured pieces lists based on board state."""
        self.captured_by_white.clear()
        self.captured_by_black.clear()
        
        # Count pieces on board
        white_pieces = {piece_type: 0 for piece_type in self.piece_symbols}
        black_pieces = {piece_type: 0 for piece_type in self.piece_symbols}
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    white_pieces[piece.piece_type] += 1
                else:
                    black_pieces[piece.piece_type] += 1
        
        # Calculate captured pieces (starting pieces - current pieces)
        starting_pieces = {
            chess.PAWN: 8,
            chess.KNIGHT: 2,
            chess.BISHOP: 2,
            chess.ROOK: 2,
            chess.QUEEN: 1,
            chess.KING: 1
        }
        
        for piece_type in self.piece_symbols:
            white_captured = starting_pieces[piece_type] - white_pieces[piece_type]
            black_captured = starting_pieces[piece_type] - black_pieces[piece_type]
            
            # Add captured pieces to lists
            for _ in range(white_captured):
                self.captured_by_black.append(piece_type)
            for _ in range(black_captured):
                self.captured_by_white.append(piece_type)
    
    def get_piece_value(self, piece_type):
        """Get piece value for material count display."""
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values.get(piece_type, 0)
    
    def calculate_material_advantage(self):
        """Calculate material advantage for white."""
        white_value = sum(self.get_piece_value(piece) for piece in self.captured_by_black)
        black_value = sum(self.get_piece_value(piece) for piece in self.captured_by_white)
        return white_value - black_value
    
    def draw_captured_pieces_panel(self, img, side='white'):
        """Draw captured pieces panel for one side."""
        colors = self.theme.get_colors()
        
        if side == 'white':
            captured_pieces = self.captured_by_white
            panel_x = 20
            panel_y = self.height - 120
            title = "WHITE CAPTURED"
        else:
            captured_pieces = self.captured_by_black
            panel_x = self.width - 220
            panel_y = self.height - 120
            title = "BLACK CAPTURED"
        
        if not captured_pieces:
            return img
        
        # Draw panel
        panel_w, panel_h = 200, 100
        img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h, title)
        
        # Calculate material value
        material_value = sum(self.get_piece_value(piece) for piece in captured_pieces)
        
        # Draw material value
        value_text = f"+{material_value}"
        cv2.putText(img, value_text, (panel_x + panel_w - 40, panel_y + 30), 
                   self.font, 0.6, colors['accent_color'], 2, cv2.LINE_AA)
        
        # Draw captured pieces
        if self.chessboard_ui and self.chessboard_ui.piece_images:
            x_offset = panel_x + 10
            y_offset = panel_y + 60
            
            for i, piece_type in enumerate(captured_pieces[:8]):  # Show max 8 pieces
                piece_color = chess.BLACK if side == 'white' else chess.WHITE
                piece_img = self.chessboard_ui.piece_images.get((piece_type, piece_color))
                
                if piece_img is not None:
                    # Draw small piece
                    piece_size = 20
                    piece_resized = cv2.resize(piece_img, (piece_size, piece_size))
                    
                    x_pos = x_offset + (i * 22)
                    y_pos = y_offset
                    
                    if piece_resized.shape[2] == 4:
                        alpha = piece_resized[:, :, 3] / 255.0
                        for c in range(3):
                            img[y_pos:y_pos+piece_size, x_pos:x_pos+piece_size, c] = (
                                alpha * piece_resized[:, :, c] + 
                                (1 - alpha) * img[y_pos:y_pos+piece_size, x_pos:x_pos+piece_size, c]
                            )
                    else:
                        img[y_pos:y_pos+piece_size, x_pos:x_pos+piece_size] = piece_resized[:, :, :3]
            
            # Show count if more than 8 pieces
            if len(captured_pieces) > 8:
                more_text = f"+{len(captured_pieces) - 8}"
                cv2.putText(img, more_text, (x_offset + 8 * 22, y_offset + 15), 
                           self.font, 0.4, colors['text_color'], 1, cv2.LINE_AA)
        else:
            # Fallback to text display
            piece_counts = {}
            for piece_type in captured_pieces:
                symbol = self.piece_symbols[piece_type]
                piece_counts[symbol] = piece_counts.get(symbol, 0) + 1
            
            text = " ".join([f"{symbol}x{count}" for symbol, count in piece_counts.items()])
            cv2.putText(img, text, (panel_x + 10, panel_y + 60), 
                       self.font, 0.5, colors['text_color'], 1, cv2.LINE_AA)
        
        return img
    
    def draw_material_advantage(self, img):
        """Draw material advantage indicator."""
        colors = self.theme.get_colors()
        
        advantage = self.calculate_material_advantage()
        
        if advantage == 0:
            return img
        
        # Panel dimensions
        panel_w, panel_h = 150, 40
        panel_x = (self.width - panel_w) // 2
        panel_y = self.height - 60
        
        # Draw panel
        img = self.theme.draw_panel(img, panel_x, panel_y, panel_w, panel_h)
        
        # Determine advantage color and text
        if advantage > 0:
            advantage_text = f"White +{advantage}"
            advantage_color = colors['legal_color']
        else:
            advantage_text = f"Black +{abs(advantage)}"
            advantage_color = colors['illegal_color']
        
        # Draw text
        text_size = cv2.getTextSize(advantage_text, self.font, 0.6, 2)[0]
        text_x = panel_x + (panel_w - text_size[0]) // 2
        text_y = panel_y + 25
        
        cv2.putText(img, advantage_text, (text_x, text_y), 
                   self.font, 0.6, advantage_color, 2, cv2.LINE_AA)
        
        return img
    
    def draw(self, img):
        """Draw all captured pieces displays."""
        # Draw captured pieces panels
        img = self.draw_captured_pieces_panel(img, 'white')
        img = self.draw_captured_pieces_panel(img, 'black')
        
        # Draw material advantage
        img = self.draw_material_advantage(img)
        
        return img
