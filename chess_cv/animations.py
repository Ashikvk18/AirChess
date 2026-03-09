"""
Animation system for smooth piece movements and visual effects.
"""
import cv2
import numpy as np
import chess
import time
from collections import deque

class PieceAnimation:
    def __init__(self, start_pos, end_pos, piece, duration=0.3):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece = piece
        self.duration = duration
        self.start_time = time.time()
        self.active = True
        
    def get_current_position(self):
        """Get interpolated position based on elapsed time."""
        if not self.active:
            return self.end_pos
            
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            self.active = False
            return self.end_pos
            
        # Easing function (ease-out cubic)
        t = elapsed / self.duration
        eased = 1 - (1 - t) ** 3
        
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * eased
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * eased
        
        return (int(x), int(y))

class ParticleEffect:
    def __init__(self, x, y, color, particle_count=10):
        self.particles = []
        for _ in range(particle_count):
            angle = np.random.uniform(0, 2 * np.pi)
            speed = np.random.uniform(2, 8)
            self.particles.append({
                'x': float(x),
                'y': float(y),
                'vx': np.cos(angle) * speed,
                'vy': np.sin(angle) * speed,
                'life': 1.0,
                'color': color
            })
        self.active = True
        
    def update(self, dt=0.016):  # ~60 FPS
        """Update particle positions and life."""
        any_alive = False
        for particle in self.particles:
            if particle['life'] > 0:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.3  # Gravity
                particle['life'] -= dt * 2  # Fade out
                any_alive = True
        
        self.active = any_alive
        
    def draw(self, img):
        """Draw particles on image."""
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = particle['life']
                color = tuple(int(c * alpha) for c in particle['color'])
                cv2.circle(img, (int(particle['x']), int(particle['y'])), 
                          int(3 * alpha), color, -1)

class AnimationSystem:
    def __init__(self, chessboard_ui):
        self.chessboard_ui = chessboard_ui
        self.animations = []
        self.particle_effects = []
        self.move_history = deque(maxlen=10)
        self.enabled = True
        
    def toggle_animations(self):
        """Toggle animations on/off."""
        self.enabled = not self.enabled
        if not self.enabled:
            self.animations.clear()
            self.particle_effects.clear()
        return self.enabled
    
    def add_move_animation(self, move, piece):
        """Add animation for a piece move."""
        if not self.enabled:
            return
            
        start_square = move.from_square
        end_square = move.to_square
        
        start_pos = self.chessboard_ui.get_square_center(start_square)
        end_pos = self.chessboard_ui.get_square_center(end_square)
        
        animation = PieceAnimation(start_pos, end_pos, piece)
        self.animations.append(animation)
        
        # Add capture effect
        if self.chessboard_ui.piece_images:
            captured_piece = None  # Would need board reference
            if captured_piece:
                colors = self.chessboard_ui.theme.get_colors()
                effect = ParticleEffect(end_pos[0], end_pos[1], colors['check_color'], 15)
                self.particle_effects.append(effect)
    
    def add_selection_effect(self, square):
        """Add particle effect for piece selection."""
        if not self.enabled:
            return
            
        x, y = self.chessboard_ui.get_square_center(square)
        colors = self.chessboard_ui.theme.get_colors()
        effect = ParticleEffect(x, y, colors['selected_color'], 8)
        self.particle_effects.append(effect)
    
    def add_invalid_move_effect(self, square):
        """Add effect for invalid move attempt."""
        if not self.enabled:
            return
            
        x, y = self.chessboard_ui.get_square_center(square)
        colors = self.chessboard_ui.theme.get_colors()
        effect = ParticleEffect(x, y, colors['illegal_color'], 12)
        self.particle_effects.append(effect)
    
    def update(self):
        """Update all animations and effects."""
        # Update animations
        self.animations = [anim for anim in self.animations if anim.active]
        
        # Update particle effects
        for effect in self.particle_effects:
            effect.update()
        self.particle_effects = [effect for effect in self.particle_effects if effect.active]
    
    def draw_animating_pieces(self, img):
        """Draw pieces that are currently animating."""
        if not self.enabled:
            return img
            
        for animation in self.animations:
            if animation.active:
                current_pos = animation.get_current_position()
                piece_img = self.chessboard_ui.piece_images.get(
                    (animation.piece.piece_type, animation.piece.color)
                )
                
                if piece_img is not None:
                    sz = self.chessboard_ui.square_size
                    px0 = current_pos[0] - sz // 2
                    py0 = current_pos[1] - sz // 2
                    px1 = px0 + sz
                    py1 = py0 + sz
                    
                    # Add motion blur effect
                    if animation.active:
                        blur_img = img.copy()
                        piece_resized = cv2.resize(piece_img, (sz, sz))
                        if piece_resized.shape[2] == 4:
                            alpha = piece_resized[:, :, 3] / 255.0
                            for c in range(3):
                                blur_img[py0:py1, px0:px1, c] = (
                                    alpha * piece_resized[:, :, c] + 
                                    (1 - alpha) * blur_img[py0:py1, px0:px1, c]
                                )
                        
                        # Apply motion blur
                        kernel_size = 5
                        kernel = np.zeros((kernel_size, kernel_size))
                        kernel[int(kernel_size/2), :] = 1
                        kernel = kernel / kernel_size
                        blur_img[py0:py1, px0:px1] = cv2.filter2D(
                            blur_img[py0:py1, px0:px1], -1, kernel
                        )
                        img = cv2.addWeighted(img, 0.7, blur_img, 0.3, 0)
                    
                    # Draw actual piece
                    piece_resized = cv2.resize(piece_img, (sz, sz))
                    if piece_resized.shape[2] == 4:
                        alpha = piece_resized[:, :, 3] / 255.0
                        for c in range(3):
                            img[py0:py1, px0:px1, c] = (
                                alpha * piece_resized[:, :, c] + 
                                (1 - alpha) * img[py0:py1, px0:px1, c]
                            )
                    else:
                        img[py0:py1, px0:px1] = piece_resized[:, :, :3]
        
        return img
    
    def draw_particle_effects(self, img):
        """Draw all particle effects."""
        if not self.enabled:
            return img
            
        for effect in self.particle_effects:
            effect.draw(img)
        
        return img
