# ♟️ Hand Gesture Chess

<div align="center">

![Chess Banner](https://img.shields.io/badge/🎮-Hand_Gesture_Chess-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7%2B-green?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-red?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-orange?style=for-the-badge&logo=google)

*A revolutionary chess experience where your hands become the pieces*

</div>

---

## 🌟 Overview

Experience chess like never before! **Hand Gesture Chess** transforms your webcam into an interactive chessboard where you control pieces using intuitive hand gestures. No mouse, no keyboard - just natural hand movements to play chess against an AI opponent.

Using advanced computer vision with MediaPipe, the system detects your hand gestures in real-time, allowing you to pinch, drag, and drop chess pieces with precision and fluidity.

---

## ✨ Key Features

### 🎯 **Intuitive Gesture Controls**
- **Pinch to Select** - Simply pinch your thumb and index finger to pick up pieces
- **Drag to Move** - Maintain the pinch while dragging to move pieces
- **Release to Drop** - Release your fingers to place pieces on the board

### 🎨 **Modern Visual Experience**
- **4 Beautiful Themes** - Classic Wood, Marble, Modern, and Dark themes
- **Smooth Animations** - Fluid piece movements with particle effects
- **Visual Feedback** - Real-time highlights for legal moves and selections
- **Modern UI** - Gradient borders, shadows, and rounded corners

### 🎮 **Enhanced Gameplay**
- **Interactive HUD** - Turn indicators, move history, and game status
- **Settings Panel** - Customize themes and toggle animations
- **Gesture Guide** - On-screen visual instructions
- **Captured Pieces Display** - Track material advantage
- **Game Alerts** - Check, checkmate, and stalemate notifications

### ⚡ **Performance**
- **Real-time Processing** - 60 FPS smooth gameplay
- **Optimized Computer Vision** - Efficient hand tracking
- **Responsive Controls** - Minimal latency gesture detection

---

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.7 or higher
- Webcam (built-in or external)
- Windows, macOS, or Linux

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/hand-gesture-chess.git
   cd hand-gesture-chess
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

That's it! The game will automatically detect your webcam and start tracking your hand movements.

---

## 🎮 Controls & Interface

### 👆 **Gesture Controls**
| Gesture | Action | Description |
|---------|--------|-------------|
| 👌 **Pinch** | Select Piece | Thumb + index finger together |
| ✋ **Drag** | Move Piece | Maintain pinch while moving |
| 🖐️ **Release** | Drop Piece | Open fingers to place piece |

### ⌨️ **Keyboard Shortcuts**
| Key | Function |
|-----|----------|
| **T** | Toggle Settings Panel |
| **G** | Show/Hide Gesture Guide |
| **↑↓** | Navigate Settings Menu |
| **Enter** | Select Settings Option |
| **ESC** | Exit Game |

---

## 🎨 Visual Themes

### 🌳 **Classic Wood**
Traditional chessboard with warm wood tones and classic piece styling

### 💎 **Marble**
Elegant marble board with high contrast for clarity

### 🌌 **Modern**
Contemporary design with blue accents and clean aesthetics

### 🌑 **Dark**
Dark theme optimized for low-light environments

---

## 🏗️ Project Architecture

```
hand-gesture-chess/
├── 📁 chess_cv/                    # Core application logic
│   ├── 🎯 app.py                   # Main application and game loop
│   ├── 🎨 theme.py                 # Visual theme system
│   ├── ♟️ chessboard.py            # Board rendering and UI
│   ├── 👋 hand_tracker.py          # MediaPipe hand tracking
│   ├── 🎭 gesture.py               # Gesture detection logic
│   ├── 🤖 engine.py                # Chess AI engine
│   ├── 📊 hud.py                   # Heads-up display overlay
│   ├── ⚙️ settings.py              # Settings panel interface
│   ├── 📖 gesture_guide.py         # Interactive help system
│   ├── ✨ animations.py            # Piece movement animations
│   ├── 🚨 alerts.py                # Game state notifications
│   ├── 🏆 captured.py              # Captured pieces display
│   └── 📁 assets/                  # Piece images and resources
├── 🚀 main.py                      # Application entry point
├── 📋 requirements.txt             # Python dependencies
├── 🤖 hand_landmarker.task         # MediaPipe ML model
└── 📄 README.md                    # This file
```

---

## 🔧 Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **OpenCV** | Computer vision and image processing |
| **MediaPipe** | Hand gesture detection and tracking |
| **python-chess** | Chess game logic and rules |
| **NumPy** | Numerical computations and array operations |

---

## 🎯 How It Works

1. **Camera Input** - Webcam captures real-time video
2. **Hand Detection** - MediaPipe identifies hand landmarks
3. **Gesture Recognition** - Custom algorithm detects pinch/drag/release
4. **Coordinate Mapping** - Hand position mapped to chessboard squares
5. **Game Logic** - Chess engine validates moves and responds
6. **Visual Feedback** - UI updates with animations and effects

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### 🐛 Bug Reports
Found a bug? Please open an issue with:
- Description of the problem
- Steps to reproduce
- Your system information
- Screenshots if applicable

---

## 📱 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.7+ | 3.9+ |
| **RAM** | 4GB | 8GB |
| **CPU** | Dual-core | Quad-core |
| **Camera** | 720p @ 30fps | 1080p @ 60fps |
| **OS** | Windows 10/macOS 10.14/Ubuntu 18.04 | Latest versions |

---

## 🎮 Tips for Best Experience

### ✅ **Optimal Setup**
- Ensure good lighting for better hand detection
- Position camera to capture your upper body and hands
- Wear contrasting colored clothing for better tracking
- Keep hands within camera frame during gameplay

### 🎯 **Gesture Tips**
- Make clear, deliberate pinch gestures
- Maintain steady hand position while dragging
- Release fingers decisively for accurate piece placement
- Use your dominant hand for better control

---

## 🏆 Developer

<div align="center">

**Created with ❤️ by [tubakhxn](https://github.com/tubakhxn)**

*Pushing the boundaries of human-computer interaction through gesture-based gaming*

</div>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe Team** - For the amazing hand tracking technology
- **OpenCV Community** - For computer vision tools and support
- **python-chess** - For robust chess game logic
- **Chess Community** - For inspiring innovative gameplay experiences

---

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/<your-username>/hand-gesture-chess?style=social)
![GitHub forks](https://img.shields.io/github/forks/<your-username>/hand-gesture-chess?style=social)
![GitHub issues](https://img.shields.io/github/issues/<your-username>/hand-gesture-chess)
![GitHub license](https://img.shields.io/github/license/<your-username>/hand-gesture-chess)

**⭐ Star this repo if you find it interesting!**

</div>

---


