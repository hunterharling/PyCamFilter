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


def saturateChannel(img, colorChannel, amount):
    imgRGB = img.copy()

    # channel: 0=B, 1=G, 2=R
    channel = 0
    if colorChannel == "R":
        channel = 2
    elif colorChannel == "G":
        channel = 1

    imgRGB[:, :, channel] = np.clip(imgRGB[:, :, channel] * amount, 0, 255)

    return imgRGB


def filteredCam(camera, colorChannel, saturationAmount, fps, pref_width, pref_height):
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

            if colorChannel == "A":
                frame = saturateImg(frame, saturationAmount)
            else:
                frame = saturateChannel(
                    frame, colorChannel, saturationAmount
                )

            cam.send(frame)
            cam.sleep_until_next_frame()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0,
                        help="ID of webcam input device (default: 0)")
    parser.add_argument("--channel", choices=["R", "G", "B", "A"],
                        default="A", help="Channel to saturate: R, G, B, or A (all)")
    parser.add_argument("--amount", type=float, default=1.0,
                        help="Amount of saturation to be applied")
    parser.add_argument("--fps", type=int, default=30,
                        help="Frames per second")
    parser.add_argument("--width", type=int, default=1920,
                        help="Preferred width")
    parser.add_argument("--height", type=int, default=1080,
                        help="Preferred height")
    args = parser.parse_args()

    filteredCam(args.camera, args.channel, args.amount, args.fps, args.width, args.height)
