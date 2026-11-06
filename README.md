# ASCII Art Projects

This repository contains two small programs that turn visuals into ASCII art:

- **`main.cpp`** — animates a rotating 3D donut in the terminal.
- **`main.py`** — turns a live webcam feed into ASCII art in the terminal.

## Python ASCII camera

You need Python, a webcam, and OpenCV. Install OpenCV with:

```bash
python -m pip install opencv-python
```

Run the camera program with:

```bash
python main.py
```

Allow camera access if your computer asks. The program uses the default camera and mirrors its image. Press **q** to quit.

## C++ rotating donut

The C++ program uses the Windows API (`Sleep`), so it is intended for Windows. With a C++ compiler such as MinGW installed, compile and run it from Command Prompt or PowerShell:

```powershell
g++ main.cpp -o donut.exe
.\donut.exe
```

Press **Ctrl+C** in the terminal to stop the animation.
