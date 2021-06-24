import cv2
import time
import os
import motion_detector
import object_identifier
import sms_sender
from window_capture import WindowCapture
from threading import Thread
import admincheck
import email_sender
from imic_launcher import VirtualDesktop


class Main:
    def __init__(self):
        self.on = True
        self.notify_type = False
        self.id = None
        self.find_pid()
        self.virtual_desktop = VirtualDesktop()
        self.script_init = 0
        
        if self.id is not None:
            self.virtual_desktop.move_app("visible")
        
        while self.id is None:
            if self.script_init == 2:
                print("couldn't open")
                self.on = False
                break
            
            path = self.cam_path_specifier()
            self.virtual_desktop.launch_cam_app(
                fr"{path[0]} && cd {path[1]} && IMICamera.exe")
            
            start_time = time.time()
            
            while self.id is None:
                self.find_pid()
                time.sleep(1)
                if time.time()-start_time >= 20:
                    break
            self.script_init += 1
            
    def app_handler(self):
        email = "Email"
        sms = "SMS"
        
        while 1:
            print(
                f"Current Notification mode==>{sms if self.notify_type else email} ")
            print(
                f"Press 'N' to change notification mode to {email if self.notify_type else sms}")
            print("Press 'Q' to close the application")
            toggle = input("Choice: ")

            if toggle == 'q':
                self.on = False
                break
            elif toggle == 'n':
                self.notify_type = not self.notify_type
       
    def find_pid(self):
        import psutil
        for process in psutil.process_iter():
            if process.name() == "IMICamera.exe":
                self.id = process.pid
                return

    def cam_path_specifier(self):
        from abspath import resource_path
        with open(resource_path('imicpath.txt'), 'rt') as f:
            return f.read().rstrip('\n').split('\\', 1)


class DogDetection(Thread, Main):
    def __init__(self):
        Main.__init__(self)
        Thread.__init__(self)
        self.window_setup()
        self.start()

    def run(self):
        import signal
        while self.on:
            found = self.door_cam_image_classifier()
            if found == True:
                print("Application to resume in 60 sec.")
                time.sleep(60)
            else:
                break
        os.kill(self.id, signal.SIGTERM)

    def door_cam_image_classifier(self):
        fps = 20.0

        prev = 0
        i = 0
        detect = False
        prev_img = None
        check_interval = True
    
        while self.on:
            time_elapsed = time.time()-prev
            
            if time_elapsed > 1.0/fps:
                img = self.window_capture.screenshot()
                frame = img
                prev = time.time()
                if i == 0:
                    prev_img = img
                    i = 1
                detect = motion_detector.motion_detector(frame, prev_img)
                if detect == True:
                    check_interval = False
                    found = object_identifier.object_classifier(frame)
                    if found[0] == True:
                        if found[1] == 1:
                            if self.notify_type:
                                sms_sender.messager()
                            else:
                                email_sender.emailer()
                        break
                if check_interval == False and detect == False:
                    check_interval = True
                prev_img = img
            
            if cv2.waitKey(int((1/fps)*1000)) == ord('q'):
                break
            if check_interval == True:  #captures screen every three seconds till it detects motion, and once detected, resumes higher fps
                time.sleep(3)
        
        cv2.destroyAllWindows()
        return detect
      
    def window_setup(self):
        start_time = time.time()
        while self.id is not None:
            if time.time()-start_time >= 30:
                self.on = False
                break
            try:
                self.window_capture = WindowCapture("IMICamera")
                if self.script_init != 0:
                    self.main_door_button_selector()
                else:
                    self.virtual_desktop.move_app()
                    self.virtual_desktop.move_app()

                self.on = True
                break
            except:
                self.on = False
        
        if not self.on:
            print("IMIcam not found")

    def main_door_button_selector(self):
        import pyautogui
        from abspath import resource_path
        try:
            iconX, iconY = pyautogui.locateCenterOnScreen(
                resource_path('mdoor.jpg'), confidence=0.75)
            pyautogui.click(iconX, iconY, interval=0.25)
        except TypeError:
            self.on = False
        iconX, iconY = pyautogui.locateCenterOnScreen(
            resource_path('playbt.jpg'), confidence=0.75)
        pyautogui.click(iconX, iconY, interval=0.25)
        self.virtual_desktop.main_desk()
        time.sleep(1)
        self.virtual_desktop.move_app()
        self.virtual_desktop.move_app()
        self.virtual_desktop.main_desk()
        self.buffer_wait()

    def buffer_wait(self):
        t = 0
        while t < 30:
            print(f"waiting for buffer: {t}", end="\r")
            time.sleep(1)
            t += 1
        print("")


if __name__ == "__main__":
    if not admincheck.isUserAdmin():
        rc = admincheck.runAsAdmin()
    else:
        print("You are an admin!")
        rc = 1
        main = DogDetection()
        main.app_handler()
