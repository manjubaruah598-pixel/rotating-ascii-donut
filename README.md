# ASCII Vision & Terminal Art

This repository is a small collection of experimental computer-vision and terminal-art projects created for learning and fun.

## Included projects

- `main.cpp` — a rotating 3D ASCII donut animation that runs in the Windows terminal.
- `main.py` — a menu-based program with two modes:
  - ASCII webcam viewer
  - offline face tracker using skin-color detection and simple contour filtering
- `face.py` — standalone face-tracking demo focused on the real-time face detection logic.

## Face tracker note

`face.py` is a beginner-friendly OpenCV project designed to help understand:

- HSV color filtering
- mask cleanup using morphological operations
- contour detection
- bounding-box tracking for a face-like region

This is not a production-grade face-recognition system. It is a simple offline demo built for learning how computer vision works in practice.

## Requirements

### Python

```bash
python -m pip install opencv-python
```

### C++

A Windows C++ compiler such as MinGW or MSVC is required.

## Run the Python programs

From the repository folder:

```bash
python main.py
```

Then choose one of the options:

- `1` for the ASCII camera
- `2` for the face tracker

To run only the face tracker demo:

```bash
python face.py
```

## Run the C++ donut program

```powershell
g++ main.cpp -o donut.exe
.\donut.exe
```

Press `Ctrl+C` or close the terminal to stop the animation.

## Project goals

This repository is meant to demonstrate how creative coding can be done with:

- terminal rendering
- live camera processing
- OpenCV-based experimentation
- beginner-friendly computer vision workflows
