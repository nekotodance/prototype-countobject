[README in Japanese](readme-jp.md)

## About prototype-countobject
This is a prototype software to detect objects from webcam video.  
It uses open-cv, PyTorch, and YOLOv5.  

![prototype-countobject](docs/prototype-countobject.jpg)

## Notes.
- We have only checked on a Windows PC with a Geforce GPU, although it may work in other environments!  
- Downloading the library requires more than 1GB of communication. Please run in a high speed/low cost communication environment  
- The entire library requires about 1.6 GB of disk space  
- The first time you start the program, it will take a little extra time because the pre-trained model yolov5s.pt will be downloaded.  

## How to install (for those with knowledge)
#### Required libraries
    pip install torch torchvision opencv-python ultralytics

#### How to run
    py prototype-countobject.py

## How to install (simple method for Windows)
[Download simplified installation zip].  
    https://github.com/nekotodance/prototype-countobject/releases/download/latest/prototype-countobject.zip  

- Install Python (SD standard 3.10.6 recommended)  
- Extract the zip file  
- Right-click “install.ps1” in the extracted folder and select “Run with PowerShell  
- Double-click on the link file to start  

## How to use
#### Preparation
Modify the following parts of the source code to match the webcam you will use.  

- WEBCUM_DEVICE_ID  
Specify the device ID of the webcam.  
Try starting from 0, since it is assigned to the virtual camera, etc.  
- WEBCUM_WIDTH, WEBCUM_HEIGHT  
Specify the video size of the webcam.  
Specify 1920,1080 for FullHD, 1280,720 for HD, etc. according to the webcam to be used.  
- WEBCUM_FPS  
Specify the fps of the webcam.  
Specify 60, 30, 24, etc. according to the webcam used.  

#### Detection object
Modify the following parts of the source code to match the object to be detected.  
target_classes = [“cup”, “cell phone”].  

The default target classes are cups and cell phones.  

#### Key Operations
Q,ESC : Exit  
R : Mirror display on/off  
C : Show/Hide WEB camera image  
V : Detection status display on/off on standard output  

That's all.