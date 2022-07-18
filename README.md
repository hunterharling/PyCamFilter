# PyCamFilter
## A Python script to filter the saturation of a webcam for use with video call apps
PyCamFilter allows you to adjust the saturation and color balance of your webcam feed and uses [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) to output this feed to a virtual camera device. This device can then be used like a normal camera for video call apps.

### Setup
For this to work, OBS must be installed.
1. Install OBS
2. Start OBS Virtual Camera
3. Stop OBS Virtual Camera and close OBS

To set up the script, create a virtualenv, clone repo, and install the requirements.
```sh
git clone https://github.com/hunterharling/py-cam-filter.git
cd PyCamFilter
pip install -r requirements.txt
```

### Usage
After installing and starting the OBS Virtual Camera, use the filter by running `python filterCam.py`.
Arguments:
`--camera`: The camera device ID to use as input. Check device IDs to determine which camera to use (it will likely be 0 or 1). Default: 0
`--blue`: Float, amount of saturation to apply to the blue channel. Default: 1.0
`--green`: Float, amount of saturation to apply to the green channel. Default: 1.0
`--red`: Float, amount of saturation to apply to the red channel Default: 1.0
`--all`: Float, amount of saturation to apply to all color channels. Default: 1.0
`--width`: Preferred width of the camera image. Default: 1920
`--height`: Preferred height of the camera image. Default: 1080
`--fps`: Preferred fps of the camera. Default: 30
  
Example:
```sh
python fitlerCam.py --camera 1 --blue 1.1 --green 0.8 --red 0.8 
```
This example uses camera 1 as the input device, desaturates the red and green channels by 20%, and saturates the blue channel by 10%

You can also increase the saturation and apply to all color channels:
```sh
python fitlerCam.py --camera 1 --all 1.5
```
