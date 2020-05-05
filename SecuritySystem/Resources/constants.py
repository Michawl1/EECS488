"""
Constants for the use of the application
"""
DEFAULT_PORT = 6969

NoRec = {
    "width": 853,
    "height": 480,
    "fps": 0,
    "fpspoll": 3
}
LowRes = {
    "width": 853,
    "height": 480,
    "fps": 3,
    "fpspoll": 3
}
MedRes = {
    "width": 1280,
    "height": 720,
    "fps": 6,
    "fpspoll": 6
}
HighRes = {
    "width": 1920,
    "height": 1080,
    "fps": 10,
    "fpspoll": 10
}

States = [NoRec, LowRes, MedRes, HighRes]

ImgPath = "./Image"

MaxCameras = 4
