import pyvirtualcam
import numpy as np
import cv2
import argparse


def saturateImg(img, amount):
    # convert to float32 to prevent overflow
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")

    # adjust saturation
    (h, s, v) = cv2.split(imgHSV)
    s = s * amount
    s = np.clip(s, 0, 255)

    # merge and convert to uint8
    imgHSV = cv2.merge([h, s, v])
    imgRGB = cv2.cvtColor(imgHSV.astype("uint8"), cv2.COLOR_HSV2BGR)

    return imgRGB


def saturateChannels(img, colorChannels):
    imgRGB = img.copy()

    # RGB saturation
    s = colorChannels[3]
    if s > 1.0:
        imgRGB = saturateImg(img, s)

    # B,G,R channels
    for i in range(3):
        imgRGB[:, :, i] = np.clip(imgRGB[:, :, i] * colorChannels[i], 0, 255)

    return imgRGB


def filteredCam(camera, colorChannels, fps, pref_width, pref_height):
    vc = cv2.VideoCapture(camera)

    vc.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
    vc.set(cv2.CAP_PROP_FPS, fps)

    width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_in = vc.get(cv2.CAP_PROP_FPS)

    print(f'Webcam capture started ({width}x{height} @ {fps_in}fps)')

    with pyvirtualcam.Camera(width=width, height=height, fmt=pyvirtualcam.PixelFormat.BGR, fps=fps_in) as cam:
        print(f'Using virtual camera: {cam.device}')

        while True:
            ret, frame = vc.read()
            if not ret:
                raise RuntimeError('Error fetching frame')

            frame = saturateChannels(frame, colorChannels)

            cam.send(frame)
            cam.sleep_until_next_frame()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0,
                        help="ID of webcam input device (default: 0)")
    parser.add_argument("--fps", type=int, default=30,
                        help="Frames per second")
    parser.add_argument("--width", type=int, default=1920,
                        help="Preferred width")
    parser.add_argument("--height", type=int, default=1080,
                        help="Preferred height")
    parser.add_argument("--red", type=float, default=1.0, help="Red saturation")
    parser.add_argument("--green", type=float, default=1.0, help="Green saturation")
    parser.add_argument("--blue", type=float, default=1.0, help="Blue saturation")
    parser.add_argument("--all", type=float, default=1.0, help="RGB saturation")
    args = parser.parse_args()

    filteredCam(
        args.camera, 
        [args.blue, args.green, args.red, args.all,],
        args.fps, 
        args.width, 
        args.height
    )
