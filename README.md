# Dog At Your Door
Want to get notified when your dog is at the door? You've come to right place.<br><br>
The repository automates the process of right from opening your Camera App(MI Home Security Camera in my case. You can make appropriate changes for any other app in the code) and capturing screen snapshots.

## How it works
It incorporates OpenCV with YOLO(You Only Look Once) to identify dogs whenever a motion is detected.<br><br>
The screen capturing takes place every 3 seconds until motion is detected, post which it starts capturing at a higher fps, and if no dogs are detected, the program returns to its normal mode.<br><br>
On detection of your dog, the program uses GMAIL API(for which you need to generate your token) to notify you, and goes into a 60 sec. sleep, eventually resuming its operations

## To run the code
door_cam_detector.py is the entry point of the code, thus executing --> "python door_cam_detector.py" should get you started.
