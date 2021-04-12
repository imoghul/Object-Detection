# URC Object Detection

This code attempts to find the gate and dice objects from a video stream. It does this by first detecting with countours, 
then it applies the neural network to the image and predicts what type of object it is.

## Dependency and Weights Installation

Make sure you are in this directory before running the setup script

```bash
bash setup.sh
python3 -m pip install opencv-python
python3 -m pip install imutils
```

## Usage

```bash
python3 vision.py (--video/-v or --image/-i) (/path/to/file or webcam number)
```

## More Info

https://docs.google.com/document/d/19NWmppJWI0FFzoLGQPglcDG_pcT4KJGOV6lHz7tane4/edit?usp=sharing