import time
import subprocess

def pic(device=0, f="img.jpg"):
    subprocess.check_output(["fswebcam", "--device", "/dev/video{}".format(device), "--resolution", "1280x960", f])

def test_DTR_False(ser):
    for cam in range(2):
        pic(cam, "cam{}_{}_{}.jpg".format(cam, "DTR_False", "before"))
    ser.dtr=False
    time.sleep(0.5)
    assert ser.cts == False
    for cam in range(2):
        pic(cam, "cam{}_{}_{}.jpg".format(cam, "DTR_False", "after"))


def test_DTR_True(ser):
    for cam in range(2):
        pic(cam, "cam{}_{}_{}.jpg".format(cam, "DTR_True", "before"))
    ser.dtr=True
    time.sleep(0.5)
    assert ser.cts == True
    for cam in range(2):
        pic(cam, "cam{}_{}_{}.jpg".format(cam, "DTR_True", "after"))

