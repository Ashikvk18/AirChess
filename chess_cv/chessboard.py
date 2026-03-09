"""
Chessboard UI rendering and coordinate mapping with modern themes.
"""

import numpy as np
import cv2
import chess
import os
from .theme import UITheme, Theme

class ChessboardUI:
    def __init__(self, board_size=480, margin=40):
        self.board_size = board_size
        self.margin = margin
        self.square_size = (board_size - 2 * margin) // 8
        self.theme = UITheme()
        # Load piece images
        self.piece_images = self.load_piece_images()
        # Board positioning (centered on screen)
        self.board_x = 240  # Center position on 960px width
        self.board_y = 120  # Upper position for better visibility

    def set_theme(self, theme_name):
        """Set the visual theme."""
        self.theme.set_theme(theme_name)

    def load_piece_images(self):
        # Map (piece_type, color) to PNG path in assets/wood/
        base = os.path.join(os.path.dirname(__file__), "assets", "wood")
        mapping = {
            (chess.PAWN, True):   "wP.png",
            (chess.KNIGHT, True): "wN.png",
            (chess.BISHOP, True): "wB.png",
            (chess.ROOK, True):   "wR.png",
            (chess.QUEEN, True):  "wQ.png",
            (chess.KING, True):   "wK.png",
            (chess.PAWN, False):  "bP.png",
            (chess.KNIGHT, False):"bN.png",
            (chess.BISHOP, False):"bB.png",
            (chess.ROOK, False):  "bR.png",
            (chess.QUEEN, False): "bQ.png",
            (chess.KING, False):  "bK.png",
        }
        images = {}
        for key, fname in mapping.items():
            path = os.path.join(base, fname)
            if os.path.exists(path):
                img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    images[key] = img
        return images

    def get_square_from_pos(self, pos):
        if pos is None:
            return None
        x, y = pos
        # Board is always at top-left (margin, margin)
        bx = x - self.margin
        by = y - self.margin
        if bx < 0 or by < 0 or bx >= self.square_size * 8 or by >= self.square_size * 8:
            return None
        file = int(bx // self.square_size)
        rank = int(7 - (by // self.square_size))
        if 0 <= file < 8 and 0 <= rank < 8:
            return chess.square(file, rank)
        return None

    def get_square_center(self, square):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x = self.board_x + self.margin + file * self.square_size + self.square_size // 2
        y = self.board_y + self.margin + (7 - rank) * self.square_size + self.square_size // 2
        return (x, y)

    def draw(self, img, board, hover_square=None, selected_square=None, legal_moves=None):
        colors = self.theme.get_colors()
        
        # Draw board shadow for depth
        shadow_offset = 8
        board_rect = (
            self.board_x + self.margin - shadow_offset,
            self.board_y + self.margin - shadow_offset,
            self.board_x + self.margin + self.square_size * 8 + shadow_offset,
            self.board_y + self.margin + self.square_size * 8 + shadow_offset
        )
        cv2.rectangle(img, (board_rect[0], board_rect[1]), (board_rect[2], board_rect[3]), (0, 0, 0), -1)
        cv2.GaussianBlur(img[self.board_y + self.margin - shadow_offset:self.board_y + self.margin + self.square_size * 8 + shadow_offset,
                           self.board_x + self.margin - shadow_offset:self.board_x + self.margin + self.square_size * 8 + shadow_offset], 
                        (15, 15), 0, dst=img[self.board_y + self.margin - shadow_offset:self.board_y + self.margin + self.square_size * 8 + shadow_offset,
                           self.board_x + self.margin - shadow_offset:self.board_x + self.margin + self.square_size * 8 + shadow_offset])
        
        # Draw board with modern styling
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                color = colors['board_colors'][(file + rank) % 2]
                x0 = self.board_x + self.margin + file * self.square_size
                y0 = self.board_y + self.margin + rank * self.square_size
                x1 = x0 + self.square_size
                y1 = y0 + self.square_size
                
                # Draw square with gradient effect
                cv2.rectangle(img, (x0, y0), (x1, y1), color, -1)
                
                # Add subtle inner border for depth
                inner_color = tuple(int(c * 0.95) for c in color)
                cv2.rectangle(img, (x0+1, y0+1), (x1-1, y1-1), inner_color, 1)
                
                # Highlight legal moves with modern styling
                if legal_moves and square in legal_moves:
                    self.theme.draw_rounded_rectangle(
                        img, x0+3, y0+3, self.square_size-6, self.square_size-6, 
                        8, colors['legal_color'], 3
                    )
                
                # Highlight hover with glow effect
                if hover_square == square:
                    # Draw glow effect
                    for i in range(4):
                        glow_alpha = 0.4 - i * 0.1
                        glow_color = tuple(int(c * glow_alpha) for c in colors['hover_color'])
                        cv2.rectangle(img, (x0-i, y0-i), (x1+i, y1+i), glow_color, 2)
                
                # Highlight selected with gradient border
                if selected_square == square:
                    self.theme.draw_gradient_border(
                        img, x0, y0, self.square_size, self.square_size, 
                        5, colors['selected_color']
                    )
        
        # Draw pieces with shadow effects
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                img_piece = self.piece_images.get((piece.piece_type, piece.color))
                if img_piece is not None:
                    x, y = self.get_square_center(square)
                    sz = self.square_size
                    px0 = x - sz // 2
                    py0 = y - sz // 2
                    px1 = px0 + sz
                    py1 = py0 + sz
                    
                    # Draw shadow for piece
                    shadow_offset = 2
                    shadow_img = img.copy()
                    piece_img = cv2.resize(img_piece, (sz, sz))
                    if piece_img.shape[2] == 4:
                        alpha = piece_img[:, :, 3] / 255.0
                        shadow_alpha = alpha * 0.3
                        for c in range(3):
                            shadow_img[py0+shadow_offset:py1+shadow_offset, px0+shadow_offset:px1+shadow_offset, c] = (
                                shadow_alpha * piece_img[:, :, c] * 0.3 + 
                                (1 - shadow_alpha) * shadow_img[py0+shadow_offset:py1+shadow_offset, px0+shadow_offset:px1+shadow_offset, c]
                            )
                    
                    # Blend shadow back
                    img = cv2.addWeighted(img, 0.7, shadow_img, 0.3, 0)
                    
                    # Draw actual piece
                    piece_img = cv2.resize(img_piece, (sz, sz))
                    if piece_img.shape[2] == 4:
                        alpha = piece_img[:, :, 3] / 255.0
                        for c in range(3):
                            img[py0:py1, px0:px1, c] = (
                                alpha * piece_img[:, :, c] + (1 - alpha) * img[py0:py1, px0:px1, c]
                            )
                    else:
                        img[py0:py1, px0:px1] = piece_img[:, :, :3]
        return img

        # Removed duplicate/old draw() method that did not support legal_moves

    def draw_piece(self, img, piece, center):
        key = (piece.piece_type, piece.color)
        piece_img = self.piece_images.get(key)
        if piece_img is not None:
            # Resize to fit square
            size = int(self.square_size * 0.95)
            piece_img = cv2.resize(piece_img, (size, size), interpolation=cv2.INTER_AREA)
            x, y = center
            x -= size // 2
            y -= size // 2
            self.overlay_png(img, piece_img, x, y)
        else:
            # fallback: draw Unicode if PNG missing
            unicode_pieces = {
                (chess.PAWN, True):   "♙",
                (chess.KNIGHT, True): "♘",
                (chess.BISHOP, True): "♗",
                (chess.ROOK, True):   "♖",
                (chess.QUEEN, True):  "♕",
                (chess.KING, True):   "♔",
                (chess.PAWN, False):  "♟",
                (chess.KNIGHT, False):"♞",
                (chess.BISHOP, False):"♝",
                (chess.ROOK, False):  "♜",
                (chess.QUEEN, False): "♛",
                (chess.KING, False):  "♚",
            }
            symbol = unicode_pieces.get(key, "?")
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.6
            thickness = 2
            color = (20, 20, 20) if piece.color == chess.WHITE else (40, 40, 40)
            (w, h), _ = cv2.getTextSize(symbol, font, font_scale, thickness)
            pos = (center[0] - w // 2, center[1] + h // 2)
            cv2.putText(img, symbol, pos, font, font_scale, color, thickness, lineType=cv2.LINE_AA)

    def overlay_png(self, bg, fg, x, y):
        # Overlay PNG with alpha channel
        h, w = fg.shape[:2]
        if fg.shape[2] == 4:
            alpha = fg[:, :, 3] / 255.0
            for c in range(3):
                bg[y:y+h, x:x+w, c] = (1 - alpha) * bg[y:y+h, x:x+w, c] + alpha * fg[:, :, c]
        else:
            bg[y:y+h, x:x+w] = fg
