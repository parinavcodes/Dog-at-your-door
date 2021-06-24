import cv2
# import pyautogui
# import numpy as np
import time
import os
# from win32api import GetSystemMetrics
# from PIL import ImageGrab
# import windowdim
# import math
# import signal
# import ctypes
# import sys
import motion_detector
import object_identifier
import sms_sender
from window_capture import WindowCapture
from threading import Thread
import admincheck
import email_sender
from imic_launcher import VirtualDesktop
# import psutil
# import threading
# import queue


# print(GetSystemMetrics(0), GetSystemMetrics(1))
# tracemalloc.start()


# out = cv2.VideoWriter("opt.mp4", fourcc, 20.0,
#                       (1920, 1080))

# print(math.ceil(dim['x1']+dim['x1']*0.25), math.ceil(dim['y1']+dim['y1']*0.25),
#       math.ceil(dim['x2']+dim['x2']*0.25), math.ceil(dim['y2']+dim['y2']*0.25))

# print(math.ceil(dim['x2']+dim['x2']*0.25-dim['x1']-dim['x1']*0.25),
#       math.ceil(dim['y2']+dim['y2']*0.25-dim['y1']-dim['y1']*0.25))


class Main:
    def __init__(self):
        # self.visibility_args = queue.Queue()
        # self.visibility_args.put(None)
        # runAsAdmin()
        # if not self.admin_check():
        #     print("giving admin rights")
        #     ctypes.windll.shell32.ShellExecuteW(
        #         None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
        # time.sleep(2)

        # self.visible = True
        self.on = True
        self.notify_type = False
        self.id = None
        self.find_pid()
        self.virtual_desktop = VirtualDesktop()
        self.script_init = 0
        if self.id is not None:
            self.virtual_desktop.move_app("visible")
        while self.id is None:
            # if self.id is None:
            # print("in")
            if self.script_init == 2:
                print("couldn't open")
                self.on = False
                break
            path = self.cam_path_specifier()
            # print(fr"{path[0]} && cd {path[1]} && IMICamera.exe")
            self.virtual_desktop.launch_cam_app(
                fr"{path[0]} && cd {path[1]} && IMICamera.exe")
            start_time = time.time()
            while self.id is None:
                # print("here")
                self.find_pid()
                time.sleep(1)
                if time.time()-start_time >= 20:
                    break
            # print(self.id)
            self.script_init += 1
            # print("IMICamera not found, open IMICamera to enable the application to run")
            # time.sleep(4)
            # exit()
        # time.sleep(30)
        # print("here")
        # self.open_cam_app()
        # self.find_pid()
        # self.lock = threading.RLock()

    # def admin_check(self):
    #     try:
    #         return ctypes.windll.shell32.IsUserAnAdmin()
    #     except:
    #         return False

    def app_handler(self):
        # DogDetection(self.visible)
        email = "Email"
        sms = "SMS"
        # hide = "hide"
        # show = "show"
        while 1:
            print(
                f"Current Notification mode==>{sms if self.notify_type else email} ")
            print(
                f"Press 'N' to change notification mode to {email if self.notify_type else sms}")
            print("Press 'Q' to close the application")
            # print(
            #     f"Press 'V' to {hide if self.visible else show} IMI Camera window")
            toggle = input("Choice: ")

            if toggle == 'q':
                self.on = False
                break
            # elif toggle == 'v':
            #     # with self.lock:
            #     self.visible = not self.visible
            elif toggle == 'n':
                self.notify_type = not self.notify_type
            # self.visibility_args.put(self.visible)
            # print(self.visible)
            # dog_detect(self.visible)
            # print(threading.active_count())
            # if found == False:
            #     break

    def find_pid(self):
        import psutil
        for process in psutil.process_iter():
            # c = c+1
            # Name = process.name()  # Name of the process
            # ID = process.pid  # ID of the process
            if process.name() == "IMICamera.exe":
                # print("Process name =", process.name(), ",", "Process ID =", ID)
                self.id = process.pid
                return

    def cam_path_specifier(self):
        from abspath import resource_path
        with open(resource_path('imicpath.txt'), 'rt') as f:
            return f.read().rstrip('\n').split('\\', 1)


class DogDetection(Thread, Main):
    def __init__(self):
        # self.visible = visible
        Main.__init__(self)
        Thread.__init__(self)
        self.window_setup()
        self.start()

    def run(self):
        import signal
        while self.on:
            # with self.lock:
            found = self.door_cam_image_classifier()
            if found == True:
                print("Application to resume in 60 sec.")
                time.sleep(60)
            else:
                # print("reached here")
                break
        os.kill(self.id, signal.SIGTERM)

    def door_cam_image_classifier(self):
        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # dim = windowdim.window_dimensions()
        # out = cv2.VideoWriter("opt2.mp4", fourcc, 20.0,
        #   (1920, 1080))

        fps = 20.0

        prev = 0
        i = 0
        detect = False
        prev_img = None
        check_interval = True
        # entry = 0
        while self.on:

            # start_time = time.time()
            # print(self.visible)
            # if self.visible == False:
            #     self.window_capture.move_window(1500, 200)
            # else:
            #     self.window_capture.move_window(0, 0)

            time_elapsed = time.time()-prev
            if time_elapsed > 1.0/fps:
                # img = pyautogui.screenshot()
                # img = ImageGrab.grab(
                #     bbox=(math.ceil(dim['x1']+dim['x1']*0.54), math.ceil(dim['y1']+dim['y1']*0.60), math.ceil(dim['x2']-dim['x2']*0.14), math.ceil(dim['y2']-dim['y2']*0.28)))
                img = self.window_capture.screenshot()
                frame = img
                # cv2.imshow('frame', img)
                prev = time.time()
                # frame = np.array(img)
                if i == 0:
                    # prev_img = np.array(img)
                    prev_img = img
                    i = 1
                detect = motion_detector.motion_detector(frame, prev_img)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # identify_res = False
                if detect == True:
                    # print("higher fps")
                    check_interval = False
                    found = object_identifier.object_classifier(frame)
                    # print(found)
                    if found[0] == True:
                        # print("enter")
                        if found[1] == 1:
                            if self.notify_type:
                                sms_sender.messager()
                            else:
                                email_sender.emailer()
                                # out.write(frame)
                        break
                if check_interval == False and detect == False:
                    # print("low fps")
                    check_interval = True
                    # if entry == 0:
                    #     entry = entry+1
                    # elif entry == 1:
                    #     break
                    # time.sleep(6)
                # if identify_res == True:
                # print("dog found")
                # time.sleep(60)
                # found = 1
                # break
                # prev_img = np.array(img)
                prev_img = img
                # cv2.imshow("screen rec.", frame)
                # t = int((1/fps)*1000) 6:54
                # print(int((1/fps)*1000))
                # current, peak = tracemalloc.get_traced_memory()
                # print(
                #     f"Current {i} memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
            # print(1/(time.time()-start_time))
            if cv2.waitKey(int((1/fps)*1000)) == ord('q'):
                break
            if check_interval == True:
                # print("3 sec. pause")
                time.sleep(3)
            # print(1/(time.time()-start_time))

            # i = i+1

        cv2.destroyAllWindows()
        # out.release()
        return detect
        # current, peak = tracemalloc.get_traced_memory()
        # print(
        #     f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")

        # tracemalloc.stop()

    def window_setup(self):
        start_time = time.time()
        while self.id is not None:
            if time.time()-start_time >= 30:
                self.on = False
                # print("time exceed false")
                break
            try:
                self.window_capture = WindowCapture("IMICamera")
                # self.window_capture.bring_window_top(
                #     "no change")
                # # self.window_capture.move_window(0, 0)
                if self.script_init != 0:
                    self.main_door_button_selector()
                else:
                    self.virtual_desktop.move_app()
                    self.virtual_desktop.move_app()

                # self.window_capture.bring_window_top(
                #     "")
                self.on = True
                break
            except:
                # time.sleep(5)
                self.on = False
                # print("false")
        if not self.on:
            print("IMIcam not found")

    def main_door_button_selector(self):
        import pyautogui
        from abspath import resource_path
        # while 1:
        try:
            iconX, iconY = pyautogui.locateCenterOnScreen(
                resource_path('mdoor.jpg'), confidence=0.75)
            pyautogui.click(iconX, iconY, interval=0.25)
        except TypeError:
            # time.sleep(5)
            # print("didnt find")
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
            # mins, secs = divmod(t, 60)
            # timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"waiting for buffer: {t}", end="\r")
            time.sleep(1)
            t += 1
        print("")


if __name__ == "__main__":
    if not admincheck.isUserAdmin():
        # print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        # rc = runAsAdmin(["c:\\Windows\\notepad.exe"])
        rc = admincheck.runAsAdmin()
    else:
        print("You are an admin!")
        rc = 1
        main = DogDetection()
        # Main()
        main.app_handler()

#  pyinstaller --onedir --hidden-import="pkg_resources.py2_warn" --hidden-import="googleapiclient" --hidden-import="apiclient" --add-data "yolo1\yolov4.cfg;yolo1" --add-data "yolo1\yolov4.weights;yolo1" --add-data "mdoor.jpg;." --add-data "playbt.jpg;." --add-data "email_token.pickle;." --add-data "imicpath.txt;." --add-data "VirtualDesktopAccessor.dll;." --add-data "email_list.txt;." --add-data "yolo1\coco.names.txt;yolo1" door_cam_detector.py

    # print("hii")
    # x = input('Press Enter to exit.')

    # dog_detection = DogDetection()
    # visible = 0
    # while 1:
    #     DogDetection()
    #     found = dog_detection.app_handler(visible)
    #     x = input("enter")
    #     if found == False:
    #         break
