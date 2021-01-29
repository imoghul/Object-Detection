# URC Object Detection

This code attempts to find the gate and dice objects from a video stream. It does this by first detecting with countours, 
then it applies the neural network to the image and predicts what type of object it is.

## Dependency Installation

```bash
python3 -m pip install opencv-python
python3 -m pip install imutils
```

## Usage

```bash
python3 vision.py (--video/-v or --image/-i) /path/to/file
```