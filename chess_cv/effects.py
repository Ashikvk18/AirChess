"""
Enhanced visual effects system for smooth transitions and micro-interactions.
"""
import cv2
import numpy as np
import time
import math

class VisualEffects:
    def __init__(self):
        self.transitions = {}
        self.particles = []
        self.screen_shake = {'active': False, 'start_time': 0, 'duration': 0, 'intensity': 0}
        self.fade_effect = {'active': False, 'alpha': 0, 'duration': 0, 'start_time': 0}
        
    def add_transition(self, element_id, start_value, end_value, duration=0.5, easing='ease_out'):
        """Add a smooth transition for any UI element."""
        self.transitions[element_id] = {
            'start_value': start_value,
            'end_value': end_value,
            'duration': duration,
            'start_time': time.time(),
            'easing': easing,
            'active': True
        }
    
    def update_transitions(self):
        """Update all active transitions."""
        current_time = time.time()
        
        for element_id in list(self.transitions.keys()):
            transition = self.transitions[element_id]
            
            if not transition['active']:
                continue
                
            elapsed = current_time - transition['start_time']
            
            if elapsed >= transition['duration']:
                transition['active'] = False
                transition['current_value'] = transition['end_value']
            else:
                # Calculate progress with easing
                t = elapsed / transition['duration']
                
                if transition['easing'] == 'ease_out':
                    eased = 1 - (1 - t) ** 3
                elif transition['easing'] == 'ease_in':
                    eased = t ** 3
                elif transition['easing'] == 'ease_in_out':
                    if t < 0.5:
                        eased = 4 * t ** 3
                    else:
                        eased = 1 - 4 * (1 - t) ** 3
                else:
                    eased = t
                
                # Interpolate value
                if isinstance(transition['start_value'], tuple):
                    current_value = tuple(
                        transition['start_value'][i] + 
                        (transition['end_value'][i] - transition['start_value'][i]) * eased
                        for i in range(len(transition['start_value']))
                    )
                else:
                    current_value = transition['start_value'] + (transition['end_value'] - transition['start_value']) * eased
                
                transition['current_value'] = current_value
    
    def get_transition_value(self, element_id):
        """Get current value of a transition."""
        if element_id in self.transitions:
            transition = self.transitions[element_id]
            if transition['active']:
                return transition['current_value']
            else:
                return transition['end_value']
        return None
    
    def add_screen_shake(self, intensity=5, duration=0.3):
        """Add screen shake effect for dramatic moments."""
        self.screen_shake = {
            'active': True,
            'start_time': time.time(),
            'duration': duration,
            'intensity': intensity
        }
    
    def apply_screen_shake(self, img):
        """Apply screen shake to image."""
        if not self.screen_shake['active']:
            return img
        
        elapsed = time.time() - self.screen_shake['start_time']
        
        if elapsed >= self.screen_shake['duration']:
            self.screen_shake['active'] = False
            return img
        
        # Calculate shake intensity with decay
        decay = 1.0 - (elapsed / self.screen_shake['duration'])
        current_intensity = self.screen_shake['intensity'] * decay
        
        # Random offset
        offset_x = int(np.random.uniform(-current_intensity, current_intensity))
        offset_y = int(np.random.uniform(-current_intensity, current_intensity))
        
        # Apply shake by cropping and repositioning
        h, w = img.shape[:2]
        
        # Ensure we don't go out of bounds
        x_start = max(0, offset_x)
        y_start = max(0, offset_y)
        x_end = min(w, w + offset_x)
        y_end = min(h, h + offset_y)
        
        shaken_img = np.zeros_like(img)
        shaken_img[y_start:y_end, x_start:x_end] = img[y_start - offset_y:y_end - offset_y, x_start - offset_x:x_end - offset_x]
        
        return shaken_img
    
    def add_fade_effect(self, target_alpha=0.5, duration=1.0, color=(0, 0, 0)):
        """Add fade overlay effect."""
        self.fade_effect = {
            'active': True,
            'start_time': time.time(),
            'duration': duration,
            'target_alpha': target_alpha,
            'color': color,
            'current_alpha': 0
        }
    
    def apply_fade_effect(self, img):
        """Apply fade overlay to image."""
        if not self.fade_effect['active']:
            return img
        
        elapsed = time.time() - self.fade_effect['start_time']
        
        if elapsed >= self.fade_effect['duration']:
            self.fade_effect['active'] = False
            return img
        
        # Calculate fade progress
        progress = elapsed / self.fade_effect['duration']
        
        if progress < 0.5:
            # Fade in
            self.fade_effect['current_alpha'] = self.fade_effect['target_alpha'] * (progress * 2)
        else:
            # Fade out
            self.fade_effect['current_alpha'] = self.fade_effect['target_alpha'] * (2 - progress * 2)
        
        # Apply overlay
        overlay = img.copy()
        overlay[:] = self.fade_effect['color']
        
        img = cv2.addWeighted(img, 1.0, overlay, self.fade_effect['current_alpha'], 0)
        
        return img
    
    def add_pulse_effect(self, img, x, y, radius, color, duration=1.0):
        """Add expanding pulse effect at specified position."""
        elapsed = time.time() % duration
        progress = elapsed / duration
        
        # Calculate expanding radius
        current_radius = int(radius * progress)
        alpha = 1.0 - progress
        
        if alpha > 0:
            pulse_color = tuple(int(c * alpha) for c in color)
            cv2.circle(img, (x, y), current_radius, pulse_color, 3)
    
    def add_glow_effect(self, img, x, y, size, color, intensity=0.5):
        """Add soft glow effect around an area."""
        # Create glow overlay
        glow = np.zeros_like(img)
        
        # Draw multiple circles with decreasing alpha for glow effect
        for i in range(5):
            alpha = intensity * (1.0 - i / 5.0)
            glow_color = tuple(int(c * alpha) for c in color)
            glow_size = size + i * 3
            
            cv2.circle(glow, (x, y), glow_size, glow_color, -1)
        
        # Apply blur for soft glow
        glow = cv2.GaussianBlur(glow, (15, 15), 0)
        
        # Blend with original image
        img = cv2.addWeighted(img, 1.0, glow, 0.6, 0)
        
        return img
    
    def update(self):
        """Update all visual effects."""
        self.update_transitions()
        
        # Update particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 0.02
    
    def add_particles(self, x, y, count=10, color=(255, 255, 255), velocity_range=(-5, 5)):
        """Add particle burst effect."""
        for _ in range(count):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': np.random.uniform(*velocity_range),
                'vy': np.random.uniform(*velocity_range),
                'color': color,
                'life': 1.0,
                'size': np.random.uniform(2, 5)
            })
    
    def draw_particles(self, img):
        """Draw all active particles."""
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = particle['life']
                color = tuple(int(c * alpha) for c in particle['color'])
                size = int(particle['size'] * alpha)
                
                cv2.circle(img, (int(particle['x']), int(particle['y'])), size, color, -1)
    
    def apply_all_effects(self, img):
        """Apply all active visual effects to image."""
        img = self.apply_screen_shake(img)
        img = self.apply_fade_effect(img)
        self.draw_particles(img)
        
        return img
